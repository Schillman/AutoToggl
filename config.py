settings = {
    "token": "Toggl API KEY found under your Profil on toggl.com",
    # Only one of the Report settings can be set to True at a given time. if multiple reports are set to True nothing will happen.
    "reportWork": True,
    "reportVacation": False,
    "reportParentalLeave": False,
    # ----
    "country": "Sweden",  # Used to get the countries holidays.
    "fullDayHours": 8,  # Number of hours you report per day ie. No. of hours you work.
    "weeks": 1,  # Number of weeks you'd like to go back and report time on, if any remaining hours remains, it will report the entries given in the inputObject (Note* It will add the antire entry to that day and not just the hours that was missing.)
    "allowPreviousMonth": False,  # If set to True, it will allow you to report time for the previous month as well. (Note* if the previous month locked then the code will error out
    "startDate": None,  # "2021-08-02",
    "endDate": None,  # "2021-08-03",
}
# https://github.com/toggl/toggl_api_docs/blob/master/chapters/time_entries.md
# Most of the Parameters below are self explainatory but you could also find more info at above link.
# All entries will be created from 8 am and onwards.

if (
    settings["reportWork"] == True
    and settings["reportVacation"] == False
    and settings["reportParentalLeave"] == False
):
    inputObj = {
        "Mon": {
            "Customers": {
                "CustomerName": {
                    "Name": "CustomerName",
                    "Description": "WhatEverYouLike",
                    "ProjectID": 1676203124,  # Easiest way to find this is to open the project via track.toggl.com
                    # it will look something like this https://track.toggl.com/1959394/projects/<ProjectID>/tasks
                    "DurationInHours": 8,  # How much time you'de like to report on this day for this customer.
                    "startTime": "08:00",
                    "billable": True,
                },
            }
        },
        "Tue": {
            "Customers": {
                "CustomerName": {
                    "Name": "CustomerName",
                    "Description": "WhatEverYouLike",
                    "ProjectID": 1676203124,
                    "DurationInHours": 4,
                    "startTime": "08:00",
                    "billable": True,
                },
                "CustomerName2": {
                    "Name": "CustomerName2",
                    "Description": "WhatEverYouLike",
                    "ProjectID": 1234567890,
                    "DurationInHours": 4,
                    "startTime": "12:00",
                    "billable": True,
                },
            }
        },
        "Wed": {
            "Customers": {
                "CustomerName": {
                    "Name": "CustomerName",
                    "Description": "WhatEverYouLike",
                    "ProjectID": 1676203124,
                    "DurationInHours": 8,  # How much time you'de like to report on this day for this customer.
                    "startTime": "08:00",
                    "billable": True,
                },
            }
        },
        "Thu": {
            "Customers": {
                "CustomerName": {
                    "Name": "CustomerName",
                    "Description": "WhatEverYouLike",
                    "ProjectID": 1676203124,
                    "DurationInHours": 8,  # How much time you'de like to report on this day for this customer.
                    "startTime": "08:00",
                    "billable": True,
                },
            }
        },
        "Fri": {
            "Customers": {
                "CustomerName": {
                    "Name": "CustomerName",
                    "Description": "WhatEverYouLike",
                    "ProjectID": 1676203124,
                    "DurationInHours": 8,  # How much time you'de like to report on this day for this customer.
                    "startTime": "08:00",
                    "billable": True,
                },
            }
        },
    }
elif (
    settings["reportVacation"] == True
    and settings["reportParentalLeave"] == False
    and settings["reportWork"] == False
):
    inputObj = {
        "Mon": {
            "Customers": {
                "YourCompanyName": {
                    "Name": "YourCompanyName",
                    "Description": "WhatEverYouLike",
                    "ProjectID": 1671243124,
                    "DurationInHours": 8,
                    "startTime": "08:00",
                    "billable": False,
                },
            }
        },
        "Tue": {
            "Customers": {
                "YourCompanyName": {
                    "Name": "YourCompanyName",
                    "Description": "WhatEverYouLike",
                    "ProjectID": 1671243124,
                    "DurationInHours": 8,
                    "startTime": "08:00",
                    "billable": False,
                },
            }
        },
        "Wed": {
            "Customers": {
                "YourCompanyName": {
                    "Name": "YourCompanyName",
                    "Description": "WhatEverYouLike",
                    "ProjectID": 1671243124,
                    "DurationInHours": 8,
                    "startTime": "08:00",
                    "billable": False,
                },
            }
        },
        "Fri": {
            "Customers": {
                "YourCompanyName": {
                    "Name": "YourCompanyName",
                    "Description": "WhatEverYouLike",
                    "ProjectID": 1671243124,
                    "DurationInHours": 8,
                    "startTime": "08:00",
                    "billable": False,
                },
            }
        },
    }
elif (
    settings["reportParentalLeave"] == True
    and settings["reportVacation"] == False
    and settings["reportWork"] == False
):
    inputObj = {
        "Mon": {
            "Customers": {
                "YourCompanyName": {
                    "Name": "YourCompanyName",
                    "Description": "Parental Leave",
                    "ProjectID": 123420425,
                    "DurationInHours": 8,
                    "startTime": "08:00",
                    "billable": False,
                },
            }
        },
        "Tue": {
            "Customers": {
                "YourCompanyName": {
                    "Name": "YourCompanyName",
                    "Description": "Parental Leave",
                    "ProjectID": 123420425,
                    "DurationInHours": 8,
                    "startTime": "08:00",
                    "billable": False,
                },
            }
        },
        "Wed": {
            "Customers": {
                "YourCompanyName": {
                    "Name": "YourCompanyName",
                    "Description": "Parental Leave",
                    "ProjectID": 123420425,
                    "DurationInHours": 8,
                    "startTime": "08:00",
                    "billable": False,
                },
            }
        },
        "Thu": {
            "Customers": {
                "YourCompanyName": {
                    "Name": "YourCompanyName",
                    "Description": "Parental Leave",
                    "ProjectID": 123420425,
                    "DurationInHours": 8,
                    "startTime": "08:00",
                    "billable": False,
                },
            }
        },
        "Fri": {
            "Customers": {
                "YourCompanyName": {
                    "Name": "YourCompanyName",
                    "Description": "Parental Leave",
                    "ProjectID": 123420425,
                    "DurationInHours": 8,
                    "startTime": "08:00",
                    "billable": False,
                },
            }
        },
    }
else:
    print('Warning: Only one "report setting" can be set to True at a given time.')
