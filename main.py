from selenium import webdriver # Since the tracker site has protection against bots, we get around this by using selenium instead of requests.
from selenium.webdriver.chrome.options import Options
import re
import json # Used to get the json data from the tracker website and extract info
import time





def get_player_data(username):
    url = f"https://fortnitetracker.com/profile/all/{username}" # get the url for the stattracker website

    chrome_options = Options()
    # chrome_options.add_argument("--start-minimized")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # less detection
    
    driver = webdriver.Chrome(options=chrome_options) # Chrome isntance to scrape the data (Can't just use requests - Get status code 403 even with headers)
    driver.minimize_window() # Can't scrape it in headerless, so just minimize the window when it opens lol

    try:
        driver.get(url)

        time.sleep(2)  # optional: extra wait for full JavaScript rendering

        # Once fully loaded, get page source
        html = driver.page_source
       
        # Get the section of the json from the page that contains the player's data. It's titled "Profile"
        profile_json_text = re.search(r'const profile = ({.*?});', html, re.DOTALL)

        if not profile_json_text: # if the profile can't be found in the json, print an error and return default 0,0
            print("Could not find profile JSON in page.")
            return 

        profile_raw = profile_json_text.group(1) 
        profile_raw = profile_raw.replace("undefined", "null")  # Fix invalid JS if necessary
        profile_data = json.loads(profile_raw)

        # get_player_stat(profile_data, "all", "all", "KD", "Value")
        # get_gamemode_stats(profile_data, platform=None, gamemode="all")
        chosen_stats = get_player_stats(profile_data, category="stats", platform="preferred", gamemode="all", stat="lol", option=None)
        print(chosen_stats)
     
    except Exception as e: # throw an error if there's a problem with the webpage
        print(f"Error: {e}")
        return 0, 0

    finally:
        driver.quit()

# Function to get data about the user, such as ID, etc.
#category: platformInfo, userInfo, metadata
def get_player_info(profile_data, category=None,):
    return


# Function to return the value of a specific stat given the platform, gamemode, stat, and option of that stat
def get_player_stats(profile_data, category="stats", ranked=False,platform=None, season=None, gamemode=None, stat=None, option=None):
    
   # If you want to get only the stats for the user's preferred platform, use preferred for the platform parameter in the funtcion call
    if platform == "preferred":
        platform = profile_data["metadata"]["preferredInputId"]
    
    stats_list = profile_data.get(category, [])  # get the stats section of the player profile

    # Find the correct platform section
    target_section = None
    for section in stats_list: # the sections in the stats lists are divided by platform, so we iterate and check each one for the value in the platform parameter
        if section.get("platform") == platform and section.get("season") == season and section.get("isCompetitive") == ranked:
            target_section = section # if the current section is the section of the platform we're looking for, we're done looking
            break

    if not target_section: # If there aren't any sections for the fiven platform, print a message saying so and retunr
        print(f"No stats found for platform = {platform}")
        return None



    stats_block = target_section.get("stats") # get the stats section of the platform section we got previously
    if not stats_block: # If that given platform doesn't have a stat block, return
        print(f"No stats block found for platform = {platform}")
        return None
    if gamemode is None: return stats_block # If no gamemode is given, return the full stats block for the given platform



    mode_stats = stats_block.get(gamemode) # If a gamemode was given in function call, get the stats for that gamemode
    if not mode_stats:
        print(f"No gamemode '{gamemode}' found for platform = {platform}")
        return None



    if stat is None: return mode_stats # If no stat is given, return the full gamemode stats
    for stats in mode_stats:            #otherwise, loop through the stat sections until we either find the intended stat or not
        if stats["metadata"]["key"] == stat:
            if option is not None:      # If the user didnt give an option for the stat (e.g. value, percentile, etc.), return all of that stat's data
                return stats[option]
            else: return stats

    return


# Category: stats (default), last7DaysStats, last30DaysStats

# platform: None "all", "touch", "kbm", "gamepad", "preferred"
# gamemode: "all", "solo", "duos", "trios", "squads", "ltm"

# Stats:
# For "all" gamemode: 
#   "TRNRating", "Score", "Top1", "Top3", "Top5", "Top6", "Top10", "Top12", "Top25", "KD", "WinRatio", "Matches", "Kills", "MinutesPlayed", "KPM", "KPG", "AvgTimePlayed", "ScorePerMatch", "ScorePerMin"
# For "solo", "duos", "trios", "squads", "ltm" gamemodes:
#   "Score", "Top1", "KD", "WinRatio", "Matches", "Kills", "MinutesPlayed", "KPM", "KPG", "AvgTimePlayed", "ScorePerMatch", "ScorePerMin", "Top3_5_10", "TRNRating"

# OPTIONS FOR STATS BASED ON GAMEMODE AND STAT.

# STAT: KD, WinRatio, MinutesPlayed, KPM, KPG, AvgTimePlayed, ScorePerMin
# VALUE:  value, percentile, displayValue

# STAT: Score, Top1, Top3, Top6, Top10, Top12, Top25, Matches, Kills, ScorePerMatch
# VALUE:  value, percentile, rank, displayValue

# STAT: TRNRating, 
# VALUE:  value, percentile, rank, displayValue, displayRank

#-------------------------------------FOR "ALL"-------------------------------------#
# STAT: Top3_5_10, Top6_12_25 
# VALUE:  value, displayValue

# STAT: MinutesPlayed, KPM, KPG, AvgTimePlayed, ScorePerMatch, ScorePerMin
# VALUE:  value, percentile, displayValue
 
# STAT: Score, Top1, KD, WinRatio, Matches, Kills, MinutesPlayed, 
# VALUE:  value, percentile, rank, displayValue

# STAT: TRNRating
# VALUE:  value, percentile, rank, displayValue, displayRank

get_player_data("stillsheisty")