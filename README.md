# AutoToggl
An automated way to toggl your day to day working hours.

Toggl API Key can be found under [toggl profile](https://track.toggl.com/profile)

# Config.py

Firstly one need to configure the config.py file. Parameters are described below.

### Toggle API
Most of the Parameters below are self explainatory but you could also find more info at below link.
https://github.com/toggl/toggl_api_docs/blob/master/chapters/time_entries.md

```python
settings = { 
"token": "Toggl API KEY found under your Toggl Profil",
# Nothing hinder you from encrypt this key and import whatever module you need to read it.
# ***Note*** Do the Import prior to this Settings block if doing so.

# Only one of the *report* settings can be set to True at a given time.
# ***Note*** if multiple reports are set to True nothing will happen.
"reportWork": True,
"reportVacation": False,
"reportParentalLeave": False,

"country": "Sweden", # Used to get the countries holidays.*
"fullDayHours": 8, # Number of hours you report per day... ie. Number of hours you work.*
                   # All entries will be created from 8 am and meet your fullDayHours setting.

# Either Use **weeks** or **startDate** and **endDate**
"weeks": 1, # Number of weeks you'd like to go back and report time on, if any remaining hours remains.
            # (**Note** It will add the antire entry to that day and not just the hours that was missing.)*

# Below settings will report time for the dates specified and those within that range.
"startDate": None, # Example: "2021-08-02",
"endDate": None, # Example: "2021-08-15",

}

```

### For reporting <u>**Work**</u> activites add your inputObject as below.
<br />

``` python
if (
    settings["reportWork"] == True
    and settings["reportVacation"] == False
    and settings["reportParentalLeave"] == False
):
    inputObj = {
        "Mon": {
            "Customers": {
                "CustomerName":{
                    "Name": "CustomerName",
                    "Description": "WhatEverYouLike",
                    "ProjectID": 1676203124, # Easiest way to find this **id** is to open the project via track.toggl.com 
                        # it will look something like this https://track.toggl.com/1959394/projects/<ProjectID>/tasks
                    "DurationInHours": 8, #  How much time you'de like to report on this day for this customer.
                },
            }
        },

        # You can have multiple customers on a given day, see below

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

        # You can have multiple customers on a given day, see above

        "Wed": {
            "Customers": {
                "CustomerName": {
                    "Name": "CustomerName",
                    "Description": "WhatEverYouLike",
                    "ProjectID": 1676203124,
                    "DurationInHours": 8,
                },
            }
        },

        "Thu": {
            "Customers": {
                "CustomerName": {
                    "Name": "CustomerName",
                    "Description": "WhatEverYouLike",
                    "ProjectID": 1676203124,
                    "DurationInHours": 8,
               },
            }
        },

        "Fri": {
            "Customers": {
                "CustomerName": {
                    "Name": "CustomerName",
                    "Description": "WhatEverYouLike",
                    "ProjectID": 1676203124,
                    "DurationInHours": 8,
                },
            }
        },
    }
```

### For reporting <u>**Vacation**</u> activites add your inputObject as below.
<br />

``` python
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
```

### For reporting <u>**ParentalLeave**</u> activites add your inputObject as below.
<br />

``` python
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
                    "ProjectID": 1671243124,
                    "DurationInHours": 8,
                },
            }
        },
        "Tue": {
            "Customers": {
                "YourCompanyName": {
                    "Name": "YourCompanyName",
                    "Description": "Parental Leave",
                    "ProjectID": 1671243124,
                    "DurationInHours": 8,
                },
            }
        },
        "Wed": {
            "Customers": {
                "YourCompanyName": {
                    "Name": "YourCompanyName",
                    "Description": "Parental Leave",
                    "ProjectID": 1671243124,
                    "DurationInHours": 8,
                },
            }
        },
        "Fri": {
            "Customers": {
                "YourCompanyName": {
                    "Name": "YourCompanyName",
                    "Description": "Parental Leave",
                    "ProjectID": 1671243124,
                    "DurationInHours": 8,
                },
            }
        },
    }
else:
    print('Warning: Only one "report setting" can be set to True at a given time.')
```
