import pandas as pd
import psycopg2 as ps

pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)

import warnings

warnings.filterwarnings("ignore")

import datetime
import os
import re
import shutil
import sys
import time

# Get the current working directory (the directory of the running script)
current_dir = os.getcwd()
# Add the target directory to the system path
sys.path.append(os.path.abspath(os.path.join(current_dir, "SQL_Queries")))
from SQL_Queries import *

sys.path.append(
    os.path.abspath(os.path.join(current_dir, "Create_Cumulative_Data_Model"))
)
from Create_Cumulative_Models import *
from dotenv import load_dotenv

load_dotenv()
DB_PASSWORD = os.getenv("DB_PASSWORD")


###########################################################################################################################################
# NEW CODE BLOCK - Process season and playoff data
###########################################################################################################################################


def process_data() -> pd.DataFrame:
    """
    Transforms the raw NHL season stats data by:
      - Reading the CSV file containing NHL data.
      - Formatting the season and game type columns.
      - Filling missing values with 0.
      - Reordering columns.

    Returns:
        pd.DataFrame: The processed DataFrame containing season and playoff stats.
    """
    # Import NHL team season stats data frame
    path = os.path.abspath(os.path.join(current_dir, "..", "..", "NHL_ML_Analysis"))
    csv_list = []
    for i in os.listdir(path):
        # Select file with "NHL" in the name
        if os.path.isfile(os.path.join(path, i)) and "NHL" in i:
            csv_list.append(i)

    # Convert CSV file to DataFrame (using the first matching file)
    df = pd.read_csv(path + "\\" + str(csv_list[0]))

    # Define a helper function to format season numbers
    def format_number(number: str) -> str:
        return re.sub(r"(\d)(?=(\d{4})+(?!\d))", r"\1/", str(number))

    df["season_id"] = df["season_id"].astype(str)
    df["season"] = df["season_id"].apply(format_number)

    # Map game types to their corresponding IDs
    df["game_type_id"] = df["game_type"].map({"Playoffs": 3, "Regular Season": 2})

    # Fill all NaN values with 0
    df = df.fillna(0)

    # Reorder columns
    df = df[
        [
            "season",
            "season_id",
            "game_type",
            "game_type_id",
            "team_full_name",
            "team_id",
            "faceoff_win_pct",
            "games_played",
            "goals_against",
            "goals_against_per_game",
            "goals_for",
            "goals_for_per_game",
            "losses",
            "overtime_losses",
            "penalty_kill_net_pct",
            "penalty_kill_pct",
            "points_pct",
            "points",
            "power_play_net_pct",
            "power_play_pct",
            "regulation_and_overtime_wins",
            "shots_against_per_game",
            "shots_for_per_game",
            "ties",
            "wins",
            "wins_in_regulation",
            "wins_in_shootout",
            "time_on_ice",
            "corsi_for",
            "corsi_against",
            "corsi_for_pct",
            "fenwick_for",
            "fenwick_against",
            "fenwick_for_pct",
            "shots_for",
            "shots_against",
            "shots_for_pct",
            "goals_for_pct",
            "expected_goals_for",
            "expected_goals_against",
            "expected_goals_for_pct",
            "scoring_chances_for",
            "scoring_chances_against",
            "scoring_chances_for_pct",
            "scoring_chances_shots_for",
            "scoring_chances_shots_against",
            "scoring_chances_shots_for_pct",
            "scoring_chances_goals_for",
            "scoring_chances_goals_against",
            "scoring_chances_goals_for_pct",
            "scoring_chances_shooting_pct",
            "scoring_chances_save_pct",
            "high_danger_chances_for",
            "high_danger_chances_against",
            "high_danger_chances_for_pct",
            "high_danger_shots_for",
            "high_danger_shots_against",
            "high_danger_shots_for_pct",
            "high_danger_goals_for",
            "high_danger_goals_against",
            "high_danger_goals_for_pct",
            "high_danger_shooting_pct",
            "high_danger_save_pct",
            "medium_danger_chances_for",
            "medium_danger_chances_against",
            "medium_danger_chances_for_pct",
            "medium_danger_shots_for",
            "medium_danger_shots_against",
            "medium_danger_shots_for_pct",
            "medium_danger_goals_for",
            "medium_danger_goals_against",
            "medium_danger_goals_for_pct",
            "medium_danger_shooting_pct",
            "medium_danger_save_pct",
            "low_danger_chances_for",
            "low_danger_chances_against",
            "low_danger_chances_for_pct",
            "low_danger_shots_for",
            "low_danger_shots_against",
            "low_danger_shots_for_pct",
            "low_danger_goals_for",
            "low_danger_goals_against",
            "low_danger_goals_for_pct",
            "low_danger_shooting_pct",
            "low_danger_save_pct",
            "shooting_pct",
            "save_pct",
            "pdo_rating",
        ]
    ]

    print("Processed season stats data")

    return df


###########################################################################################################################################
# NEW CODE BLOCK - Process nhldb tables: teams, season, game_type, and season_stats
###########################################################################################################################################


def process_teams_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Processes the teams data for nhldb by selecting and deduplicating team-related columns.

    Args:
        df (pd.DataFrame): The source DataFrame containing NHL stats data.

    Returns:
        pd.DataFrame: A DataFrame containing unique teams with columns 'team_id' and 'team_full_name'.
    """
    df = df[["team_id", "team_full_name"]]
    df = df.drop_duplicates(subset=["team_id"], keep="first").reset_index(drop=True)
    print("Processed teams data")

    return df


def process_season_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Processes the season data for nhldb by selecting and deduplicating season-related columns.

    Args:
        df (pd.DataFrame): The source DataFrame containing NHL stats data.

    Returns:
        pd.DataFrame: A DataFrame containing unique seasons with columns 'season_id' and 'season'.
    """
    df = df[["season_id", "season"]]
    df = df.drop_duplicates(subset=["season_id"], keep="first").reset_index(drop=True)
    print("Processed season data")

    return df


def process_game_type_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Processes the game type data for nhldb by selecting and deduplicating game type columns.

    Args:
        df (pd.DataFrame): The source DataFrame containing NHL stats data.

    Returns:
        pd.DataFrame: A DataFrame containing unique game types with columns 'game_type_id' and 'game_type'.
    """
    df = df[["game_type_id", "game_type"]]
    df = df.drop_duplicates(subset=["game_type_id"], keep="first").reset_index(
        drop=True
    )
    print("Processed game_type data")

    return df


def season_stats_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Prepares the season_stats data by dropping unnecessary columns.

    Args:
        df (pd.DataFrame): The source DataFrame containing NHL stats data.

    Returns:
        pd.DataFrame: A DataFrame containing season statistics ready for insertion.
    """
    df = df.drop(["game_type", "season", "team_full_name"], axis=1, errors="ignore")
    print("Processed season_stats data")

    return df


###########################################################################################################################################
# NEW CODE BLOCK - Insert data into nhldb tables: teams, season, game_type, and season_stats
###########################################################################################################################################


def insert_teams_data(
    teams_df: pd.DataFrame, conn: ps.extensions.connection, cur: ps.extensions.cursor
) -> None:
    """
    Inserts teams data line by line into the nhldb 'teams' table.

    Args:
        teams_df (pd.DataFrame): DataFrame containing teams data.
        conn (ps.extensions.connection): The database connection.
        cur (ps.extensions.cursor): The database cursor.
    """
    try:
        count = 0
        for index, row in teams_df.iterrows():
            cur.execute(teams_table_insert, list(row))
            conn.commit()
            count += 1
            print(
                "Teams data inserted line-by-line into nhldb successfully " + str(count)
            )
    except ps.Error as e:
        print("\n Error:")
        print(e)
    print("Columns inserted: " + str(teams_df.shape[1]))

    return None


def insert_season_data(
    season_df: pd.DataFrame, conn: ps.extensions.connection, cur: ps.extensions.cursor
) -> None:
    """
    Inserts season data line by line into the nhldb 'season' table.

    Args:
        season_df (pd.DataFrame): DataFrame containing season data.
        conn (ps.extensions.connection): The database connection.
        cur (ps.extensions.cursor): The database cursor.
    """
    try:
        count = 0
        for index, row in season_df.iterrows():
            cur.execute(season_table_insert, list(row))
            conn.commit()
            count += 1
            print(
                "Season data inserted line-by-line into nhldb successfully "
                + str(count)
            )
    except ps.Error as e:
        print("\n Error:")
        print(e)
    print("Columns inserted: " + str(season_df.shape[1]))

    return None


def insert_game_type_data(
    game_type_df: pd.DataFrame,
    conn: ps.extensions.connection,
    cur: ps.extensions.cursor,
) -> None:
    """
    Inserts game type data line by line into the nhldb 'game_type' table.

    Args:
        game_type_df (pd.DataFrame): DataFrame containing game type data.
        conn (ps.extensions.connection): The database connection.
        cur (ps.extensions.cursor): The database cursor.
    """
    try:
        count = 0
        for index, row in game_type_df.iterrows():
            cur.execute(game_type_table_insert, list(row))
            conn.commit()
            count += 1
            print(
                "Game type data inserted line-by-line into nhldb successfully "
                + str(count)
            )
    except ps.Error as e:
        print("\n Error:")
        print(e)
    print("Columns inserted: " + str(game_type_df.shape[1]))

    return None


def insert_season_stats_data(
    season_stats_df: pd.DataFrame,
    conn: ps.extensions.connection,
    cur: ps.extensions.cursor,
) -> None:
    """
    Inserts season stats data line by line into the nhldb 'season_stats' table.

    Args:
        season_stats_df (pd.DataFrame): DataFrame containing season statistics.
        conn (ps.extensions.connection): The database connection.
        cur (ps.extensions.cursor): The database cursor.
    """
    try:
        count = 0
        for index, row in season_stats_df.iterrows():
            cur.execute(season_stats_table_insert, list(row))
            conn.commit()
            count += 1
            print(
                "Season stats data inserted line-by-line into nhldb successfully "
                + str(count)
            )
    except ps.Error as e:
        print("\n Error:")
        print(e)
    print("Columns inserted: " + str(season_stats_df.shape[1]))

    return None


###########################################################################################################################################
# NEW CODE BLOCK - Store CSV file
###########################################################################################################################################


def store_data(main_file_search_path: str, prefix: str, store_export_path: str) -> None:
    """
    Moves CSV files with the specified prefix from the main file search path to the export directory,
    organizing them into a folder named with the current date.

    Args:
        main_file_search_path (str): The directory where the files are located.
        prefix (str): The prefix that identifies which files to move.
        store_export_path (str): The target directory where files will be stored.
    """
    files = [f for f in os.listdir(main_file_search_path) if f.startswith(prefix)]
    if len(files) > 0:
        try:
            date_dir = os.path.join(
                store_export_path, datetime.datetime.now().strftime("%Y-%m-%d")
            )
            os.makedirs(date_dir, exist_ok=True)
            for file in files:
                shutil.move(
                    os.path.join(main_file_search_path, file),
                    os.path.join(date_dir, file),
                )
                print("CSV stored")
        except Exception:
            pass
    else:
        pass

    return None


###########################################################################################################################################
# NEW CODE BLOCK - Run ETL pipeline
###########################################################################################################################################


def transform_load(password: str = DB_PASSWORD) -> None:
    """
    Executes the ETL pipeline:
      - Connects to the 'nhldb' database.
      - Processes raw season and playoff data.
      - Processes individual tables (teams, season, game_type, season_stats).
      - Inserts data into nhldb tables.
      - Moves CSV files to the export directory.
      - Creates cumulative data models for regular season and playoffs.

    Args:
        password (str): The database password. Defaults to DB_PASSWORD from environment variables.

    Returns:
        None
    """
    # Connect to database
    try:
        conn = ps.connect(
            f"""
            host=localhost
            dbname=nhldb
            user=postgres
            password={password}
            """
        )
        cur = conn.cursor()
        print("Successfully connected to nhldb")
    except ps.Error as e:
        print("\n Database Error:")
        print(e)
        return

    # Process season and playoff data
    df = process_data()

    # Process teams table
    teams_df = process_teams_data(df=df)

    # Process season table
    season_df = process_season_data(df=df)

    # Process game type table
    game_type_df = process_game_type_data(df=df)

    # Process season_stats table
    season_stats_df = season_stats_data(df=df)

    # Give operator time to scan the event
    print("Loading...")
    time.sleep(5)

    # Insert teams data
    insert_teams_data(teams_df=teams_df, conn=conn, cur=cur)
    print("Loading...")
    time.sleep(5)

    # Insert season data
    insert_season_data(season_df=season_df, conn=conn, cur=cur)
    print("Loading...")
    time.sleep(5)

    # Insert game type data
    insert_game_type_data(game_type_df=game_type_df, conn=conn, cur=cur)
    print("Loading...")
    time.sleep(5)

    # Insert season_stats data
    insert_season_stats_data(season_stats_df=season_stats_df, conn=conn, cur=cur)
    print("Loading...")
    time.sleep(5)

    # Store CSV file
    store_data(
        main_file_search_path=os.path.abspath(
            os.path.join(current_dir, "..", "..", "NHL_ML_Analysis")
        ),
        prefix="NHL",
        store_export_path=os.path.abspath(
            os.path.join(current_dir, "..", "..", r"NHL_ML_Analysis\ETL\NHL_Data")
        ),
    )

    print("Working on creating cumulative data models")

    # Create cumulative models for regular season and playoffs
    create_team_stats_cumulative_regular_season_model(conn=conn, cur=cur)
    create_team_stats_cumulative_playoffs_model(conn=conn, cur=cur)

    print(
        """Cumulative data models complete:
          - Regular Season Team Stats
          - Playoffs Teams Stats
        """
    )

    conn.close()
    print("nhldb connection closed")

    return None


if __name__ == "__main__":
    transform_load()
