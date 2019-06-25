#%% Import Statements
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.static import players
import pandas as pd

ALL_STAR_STATS_INDEX = 4
REG_STATS_INDEX = 0


# %%
def get_all_star(id_number):
    player_career = playercareerstats.PlayerCareerStats(player_id=id_number).get_data_frames()
    all_star_seasons = player_career[ALL_STAR_STATS_INDEX]
    reg_seasons = player_career[REG_STATS_INDEX]
    is_all_star = pd.Series([])

    for i in range(len(reg_seasons)):
        year = reg_seasons["SEASON_ID"].iloc[i]

        if year in all_star_seasons["SEASON_ID"]:
            is_all_star = is_all_star.append(pd.Series([True]), ignore_index=True)
        else:
            is_all_star = is_all_star.append(pd.Series([False]), ignore_index=True)

    return is_all_star


def eliminate_duplicate_seasons(seasons):
    to_remove = []

    for i in range(len(seasons)):

        if (seasons["SEASON_ID"].iloc[i] == seasons["SEASON_ID"].iloc[i-1]) \
                and (seasons["PLAYER_ID"].iloc[i] == seasons["PLAYER_ID"].iloc[i-1]):
            to_remove.append(i-1)

    print(to_remove)

    seasons.drop(seasons.index[to_remove], axis=0, inplace=True)


#%%
pd.set_option('display.max_columns', 30)
#
# print(players.find_players_by_first_name('lebron'))
# player = players.find_players_by_first_name('lebron')
# career_stats = playercareerstats.PlayerCareerStats(player_id=2544).get_data_frames()
# career_stats = pd.DataFrame(data=career_stats)
#
# career_stats = career_stats[0][0]
# career_stats = pd.DataFrame(data=career_stats)
career_stats = pd.DataFrame()


#%%
active_players = pd.DataFrame(data=players.get_active_players())
player_ids = active_players['id']
print(player_ids.iloc[0])

#%%
for i in range(0,10):
    player_id = player_ids.iloc[i]
    stats = playercareerstats.PlayerCareerStats(player_id=player_id).get_data_frames()
    stats = pd.DataFrame(data=stats)
    stats = pd.DataFrame(data=stats[0][0])
    all_star_column = get_all_star(player_id)
    stats["ALL_STAR"] = all_star_column
    career_stats = career_stats.append(stats, ignore_index=True)

#%%
eliminate_duplicate_seasons(career_stats)
print(career_stats)
