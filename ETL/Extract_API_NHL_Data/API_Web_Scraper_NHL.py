import random
from time import sleep
from typing import Any, Dict, List, Union

import pandas as pd
import requests
from bs4 import BeautifulSoup

pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)

import os
import sys

# Get the current working directory (the directory of the running script)
current_dir = os.getcwd()

import warnings

warnings.filterwarnings("ignore")


###########################################################################################################################################
# NEW CODE BLOCK - Get season list from API - NHL API
###########################################################################################################################################


def nhl_season_data() -> Union[Dict[str, Any], List[Any]]:
    """
    Fetches the NHL season data from the NHL API.

    Returns:
        Union[Dict[str, Any], List[Any]]: The JSON response from the API containing the season list.
    """
    url = "https://api-web.nhle.com/v1/season"
    response = requests.get(url)
    data = response.json()
    seasons_list = data

    return seasons_list


###########################################################################################################################################
# NEW CODE BLOCK - Get regular season stats per team - NHL API
###########################################################################################################################################


def nhl_regular_season_data(
    seasons_list: Union[Dict[str, Any], List[Any]]
) -> pd.DataFrame:
    """
    Fetches regular season statistics per team for each season provided via the NHL API.

    Args:
        seasons_list (Union[Dict[str, Any], List[Any]]): A list or dictionary of seasons (as returned by nhl_season_data).

    Returns:
        pd.DataFrame: A concatenated DataFrame containing the regular season stats for all teams.
    """
    list_of_data_frames = []
    for season in seasons_list:
        url = f"https://api.nhle.com/stats/rest/en/team/summary?sort=shotsForPerGame&cayenneExp=seasonId={season}%20and%20gameTypeId=2"
        response = requests.get(url)
        data = response.json()
        data = data["data"]
        df = pd.DataFrame(data)
        list_of_data_frames.append(df)
    df = pd.concat(list_of_data_frames)
    df["gameType"] = "Regular Season"

    return df


###########################################################################################################################################
# NEW CODE BLOCK - Get playoff stats per team - NHL API
###########################################################################################################################################


def nhl_playoff_data(seasons_list: Union[Dict[str, Any], List[Any]]) -> pd.DataFrame:
    """
    Fetches playoff statistics per team for each season provided via the NHL API.

    Args:
        seasons_list (Union[Dict[str, Any], List[Any]]): A list or dictionary of seasons (as returned by nhl_season_data).

    Returns:
        pd.DataFrame: A concatenated DataFrame containing the playoff stats for all teams.
    """
    list_of_data_frames = []
    for season in seasons_list:
        url = f"https://api.nhle.com/stats/rest/en/team/summary?sort=shotsForPerGame&cayenneExp=seasonId={season}%20and%20gameTypeId=3"
        response = requests.get(url)
        data = response.json()
        data = data["data"]
        df = pd.DataFrame(data)
        list_of_data_frames.append(df)
    df = pd.concat(list_of_data_frames)
    df["gameType"] = "Playoffs"

    return df


###########################################################################################################################################
# NEW CODE BLOCK - Get regular season stats per team - naturalstatrick.com
###########################################################################################################################################


def natural_statrick_regular_season_data() -> pd.DataFrame:
    """
    Scrapes regular season team statistics from naturalstattrick.com for seasons 2007 to 2023.
    Saves the resulting DataFrame as "Regular_Season_Data.csv".

    Returns:
        pd.DataFrame: A DataFrame containing the scraped regular season stats.
    """
    df_list = []
    for season in range(2007, 2025):  # Manually set the years
        game_type = 2
        url = f"https://www.naturalstattrick.com/teamtable.php?fromseason={str(season)+str(season+1)}&thruseason={str(season)+str(season+1)}&stype={game_type}&sit=5v5&score=all&rate=n&team=all&loc=B&gpf=410&fd=&td="

        req = requests.get(url)
        print("status code: " + str(req.status_code))
        print("scraping regular season: " + str(season) + str(season + 1))

        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find("table", id="teams")

        # Extract headers from table; if header text is empty, a default column name is assigned
        headers = [
            th.get_text().strip() if th.get_text().strip() else f"Column_{i}"
            for i, th in enumerate(table.find("thead").find_all("th"))
        ]

        # Extract rows from table body.
        rows = []
        for row in table.find("tbody").find_all("tr"):
            cells = [cell.get_text().strip() for cell in row.find_all("td")]
            rows.append(cells)

        # Flatten the rows list and regroup by the number of columns expected (72)
        rows = rows[0]
        table_data = [rows[i : i + 72] for i in range(0, len(rows), 72)]

        df = pd.DataFrame(table_data, columns=headers)
        df["Season"] = str(season) + str(season + 1)
        df["GameType"] = "Regular Season"
        df = df.drop(
            ["OTL", "Point %", "Points", "ROW", "Column_0"], axis=1, errors="ignore"
        )
        df_list.append(df)

        sleep(random.uniform(30, 60))

    df = pd.concat(df_list, axis=0)

    return df


###########################################################################################################################################
# NEW CODE BLOCK - Get playoff stats per team - naturalstatrick.com
###########################################################################################################################################


def natural_statrick_playoff_data() -> pd.DataFrame:
    """
    Scrapes playoff team statistics from naturalstattrick.com for seasons 2007 to 2023.
    Saves the resulting DataFrame as "Playoffs_Data.csv".

    Returns:
        pd.DataFrame: A DataFrame containing the scraped playoff stats.
    """
    df_list = []
    for season in range(2007, 2024):  # Manually set the years
        game_type = 3
        url = f"https://www.naturalstattrick.com/teamtable.php?fromseason={str(season)+str(season+1)}&thruseason={str(season)+str(season+1)}&stype={game_type}&sit=5v5&score=all&rate=n&team=all&loc=B&gpf=410&fd=&td="

        req = requests.get(url)
        print("status code: " + str(req.status_code))
        print("scraping playoff season: " + str(season) + str(season + 1))

        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find("table", id="teams")

        # Extract headers from table; if header text is empty, a default column name is assigned
        headers = [
            th.get_text().strip() if th.get_text().strip() else f"Column_{i}"
            for i, th in enumerate(table.find("thead").find_all("th"))
        ]

        # Extract rows from table body.
        rows = []
        for row in table.find("tbody").find_all("tr"):
            cells = [cell.get_text().strip() for cell in row.find_all("td")]
            rows.append(cells)

        # Flatten the rows list and regroup by the expected number of columns (68)
        rows = rows[0]
        table_data = [rows[i : i + 68] for i in range(0, len(rows), 68)]

        df = pd.DataFrame(table_data, columns=headers)
        df["Season"] = str(season) + str(season + 1)
        df["GameType"] = "Playoffs"
        df = df.drop(
            ["OTL", "Point %", "Points", "ROW", "Column_0"], axis=1, errors="ignore"
        )
        df_list.append(df)

        sleep(random.uniform(30, 60))

    df = pd.concat(df_list, axis=0)

    return df


###########################################################################################################################################
# NEW CODE BLOCK - Run all functions to get season stats from 1983 to 2021 and playoff teams
###########################################################################################################################################


def extract() -> None:
    """
    Executes the entire data extraction and merging process:
      - Retrieves season list from NHL API.
      - Fetches regular season and playoff stats per team via the NHL API.
      - Scrapes regular season and playoff stats per team from naturalstattrick.com.
      - Merges both data sources and saves the final dataset as a CSV file.

    Returns:
        None
    """
    # Get all season data from NHL API
    seasons_list = nhl_season_data()

    # Retrieve regular season stats per team from NHL API
    regular_season_data = nhl_regular_season_data(seasons_list=seasons_list)

    # Retrieve playoff stats per team from NHL API.
    playoff_data = nhl_playoff_data(seasons_list=seasons_list)

    # Combine regular season and playoff stats from NHL API
    full_data_api = pd.concat([regular_season_data, playoff_data]).reset_index(
        drop=True
    )

    # Rename columns for consistency in the NHL API dataset
    renamed_columns_api = {
        "faceoffWinPct": "faceoff_win_pct",
        "gamesPlayed": "games_played",
        "goalsAgainst": "goals_against",
        "goalsAgainstPerGame": "goals_against_per_game",
        "goalsFor": "goals_for",
        "goalsForPerGame": "goals_for_per_game",
        "losses": "losses",
        "otLosses": "overtime_losses",
        "penaltyKillNetPct": "penalty_kill_net_pct",
        "penaltyKillPct": "penalty_kill_pct",
        "pointPct": "points_pct",
        "points": "points",
        "powerPlayNetPct": "power_play_net_pct",
        "powerPlayPct": "power_play_pct",
        "regulationAndOtWins": "regulation_and_overtime_wins",
        "seasonId": "season_id",
        "shotsAgainstPerGame": "shots_against_per_game",
        "shotsForPerGame": "shots_for_per_game",
        "teamFullName": "team_full_name",
        "teamId": "team_id",
        "ties": "ties",
        "wins": "wins",
        "winsInRegulation": "wins_in_regulation",
        "winsInShootout": "wins_in_shootout",
        "gameType": "game_type",
    }
    full_data_api = full_data_api.rename(columns=renamed_columns_api)
    full_data_api.to_csv("full_data_api.csv", index=False)

    # Retrieve naturalstattrick.com regular season stats per team
    regular_season_data_nst = natural_statrick_regular_season_data()

    # Retrieve naturalstattrick.com playoff stats per team
    playoffs_data_nst = natural_statrick_playoff_data()

    # Combine naturalstattrick.com regular season and playoff stats
    full_data_nst = pd.concat([regular_season_data_nst, playoffs_data_nst], axis=0)

    # Rename columns for consistency in the naturalstattrick dataset
    renamed_columns_nst = {
        "Team": "team",
        "GP": "games_played",
        "TOI": "time_on_ice",
        "W": "wins",
        "L": "losses",
        "CF": "corsi_for",
        "CA": "corsi_against",
        "CF%": "corsi_for_pct",
        "FF": "fenwick_for",
        "FA": "fenwick_against",
        "FF%": "fenwick_for_pct",
        "SF": "shots_for",
        "SA": "shots_against",
        "SF%": "shots_for_pct",
        "GF": "goals_for",
        "GA": "goals_against",
        "GF%": "goals_for_pct",
        "xGF": "expected_goals_for",
        "xGA": "expected_goals_against",
        "xGF%": "expected_goals_for_pct",
        "SCF": "scoring_chances_for",
        "SCA": "scoring_chances_against",
        "SCF%": "scoring_chances_for_pct",
        "SCSF": "scoring_chances_shots_for",
        "SCSA": "scoring_chances_shots_against",
        "SCSF%": "scoring_chances_shots_for_pct",
        "SCGF": "scoring_chances_goals_for",
        "SCGA": "scoring_chances_goals_against",
        "SCGF%": "scoring_chances_goals_for_pct",
        "SCSH%": "scoring_chances_shooting_pct",
        "SCSV%": "scoring_chances_save_pct",
        "HDCF": "high_danger_chances_for",
        "HDCA": "high_danger_chances_against",
        "HDCF%": "high_danger_chances_for_pct",
        "HDSF": "high_danger_shots_for",
        "HDSA": "high_danger_shots_against",
        "HDSF%": "high_danger_shots_for_pct",
        "HDGF": "high_danger_goals_for",
        "HDGA": "high_danger_goals_against",
        "HDGF%": "high_danger_goals_for_pct",
        "HDSH%": "high_danger_shooting_pct",
        "HDSV%": "high_danger_save_pct",
        "MDCF": "medium_danger_chances_for",
        "MDCA": "medium_danger_chances_against",
        "MDCF%": "medium_danger_chances_for_pct",
        "MDSF": "medium_danger_shots_for",
        "MDSA": "medium_danger_shots_against",
        "MDSF%": "medium_danger_shots_for_pct",
        "MDGF": "medium_danger_goals_for",
        "MDGA": "medium_danger_goals_against",
        "MDGF%": "medium_danger_goals_for_pct",
        "MDSH%": "medium_danger_shooting_pct",
        "MDSV%": "medium_danger_save_pct",
        "LDCF": "low_danger_chances_for",
        "LDCA": "low_danger_chances_against",
        "LDCF%": "low_danger_chances_for_pct",
        "LDSF": "low_danger_shots_for",
        "LDSA": "low_danger_shots_against",
        "LDSF%": "low_danger_shots_for_pct",
        "LDGF": "low_danger_goals_for",
        "LDGA": "low_danger_goals_against",
        "LDGF%": "low_danger_goals_for_pct",
        "LDSH%": "low_danger_shooting_pct",
        "LDSV%": "low_danger_save_pct",
        "SH%": "shooting_pct",
        "SV%": "save_pct",
        "PDO": "pdo_rating",
        "Season": "season",
        "GameType": "game_type",
    }
    full_data_nst = full_data_nst.rename(columns=renamed_columns_nst)
    full_data_nst.to_csv("full_data_nst.csv", index=False)

    # Clean and convert naturalstattrick percentage columns
    for col in full_data_nst.columns:
        if col.endswith("_pct"):
            if full_data_nst[col].dtype not in ["float64", "float32"]:
                full_data_nst[col] = full_data_nst[col].astype(str)
                full_data_nst[col] = full_data_nst[col].str.replace(
                    "-", "0", regex=False
                )
                full_data_nst[col] = full_data_nst[col].astype(float)
                full_data_nst[col] = full_data_nst[col] / 100
        else:
            None

    # Clean and align merge keys
    full_data_api["team_full_name"] = full_data_api["team_full_name"].str.replace(
        "é", "e"
    )
    full_data_api["team_full_name"] = full_data_api["team_full_name"].str.replace(
        ".", ""
    )
    full_data_nst["team"] = full_data_nst["team"].str.replace("é", "e")
    full_data_nst["team"] = full_data_nst["team"].str.replace(".", "")
    full_data_api["season_id"] = full_data_api["season_id"].astype(str)
    full_data_nst["season"] = full_data_nst["season"].astype(str)

    # Merge the NHL API data and naturalstattrick data on matching team, season, and game type
    full_data = full_data_api.merge(
        full_data_nst,
        how="left",
        left_on=["team_full_name", "season_id", "game_type"],
        right_on=["team", "season", "game_type"],
    )

    # Drop unnecessary columns.
    full_data = full_data.drop(["team", "season"], axis=1, errors="ignore")
    # Drop duplicate columns ending with '_y' and remove the '_x' suffix from the remaining columns
    full_data = full_data.drop(
        columns=[col for col in full_data.columns if col.endswith("_y")]
    )
    full_data.columns = [
        col[:-2] if col.endswith("_x") else col for col in full_data.columns
    ]

    # Save the final merged data as a CSV file
    full_data.to_csv(
        os.path.abspath(
            os.path.join(current_dir, "..", "..", r"NHL_ML_Analysis/NHL_Data.csv")
        ),
        index=False,
    )

    return None


if __name__ == "__main__":
    extract()
