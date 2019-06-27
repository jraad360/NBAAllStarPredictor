#%% This python script is used to store all the 20,000+ seasons in NBA history in a CSV file to train the model.
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.static import players
import pandas as pd
import time

import urllib3.exceptions
from urllib3.exceptions import ReadTimeoutError


ALL_STAR_STATS_INDEX = 4
REG_STATS_INDEX = 0
FILE_NAME = "all_player_stats.csv"


#%% Returns a Series of booleans indicating whether or not a season resulted in an All-Star selection
def get_all_star(id_number):
    player_career = playercareerstats.PlayerCareerStats(player_id=id_number).get_data_frames()
    all_star_seasons = player_career[ALL_STAR_STATS_INDEX]
    reg_seasons = player_career[REG_STATS_INDEX]
    is_all_star = pd.Series([])

    for i in range(len(reg_seasons)):
        year = reg_seasons["SEASON_ID"].iloc[i]

        if all_star_seasons["SEASON_ID"].str.contains(year).any():
            is_all_star = is_all_star.append(pd.Series([True]), ignore_index=True)
        else:
            is_all_star = is_all_star.append(pd.Series([False]), ignore_index=True)

    return is_all_star


#%% Eliminates partial seasons that result from trades, leaving only the total season stats
# Assumes that an individual player's seasons are in order
def eliminate_duplicate_seasons(seasons):
    to_remove = []

    for i in range(len(seasons)):

        if (seasons["SEASON_ID"].iloc[i] == seasons["SEASON_ID"].iloc[i-1]) \
                and (seasons["PLAYER_ID"].iloc[i] == seasons["PLAYER_ID"].iloc[i-1]):
            to_remove.append(i-1)

    print(to_remove)

    seasons.drop(seasons.index[to_remove], axis=0, inplace=True)


#%% Returns a DataFrame containing all the stats of the indicated number of players, including an All-Star column
def get_seasons(number_of_players, randomize=True, historical_players=True):

    # initialize career_stats DataFrame
    career_stats = pd.DataFrame()

    # fetch players and id's
    if historical_players:
        nba_players = pd.DataFrame(data=players.get_players())
    else:
        nba_players = pd.DataFrame(data=players.get_active_players())

    player_ids = nba_players['id']

    if randomize:
        player_ids = player_ids.sample(frac=1).reset_index(drop=True)

    # troubleshooting all star column with LeBron James's stats
    # player_ids[0] = 2544

    # if negative number or too many players are requested, give them all
    if number_of_players < 0 or number_of_players > len(player_ids):
        number_of_players = len(player_ids)

    # Keeping track of counter independently of a for-loop to handle timeouts
    count = 0

    while count < number_of_players:
        try:
            player_id = player_ids.iloc[count]
            stats = playercareerstats.PlayerCareerStats(player_id=player_id).get_data_frames()
            stats = pd.DataFrame(data=stats)
            stats = pd.DataFrame(data=stats[0][0])
            all_star_column = get_all_star(player_id)
            stats["ALL_STAR"] = all_star_column
            career_stats = career_stats.append(stats, ignore_index=True)
            if (count + 1) % 10 == 0:
                print("Finished with player #", count + 1)
            count += 1
        except Exception:
            wait_time = 120
            printf("Caught timeout! Waiting %i seconds...", wait_time)
            start = time.time()
            end = time.time()
            while end - start < wait_time:
                end = time.time()

    # career_stats.drop(["PLAYER_ID", "TEAM_ID"], axis=1)
    career_stats.to_csv(path_or_buf=FILE_NAME, index=False)
    return career_stats


#%% Update CSV File
no_of_players = -1
get_seasons(no_of_players, randomize=True)
