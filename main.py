from selenium import webdriver # Since the tracker site has protection against bots, we get around this by using selenium instead of requests.
from selenium.webdriver.chrome.options import Options
import re
import json # Used to get the json data from the tracker website and extract info
import time

# good for solo, duo, trio, squads, but not "all"
stat_metadata_keys = ["TRNRating", "Score", "Top1", "Top3", "Top5", "Top6", "Top10", "Top12", "Top25", "KD", "WinRatio", "Matches", "Kills", "MinutesPlayed", "KPM", "KPG", "AvgTimePlayed", "ScorePerMatch", "ScorePerMin"]
stat_metadata_keys_all = ["Score", "Top1", "KD", "WinRatio", "Matches", "Kills", "MinutesPlayed", "KPM", "KPG", "AvgTimePlayed", "ScorePerMatch", "ScorePerMin", "Top3_5_10", "TRNRating"]



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
        get_specific_stat_value(profile_data, platform=None, gamemode="all", stat="KD", option="value")
     
    except Exception as e: # throw an error if there's a problem with the webpage
        print(f"Error: {e}")
        return 0, 0

    finally:
        driver.quit()

# Function to return the value of a specific stat given the platform, gamemode, stat, and ********option of that stat
def get_player_stat(profile_data, platform, gamemode, stat, option):

    platform_section = None
    if platform == "all":
        platform = None
    if gamemode == "all":
        gamemode = None
        
    # find the section of the profile data that has the chosen platform as the correct platform
    for section in profile_data["stats"]:
        if section.get("platform") == platform or platform is None:
            platform_section = section
    # if theres no section with the chosen platform, return
    if not platform_section:
            print("Invalid platform input")
            return
            
    if gamemode in platform_section["stats"]:
        player_stats = platform_section["stats"][gamemode]
    else:
        print(f"{gamemode} not found!")
        player_stats = []
        
    for stat in player_stats:
        key = stat["metadata"]["key"]
        if key == stat:
            print("Stat_value: {stat[option]}")
            return stat[option]
             

    # print(f"returned platform_section: {platform_section}")
    return

def get_specific_stat_value(profile_data, platform, gamemode, stat, option):
    """
    Search the profile JSON for a given platform ("kbm", "gamepad", etc.) and gamemode ("solo", "duos", etc.).
    If platform_type is None, it searches where "platform": null.
    """
    stats_list = profile_data.get("stats", [])

    # Find the correct platform section
    target_section = None
    for section in stats_list:
        if section.get("platform") == platform:
            target_section = section
            break

    if not target_section:
        print(f"No stats found for platform = {platform}")
        return None

    # Now find the correct gamemode stats
    stats_block = target_section.get("stats")
    if not stats_block:
        print(f"No stats block found for platform = {platform}")
        return None

    mode_stats = stats_block.get(gamemode)
    if not mode_stats:
        print(f"No gamemode '{gamemode}' found for platform = {platform}")
        return None

    

    for stats in mode_stats:
        if stats["metadata"]["key"] == stat:
            stat_value = stats[option]
            break  # Stop looping after finding it

    if stat_value is not None:
        print(f"Stat Found: {stat_value}")
    else:
        print("stat not found in mode stats.")
    
    
    return stat_value  # This will be a list of stats!


def get_gamemode_stats(profile_data, platform, gamemode):
    """
    Search the profile JSON for a given platform ("kbm", "gamepad", etc.) and gamemode ("solo", "duos", etc.).
    If platform_type is None, it searches where "platform": null.
    """
    stats_list = profile_data.get("stats", [])

    # Find the correct platform section
    target_section = None
    for section in stats_list:
        if section.get("platform") == platform:
            target_section = section
            break

    if not target_section:
        print(f"No stats found for platform = {platform}")
        return None

    # Now find the correct gamemode stats
    stats_block = target_section.get("stats")
    if not stats_block:
        print(f"No stats block found for platform = {platform}")
        return None

    mode_stats = stats_block.get(gamemode)
    if not mode_stats:
        print(f"No gamemode '{gamemode}' found for platform = {platform}")
        return None

    print(f"Mode stats: {mode_stats}")
    return mode_stats  # This will be a list of stats!



def get_platform_stats():
    return

def get_gamemode_stats():
    return
# platform: None for all, "touch", "kbm", "gamepad"
# gamemode: "all", "duos", "squads", "trios", "solo", "ltm"
# stat options up there in meta keys

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