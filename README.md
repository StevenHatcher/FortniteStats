# **FortniteStatLibrary**
 **Access and utilize the statistics of public accounts on fortnitetracker.com**

The more info that is given to the functions, the more specific the the results will be. 
For example, 
- *Function call:* get_player_stats(profile_data, category="all", ranked=True, platform="all", season=None, gamemode="all", data="KD", option="value")
- *Example return:* 0.61 (The player's K/D ratio across all platforms, gamemodes, and seasons.)
<br>Alternatively:<br>
- *Function call:* player_stats = get_player_stats(player_data, category="stats", ranked=False)
- *Example return:* [every single unranked statistic for every gamemode and platform]

# Functions:
## get_player_data()
This function returns all of the JSON data of the given player if their account is public
**Parameters:**
- <ins>username</ins>: The player's username
    - Default is None
- <ins>maximize</ins>: If False, the chromedriver webpage will minimize when it opens
    - True, False (default)
**Returns:** JSON data of the given player
**Example:** player_data = get_player_data("username")


## get_player_stats()
Function to return the value of a specific stat given the platform, gamemode, stat, and option of that stat

**Parameters:**
- <ins>profile_data</ins>: The JSON data of the player
- <ins>category</ins>: "stats" (default), "last7DaysStats", "last30DaysStats"
- <ins>ranked</ins>: True, False (default)
- <ins>platform</ins>: None (default), "all", "touch", "kbm", "gamepad", "preferred" (gives data for player's preferred platform)
- <ins>season</ins>: None (default), [any number], "current" (gives current season)
- <ins>gamemode</ins>: None (default), "all", "solo", "duos", "trios", "squads", "ltm"
- <ins>data</ins>: (Varies by {gamemode})<br>
    - For "all" gamemode:<br>
        - "TRNRating", "Score", "Top1", "Top3", "Top5", "Top6", "Top10", "Top12", "Top25", "KD", "WinRatio", "Matches", "Kills", "MinutesPlayed", "KPM", "KPG", "AvgTimePlayed", "ScorePerMatch", "ScorePerMin"
    - For "solo", "duos", "trios", "squads", "ltm" gamemodes: <br>
        - "Score", "Top1", "KD", "WinRatio", "Matches", "Kills", "MinutesPlayed", "KPM", "KPG", "AvgTimePlayed", "ScorePerMatch", "ScorePerMin", "Top3_5_10", "TRNRating"<br>

- <ins>option</ins>: (varies by {data})<br>
    *DATA*: "KD", "WinRatio", "MinutesPlayed", "KPM", "KPG", "AvgTimePlayed", "ScorePerMin"<br>
    *VALUE*:  "value", "percentile", "displayValue"<br>

    *DATA*: "Score", "Top1", "Top3", "Top6", "Top10", "Top12", "Top25", "Matches", "Kills", "ScorePerMatch"<br>
    *VALUE*:  "value", "percentile", "rank", "displayValue"<br>

    *DATA*: "TRNRating"<br>
    *VALUE*:  "value", "percentile", "rank", "displayValue", "displayRank"<br>
    **Example:** get_player_stats(profile_data, category="all", ranked=True, platform="all", season=None, gamemode="all", data="KD", option="value")




## get_player_info()
This function will return info about the player
**Parameters:**
- <ins>profile_data</ins>: The Json data of the player's profile
- <ins>category</ins>:
    - "platformInfo", "userInfo", "metadata"
- <ins>data</ins>:
    - None (default), I'll leave the rest up to you. Get the JSON data using get_player_data() and figure out what information you're looking for, then use the correct values for data and value here. :)
- <ins>value</in>:
    - None (default)
**Returns:** JSON data of the given player
**Example**: player_info = get_player_info(profile_data, category="platformInfo", data="platformUserId")

# **Installation**
Note: Requires Selenium (pip install selenium)
1. Clone this repository into your project
2. Add the inclusion to the file you are working on:    from FortniteStat include *
