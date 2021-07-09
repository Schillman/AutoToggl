import base64
import collections
import importlib
import json
import os
import time
from collections import OrderedDict, defaultdict
from datetime import date, datetime, timedelta
from operator import itemgetter

import holidays
import requests

import config


def apiCall(token, url, method="GET", body=None):
    authToken = token + ":api_token"
    headers = {
        "Authorization": "Basic "
        + base64.b64encode(authToken.encode("ascii")).decode("utf-8")
    }

    if method == "GET":
        return requests.get(url, headers=headers)
    elif method == "POST" and body:
        return requests.post(url, headers=headers, data=(json.dumps(body)))
    else:
        raise ValueError("Missing HTTP method or Body")


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
    def __init__(self, projects, weeks):
        self.startDate = date.today() - timedelta(weeks=weeks)
        fullDaySeconds = fullDayHours * 3600
        entryUrl = (
            "https://api.track.toggl.com/api/v8/time_entries?start_date="
            + str(self.startDate)
            + "T00:00:00"
            + HttpEncode
        )
        self.time_entries = (apiCall(token, entryUrl, "GET")).json()
        self.projects = projects
        self.time_log = OrderedDict()
        # Prepare dates to be able to itirate through them.
        while self.startDate <= date.today():
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

            if not entry.holiday:  # Only show the remaining if not holiday or saturday
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
                        (entry.remaining)
                        if (weekday == "Sat" or weekday == "Sun")
                        else 0,
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
            ):

                project = self.projects[(entry["WeekDay"])]["Customers"].values()
                for customer in project:
                    time_entry = {
                        "time_entry": {
                            "pid": customer["ProjectID"],
                            "start": str(entry["Date"])
                            + "T08:00:00.000"
                            + CurrentTimeZone,
                            "duration": customer["DurationInHours"] * 3600,
                            "description": customer["Description"],
                            "created_with": "AutoToggl-BySchillman",
                        }
                    }
                    outCome = (
                        apiCall(token, newTimeEntryURL, "POST", time_entry)
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

            print("\n--- The following timereports has been made by AutoToggl™ ---")
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


# Settings
token = config.settings["token"]
country = config.settings["country"]
fullDayHours = config.settings["fullDayHours"]
weeks = config.settings["weeks"]
inputObject = config.inputObj

if time.localtime().tm_isdst == 0:
    offset = time.timezone
else:
    offset = time.altzone

TimeDiff = int(offset / 60 / 60 * -1)

if TimeDiff >= 0:
    HttpEncode = "%2B0" + str(TimeDiff) + "%3A00"
    CurrentTimeZone = "+0" + str(TimeDiff) + ":00"
else:
    HttpEncode = "%2D0" + str(TimeDiff) + "%3A00"
    CurrentTimeZone = "-0" + str(TimeDiff) + ":00"

Info = AutoToggl(inputObject, weeks)
Info.Gather_And_Report()
