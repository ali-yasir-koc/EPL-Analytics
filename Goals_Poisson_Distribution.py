# Import Library and Settings
import pandas as pd
from scipy.stats import poisson

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 100)
pd.set_option('display.width', 500)
pd.set_option('display.float_format', lambda x: '%.4f' % x)

# 23-24 Season
season_23_24 = pd.read_csv("data/2023-2024.csv")
season_23_24.shape
season_23_24.head()
season_23_24 = season_23_24[["home_team_name", "away_team_name", "home_team_goals", "away_team_goals"]]
season_23_24.columns = ["Team", "Opponent", "GF", "GA"]

season_23_24["GF"].sum()
season_23_24["GA"].sum()

season_23_24["Total"] = season_23_24["GF"] + season_23_24["GA"]

# 22-23 Season
season_22_23 = pd.read_csv("data/2022-2023.csv")
season_22_23 = season_22_23[["Home Team", "Away Team", "Goals Home", "Away Goals"]]
season_22_23.columns = ["Team", "Opponent", "GF", "GA"]
season_22_23.head()

season_22_23["GF"].sum()
season_22_23["GA"].sum()
season_22_23["Total"] = season_22_23["GF"] + season_22_23["GA"]

# 21-22 Season
season_21_22 = pd.read_csv("data/2021-2022.csv")
season_21_22.shape
season_21_22 = season_21_22[["HomeTeam", "AwayTeam", "FTHG", "FTAG"]]
season_21_22.columns = ["Team", "Opponent", "GF", "GA"]
season_21_22.head()

season_21_22["GF"].sum()
season_21_22["GA"].sum()
season_21_22["Total"] = season_21_22["GF"] + season_21_22["GA"]

# 20-21 Season
season_20_21 = pd.read_excel("data/2020-2021.xlsx")
season_20_21.head()
season_20_21.info()
season_20_21.shape
season_20_21 = season_20_21[["HomeTeam", "AwayTeam", "FTHG", "FTAG"]]
season_20_21.columns = ["Team", "Opponent", "GF", "GA"]
season_20_21.head()

season_20_21["GF"].sum()
season_20_21["GA"].sum()
season_20_21["Total"] = season_20_21["GF"] + season_20_21["GA"]

# 19-20 Season
season_19_20 = pd.read_csv("data/2019-2020.csv")
season_19_20.head()
season_19_20.info()
season_19_20.shape

season_19_20['GF'] = season_19_20['Result'].str.split('-').str[0].astype(int)
season_19_20['GA'] = season_19_20['Result'].str.split('-').str[1].astype(int)

season_19_20 = season_19_20[["Home Team", "Away Team", "GF", "GA"]]
season_19_20.columns = ["Team", "Opponent", "GF", "GA"]
season_19_20.head()

season_19_20["GF"].sum()
season_19_20["GA"].sum()
season_19_20["Total"] = season_19_20["GF"] + season_19_20["GA"]

# All Seasons
total_home_goal = season_19_20["GF"].sum() + season_20_21["GF"].sum() + \
                  season_20_21["GF"].sum() + season_22_23["GF"].sum() + season_23_24["GF"].sum()
total_away_goal = season_19_20["GA"].sum() + season_20_21["GA"].sum() + \
                  season_21_22["GA"].sum() + season_22_23["GA"].sum() + season_23_24["GA"].sum()
total_goal = season_19_20["Total"].sum() + season_20_21["Total"].sum() + \
             season_21_22["Total"].sum() + season_22_23["Total"].sum() + season_23_24["Total"].sum()
total_match = 380 * 5

avg_home_goal = total_home_goal / total_match
avg_away_goal = total_away_goal / total_match
avg_goal = total_goal / total_match
print(avg_home_goal)
print(avg_away_goal)
print(avg_goal)

# Distributions
total_goal_dict = {}
for i in range(11):
    prop = poisson.pmf(i, avg_goal)
    total_goal_dict[i] = round(prop * 380)

total_goal_dict["11+"] = 380 - sum(total_goal_dict.values())

all_seasons = pd.concat([season_19_20, season_20_21, season_21_22, season_22_23, season_23_24],
                        ignore_index = True)

all_time_df = all_seasons.groupby("Total")["GF"].count().reset_index()
all_time_df.columns = ["goal_number", "match_number"]
all_time_df.loc[10] = [10, 0]
all_time_df.loc[11] = [11, 0]
all_time_df["expected_match_number"] = [5 * i for i in total_goal_dict.values()]
all_time_df["24_25_expected"] = total_goal_dict.values()

all_time_df.to_csv("data/alltime_graph.csv", index = False)
