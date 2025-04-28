# FortniteStatLibrary
 Access and utilize the statistics of public accounts on fortnitetracker.com


## get_player_data(username=None)
This function returns all of the JSON data of the given player if their account is public
**Parameters:**
- <ins>username</ins> The player's username
**Returns:** JSON data of the given player


## get_player_stats(profile_data, category="stats", ranked=False,platform=None, season=None, gamemode=None, data=None, option=None)
Function to return the value of a specific stat given the platform, gamemode, stat, and option of that stat

**Parameters:**
- <ins>profile_data</ins>: The JSON data of the player
- <ins>category</ins>: "stats" (default), "last7DaysStats", "last30DaysStats"
- <ins>ranked</ins>: True, False (default)
- <ins>platform</ins>: None (default), "all", "touch", "kbm", "gamepad", "preferred" (gives data for player's preferred platform)
- <ins>season</ins>: None, [any number], "current" (gives current season)
- <ins>gamemode</ins>: "all", "solo", "duos", "trios", "squads", "ltm"
- <ins>data</ins>: (Varies by {gamemode})
    - For "all" gamemode: "TRNRating", "Score", "Top1", "Top3", "Top5", "Top6", "Top10", "Top12", "Top25", "KD", "WinRatio", "Matches", "Kills", "MinutesPlayed", "KPM", "KPG", "AvgTimePlayed", "ScorePerMatch", "ScorePerMin"
    - For "solo", "duos", "trios", "squads", "ltm" gamemodes: "Score", "Top1", "KD", "WinRatio", "Matches", "Kills", "MinutesPlayed", "KPM", "KPG", "AvgTimePlayed", "ScorePerMatch", "ScorePerMin", "Top3_5_10", "TRNRating"

- <ins>option</ins>: (varies by {data})
    *STAT*: KD, WinRatio, MinutesPlayed, KPM, KPG, AvgTimePlayed, ScorePerMin
    *VALUE*:  value, percentile, displayValue

    *STAT*: Score, Top1, Top3, Top6, Top10, Top12, Top25, Matches, Kills, ScorePerMatch
    *VALUE*:  value, percentile, rank, displayValue

    *STAT*: TRNRating
    *VALUE*:  value, percentile, rank, displayValue, displayRank