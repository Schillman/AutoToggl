import base64
import collections
import importlib
import json
import os
import sys
import time
from collections import OrderedDict, defaultdict
from datetime import date, datetime, timedelta
from operator import itemgetter

import config


def cls():
    os.system("cls" if os.name == "nt" else "clear")


def install_and_import(package):
    try:
        importlib.import_module(package)
    except ImportError:
        import pip

        pip.main(["install", package])
    finally:
        globals()[package] = importlib.import_module(package)


install_and_import("holidays")
install_and_import("requests")

cls()


def apiCall(token, url, method="GET", body=None):
    authToken = token + ":api_token"
    headers = {
        "Authorization": "Basic "
        + base64.b64encode(authToken.encode("ascii")).decode("utf-8")
    }
    if method == "GET":
        response = requests.get(url, headers=headers)
    elif method == "POST" and body:
        response = requests.post(url, headers=headers, data=(json.dumps(body)))
    else:
        raise ValueError("Missing HTTP method or Body")

    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(
            (
                "{} HTTP call was not successfull"
                + "\n"
                + str(e.args[0])
                + "\n"
                + "Response: "
                + str(e.response.text)
            ).format(method)
        )
        sys.exit()

    # status code 200
    return response


def whereObject(list, Attrib, searchWord, valueName):
    filter = []
    for v in list:
        if v[str(Attrib)].startswith(searchWord):
            filter.append(v[str(valueName)])
    return filter


class LogEntry:
    def __init__(self, input, countryHoliday):
        Holidays = holidays.CountryHoliday(countryHoliday)
        self.date = input
        self.time = 0
        self.remaining = 0
        if input in Holidays:
            self.holiday = Holidays[date(input.year, input.month, input.day)]
        else:
            self.holiday = False

    def convertToHours(self):
        if self.time != 0:
            self.time = float(
                self.time / 3600
            )  # cast non-zero times as float, making empty days easy to see
        if self.remaining != 0:
            self.remaining = float(self.remaining / 3600)


class AutoToggl:
    def __init__(self, projects, **Settings):
        # Variables needed throughout the code.
        self.token = Settings["token"]
        self.HttpEncode = Settings["HttpEncode"]
        self.CurrentTimeZone = Settings["CurrentTimeZone"]

        country = Settings["country"]
        fullDayHours = Settings["fullDayHours"]

        if Settings["startDate"] and Settings["endDate"]:
            print(
                "\n---\nLooking for time to report from {} to {}\n---\n".format(
                    Settings["startDate"], Settings["endDate"]
                )
            )
            self.startDate = date.fromisoformat(Settings["startDate"])
            endDate = date.fromisoformat(Settings["endDate"])
            self.specificDates = True
        else:
            print(
                "\n---\nLooking for time to report from {} till today\n---\n".format(
                    (date.today() - timedelta(weeks=Settings["weeks"]))
                )
            )
            self.startDate = date.today() - timedelta(weeks=Settings["weeks"])
            endDate = date.today()
            self.specificDates = False

        if not self.specificDates:
            print(
                f"Reporting {Settings['weeks']} weeks back\nNote*** AutoToggl by Schillman will only report time for the current active month even if the last month's dates are shown below.\n"
            )

        fullDaySeconds = fullDayHours * 3600
        entryUrl = (
            "https://api.track.toggl.com/api/v8/time_entries?start_date="
            + str(self.startDate)
            + "T00:00:00"
            + self.HttpEncode
        )
        self.time_entries = (apiCall(self.token, entryUrl, "GET")).json()
        self.projects = projects
        self.time_log = OrderedDict()
        # Prepare dates to be able to itirate through them.
        while self.startDate <= endDate:
            self.time_log[str(self.startDate)] = LogEntry(self.startDate, country)
            self.startDate = self.startDate + timedelta(days=1)
        for day in self.time_log.values():
            entry_date = str(day.date)
            # Get all the entries of a specific date
            nonCompleteEntry = whereObject(
                self.time_entries, "start", entry_date, "duration"
            )

            # Calculate Reported Time
            self.time_log[entry_date].time = self.time_log[entry_date].time + sum(
                nonCompleteEntry
            )

            # Calculate Remaining Time
            if (
                self.time_log[entry_date].remaining == 0
                and self.time_log[entry_date].holiday == False
            ):
                self.time_log[entry_date].remaining = self.time_log[
                    entry_date
                ].remaining + (fullDaySeconds - sum(nonCompleteEntry))

    def Gather_And_Report(self):
        timeReport = dict()
        fullReport = []
        DAY_INDEX = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        newTimeEntryURL = "https://api.track.toggl.com/api/v8/time_entries"
        # Printing out the headers only, for readabillity.
        print(
            "{0:7} | {1:^10} | {2:^8} | {3:^9} | {4}".format(
                "Weekday",
                "Date",
                "Reported (h)",
                "Remaining (h)",
                "Holiday (Native language)",
            )
        )
        for entry in self.time_log.values():
            entry.convertToHours()

            weekday = DAY_INDEX[entry.date.weekday()]

            timeReport = {
                "WeekDay": weekday,
                "Date": entry.date,
                "Time": entry.time,
                "Remaining": entry.remaining,
                "Holiday": entry.holiday,
            }

            fullReport.append((timeReport.copy()))
            # Only show the remaining if not holiday or saturday
            if weekday == "Sat":
                print(
                    "{0:^7}   {1}   {2:^12}  {3:^13}".format(
                        weekday, entry.date, entry.time, 0
                    )
                )
            elif not entry.holiday:
                print(
                    "{0:^7}   {1}   {2:^12}  {3:^13}".format(
                        weekday, entry.date, entry.time, entry.remaining
                    )
                )
            else:
                print(
                    "{0:^7}   {1}   {2:^12}  {3:^13}    {4}".format(
                        weekday,
                        entry.date,
                        entry.time,
                        entry.remaining,
                        str(entry.holiday),
                    )
                )
        print("\n")
        apiOutCome = dict()
        reported = []
        for entry in fullReport:
            if (
                self.projects.get((entry["WeekDay"])) != None
                and entry["Remaining"] != 0
                and entry["Holiday"] == False
                and (
                    entry["Date"].month
                    == datetime.today().month  # Only report current active month
                    or self.specificDates
                )
            ):

                project = self.projects[(entry["WeekDay"])]["Customers"].values()
                for customer in project:
                    time_entry = {
                        "time_entry": {
                            "pid": customer["ProjectID"],
                            "start": str(entry["Date"])
                            + "T{0}:00.000".format(customer["startTime"])
                            + self.CurrentTimeZone,
                            "duration": customer["DurationInHours"] * 3600,
                            "description": customer["Description"],
                            "billable": customer["billable"],
                            "created_with": "AutoToggl by Schillman",
                        }
                    }

                    outCome = apiCall(
                        self.token, newTimeEntryURL, "POST", time_entry
                    ).json()
                    if outCome:
                        apiOutCome = {
                            "DurationInHours": customer["DurationInHours"],
                            "Customer": customer["Name"],
                            "Weekday": entry["WeekDay"],
                            "Date": str(entry["Date"]),
                            "Description": customer["Description"],
                        }

                        reported.append((apiOutCome.copy()))

                    else:
                        print(outCome.text)
        if reported:
            # Group by customer for a more neatly display
            grouped = collections.defaultdict(list)
            for item in reported:
                grouped[item["Date"]].append(item)

            print(
                "\n--- The following time was reported with AutoToggl by Schillman ---"
            )
            for groupDate in grouped.values():
                print(
                    "\n{0} - {1}".format(groupDate[0]["Weekday"], groupDate[0]["Date"])
                )
                for entry in groupDate:
                    print(
                        "CompanyName: {0}\n\tDuration: {1}\n\tDescription: {2}".format(
                            entry["Customer"],
                            entry["DurationInHours"],
                            entry["Description"],
                        )
                    )
        if not reported:
            print("----\nNo remaining hours to report on.\n----\n")


inputObject = config.inputObj

# Settings - Keyword arguments to be passed trough to the function AutoToggl
Settings = {
    "token": config.settings["token"],
    "country": config.settings["country"],
    "fullDayHours": config.settings["fullDayHours"],
}

if config.settings["startDate"] and config.settings["endDate"]:
    Settings["startDate"] = config.settings["startDate"]
    Settings["endDate"] = config.settings["endDate"]
    Settings["weeks"] = None
elif config.settings["weeks"]:
    Settings["startDate"] = None
    Settings["endDate"] = None
    Settings["weeks"] = config.settings["weeks"]
else:
    print(
        "Missing setting parameter in config.py. Either 'weeks' and/or 'start/endDate'"
    )

if time.localtime().tm_isdst == 0:
    offset = time.timezone
else:
    offset = time.altzone

TimeDiff = int(offset / 60 / 60 * -1)

if TimeDiff >= 0:
    Settings["HttpEncode"] = "%2B0" + str(TimeDiff) + "%3A00"
    Settings["CurrentTimeZone"] = "+0" + str(TimeDiff) + ":00"
else:
    Settings["HttpEncode"] = "%2D0" + str(TimeDiff) + "%3A00"
    Settings["CurrentTimeZone"] = "-0" + str(TimeDiff) + ":00"

Info = AutoToggl(inputObject, **Settings)
Info.Gather_And_Report()
"\n\n\n"
input("Press Enter to Exit...")
