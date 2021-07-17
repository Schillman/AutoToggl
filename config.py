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
                },
                "CustomerName2": {
                    "Name": "CustomerName2",
                    "Description": "WhatEverYouLike",
                    "ProjectID": 1234567890,
                    "DurationInHours": 4,
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
                },
            }
        },
    }
else:
    print('Warning: Only one "report setting" can be set to True at a given time.')
