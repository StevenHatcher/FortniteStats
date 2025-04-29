from selenium import webdriver # Since the tracker site has protection against bots, we get around this by using selenium instead of requests.
from selenium.webdriver.chrome.options import Options
import re
import json # Used to get the json data from the tracker website and extract info
import time

def get_player_data(username=None, maximize=False, auto_close=False, open_time=0):
    if not username: 
        print("Invalid username")
        return None
    
    url = f"https://fortnitetracker.com/profile/all/{username}" # get the url for the stattracker website

    chrome_options = Options()
    # chrome_options.add_argument("--start-minimized")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # less detection
    
    driver = webdriver.Chrome(options=chrome_options) # Chrome isntance to scrape the data (Can't just use requests - Get status code 403 even with headers)
    if not maximize:
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
            return None

        profile_raw = profile_json_text.group(1) 
        profile_raw = profile_raw.replace("undefined", "null")  # Fix invalid JS if necessary
        profile_data = json.loads(profile_raw)

        return profile_data # return all of the profile data
     
    except Exception as e: # throw an error if there's a problem with the webpage
        print(f"Error: {e}")
        return None

    finally:
        time.sleep(open_time)  # optional: extra wait for full JavaScript rendering
        if auto_close is True:
            driver.quit() # close the webbrowser instance

# Function to get data about the user, such as ID, etc.
def get_player_info(profile_data, category=None, data=None, value=None):    
    if not profile_data: # If that isn't a valid category, return None
        print(f"No profile data found.")
        return None
    
    category_data = profile_data.get(category, []) #Get the data in the category
    if not category_data: # If that isn't a valid category, return None
        print(f"No category '{category}' found.")
        return None
    
    if data is None: return category_data # If no data parameter is given, return the whole category.
    category_values = category_data.get(data) #get the data section of the chosen category
    
    if not category_values: # If that isn't a valid category, return None
        print(f"No category value '{value}' found.")
        return None
    
    if value is None: return category_values # If no data parameter is given, return the whole category.
    
    return category_values[value] #return the value chosen.

# Function to return the value of a specific stat given the platform, gamemode, stat, and option of that stat
def get_player_stats(profile_data, category="stats", ranked=False,platform=None, season=None, gamemode=None, data=None, option=None):
    if not profile_data: return None
   # If you want to get only the stats for the user's preferred platform, use preferred for the platform parameter in the funtcion call
    if platform == "preferred":
        platform = profile_data["metadata"]["preferredInputId"]
    
    if season == "current":
            season = profile_data["metadata"]["currentSeasonInfo"]["id"]
    
    stats_list = profile_data.get(category, [])  # get the stats section of the player profile

    # Find the correct platform section
    target_section = None
    for section in stats_list: # the sections in the stats lists are divided by platform, so we iterate and check each one for the value in the platform parameter
        if section.get("platform") == platform and section.get("season") == season and section.get("isCompetitive") == ranked:
            target_section = section # if the current section is the section of the platform we're looking for, we're done looking
            break
    
    # If there aren't any sections for the given platform, print a message saying so and return
    if not target_section: 
        print(f"No stats found for platform = {platform}, season = {season}, isCompetitive? = {ranked}")
        return None



    stats_block = target_section.get("stats") # get the stats section of the platform section we got previously
    if not stats_block: # If that given platform doesn't have a stat block, return
        print(f"No stats block found for platform = {platform}")
        return None
    if gamemode is None: return stats_block # If no gamemode is given, return the full stats block for the given platform


    # If a gamemode was given in function call, get the stats for that gamemode
    mode_stats = stats_block.get(gamemode) 
    if not mode_stats:
        print(f"No gamemode '{gamemode}' found for platform = {platform}")
        return None

    # If no stat is given, return the full gamemode stats
    if data is None: return mode_stats 
    for stats in mode_stats:            #otherwise, loop through the stat sections until we either find the intended stat or not
        if stats["metadata"]["key"] == data:
            if option is not None:      # If the user didnt give an option for the stat (e.g. value, percentile, etc.), return all of that stat's data
                return stats[option]
            else: return stats

    return None
