import datetime
import os
import shutil
from time import sleep

import pandas as pd
import psycopg2 as ps

pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)

# Get the current working directory (the directory of the running script)
current_dir = os.getcwd()

from dotenv import load_dotenv

load_dotenv()
DB_PASSWORD = os.getenv("DB_PASSWORD")


###########################################################################################################################################
# NEW CODE BLOCK - Store Excel
###########################################################################################################################################


def store_old_views_excel() -> None:
    """
    Moves Excel files with the suffix '_view.xlsx' from the 'Dashboard_Data_In_Use' directory
    to the 'Previous_Dahboard_Views' directory under a subfolder named with the current date.

    Returns:
        None
    """
    source_path: str = os.path.abspath(
        os.path.join(current_dir, "..", "Dashboard_Data_In_Use")
    )
    files: list[str] = [f for f in os.listdir(source_path) if f.endswith("_view.xlsx")]

    if files:
        date_dir: str = os.path.join(
            os.path.abspath(os.path.join(current_dir, "..", "Previous_Dahboard_Views")),
            datetime.datetime.now().strftime("%Y-%m-%d"),
        )
        os.makedirs(date_dir, exist_ok=True)
        for file in files:
            shutil.move(os.path.join(source_path, file), os.path.join(date_dir, file))

    print("Excel and CSV files stored")


###########################################################################################################################################
# NEW CODE BLOCK - Pull Excel from nhldb - analysis_view
###########################################################################################################################################


def pull_analysis_view(password: str = DB_PASSWORD) -> None:
    """
    Pulls the 'analysis_view' from the nhldb database and saves it as an Excel file
    in the 'Dashboard_Data_In_Use' directory.

    Args:
        password (str): Database password. Defaults to DB_PASSWORD.

    Returns:
        None
    """

    print("pulling analysis_view")

    # Connect to database and get nhl_view
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

    query: str = """SELECT *
            FROM analytics.analysis_view;"""

    cur.execute(query)
    data = cur.fetchall()

    df_columns = [
        "team_full_name",
        "team_id",
        "game_type",
        "game_type_id",
        "playoff_outcome",
        "playoff_outcome_id",
        "years_since_last_active",
        "start_year",
        "team_improvement_during_regular_season",
        "regular_season_sum",
        "made_playoffs_sum",
        "won_stanley_cup_sum",
        "made_playoffs_efficiency",
        "won_stanley_cup_efficiency",
        "time_on_ice",
        "regular_season_count",
        "made_playoffs_count",
        "won_stanely_cup_count",
        "lost_in_stanely_cup_final_count",
        "games_played",
        "faceoff_win_pct",
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

    df = pd.DataFrame(data, columns=df_columns)

    cur.close()
    conn.close()
    print("Connection to nhldb successfully closed")

    export_path: str = os.path.abspath(
        os.path.join(current_dir, "..", r"Dashboard_Data_In_Use/analysis_view.xlsx")
    )
    df.to_excel(export_path, index=False)
    print(
        "analysis_view has been pulled as an Excel file and ready to use for analysis"
    )

    return None


###########################################################################################################################################
# NEW CODE BLOCK - Pull CSV from nhldb - dashboard_melted_view, dashboard_pivoted_view & dashboard_melted_variance_view
###########################################################################################################################################


def pull_dashboard_views(password: str = DB_PASSWORD) -> None:
    """
    Pulls the 'dashboard_melted_view' & 'dashboard_pivoted_view' from the nhldb database, pivots the data for analysis,
    and saves it as CSV files in the 'Dashboard_Data_In_Use' directory.

    Args:
        password (str): Database password. Defaults to DB_PASSWORD.

    Returns:
        None
    """
    print(
        "pulling dashboard_melted_view, dashboard_pivoted_view & dashboard_melted_variance_view"
    )

    ##############################################################
    # Connect to database and get nhl_view to pull data
    ##############################################################
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

    query: str = """SELECT *
            FROM analytics.analysis_view;"""

    cur.execute(query)
    data = cur.fetchall()

    df_columns = [
        "team_full_name",
        "team_id",
        "game_type",
        "game_type_id",
        "playoff_outcome",
        "playoff_outcome_id",
        "years_since_last_active",
        "start_year",
        "team_improvement_during_regular_season",
        "regular_season_sum",
        "made_playoffs_sum",
        "won_stanley_cup_sum",
        "made_playoffs_efficiency",
        "won_stanley_cup_efficiency",
        "time_on_ice",
        "regular_season_count",
        "made_playoffs_count",
        "won_stanely_cup_count",
        "lost_in_stanely_cup_final_count",
        "games_played",
        "faceoff_win_pct",
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

    df = pd.DataFrame(data, columns=df_columns)

    cur.close()
    conn.close()
    print("Pulled nhldb data successfully")
    print("Connection to nhldb successfully closed")

    ##############################################################
    # Create per 60 minutes features
    ##############################################################
    df = df[(df["start_year"] >= 2007)].reset_index(drop=True)
    df = df[df["game_type"] == "Regular Season"].reset_index(drop=True)

    df["time_on_ice"] = df["time_on_ice"].str.replace(":", ".", 1).str[:-3]
    df["time_on_ice"] = df["time_on_ice"].astype(float)

    per_60_minutes_columns = [
        "corsi_for",
        "corsi_against",
        "fenwick_for",
        "fenwick_against",
        "shots_for",
        "shots_against",
        "goals_for",
        "goals_against",
        "expected_goals_for",
        "expected_goals_against",
        "scoring_chances_for",
        "scoring_chances_against",
        "scoring_chances_shots_for",
        "scoring_chances_shots_against",
        "scoring_chances_goals_for",
        "scoring_chances_goals_against",
        "high_danger_chances_for",
        "high_danger_chances_against",
        "high_danger_shots_for",
        "high_danger_shots_against",
        "high_danger_goals_for",
        "high_danger_goals_against",
        "medium_danger_chances_for",
        "medium_danger_chances_against",
        "medium_danger_shots_for",
        "medium_danger_shots_against",
        "medium_danger_goals_for",
        "medium_danger_goals_against",
        "low_danger_chances_for",
        "low_danger_chances_against",
        "low_danger_shots_for",
        "low_danger_shots_against",
        "low_danger_goals_for",
        "low_danger_goals_against",
    ]

    for col in per_60_minutes_columns:
        df[col + "_per_60_minutes"] = df[col] * 60 / df["time_on_ice"]

    print("Created features per 60 minutes on ice")

    ##############################################################
    # Get variances for KPIs
    ##############################################################
    df_variance = df.copy()

    fixed_columns = [
        "team_full_name",
        "team_id",
        "game_type",
        "game_type_id",
        "playoff_outcome",
        "playoff_outcome_id",
        "years_since_last_active",
        "start_year",
        "team_improvement_during_regular_season",
        "regular_season_sum",
        "made_playoffs_sum",
        "won_stanley_cup_sum",
        "made_playoffs_efficiency",
        "won_stanley_cup_efficiency",
        "time_on_ice",
        "regular_season_count",
        "made_playoffs_count",
        "won_stanely_cup_count",
        "lost_in_stanely_cup_final_count",
        "games_played",
        "wins",
    ]

    # Identify columns to melcalculate variancet
    columns_variance = [
        "low_danger_chances_for",
        "medium_danger_goals_for_pct",
        "high_danger_goals_for_per_60_minutes",
        "high_danger_goals_against_per_60_minutes",
        "penalty_kill_net_pct",
        "power_play_net_pct",
        "low_danger_goals_for_per_60_minutes",
        "high_danger_shots_for",
        "save_pct",
    ]

    for col in columns_variance:
        df_variance[col] = df_variance[col] - df_variance.groupby("start_year")[
            col
        ].transform("mean")

    # Identify columns to melt
    columns_to_melt = [
        "low_danger_chances_for",
        "medium_danger_goals_for_pct",
        "high_danger_goals_for_per_60_minutes",
        "high_danger_goals_against_per_60_minutes",
        "penalty_kill_net_pct",
        "power_play_net_pct",
        "low_danger_goals_for_per_60_minutes",
        "high_danger_shots_for",
        "save_pct",
    ]

    # Melt the DataFrame fro dashboard filtering
    df_variance = df_variance.melt(
        id_vars=fixed_columns,  # Columns to keep as-is
        value_vars=columns_to_melt,  # Columns to melt
        var_name="nhl_metrics",  # Name of the melted column containing metric names
        value_name="nhl_metric_variance_values",  # Name of the column containing metric values
    )

    export_path = os.path.abspath(
        os.path.join(
            current_dir,
            "..",
            r"Dashboard_Data_In_Use/dashboard_melted_variance_view.csv",
        )
    )

    df_variance.to_csv(export_path, index=False)

    print("Created KPI variance data frame")

    ##############################################################
    # Melt KPI data
    ##############################################################

    # Identify columns to melt
    columns_to_melt = [
        "low_danger_chances_for",
        "medium_danger_goals_for_pct",
        "high_danger_goals_for_per_60_minutes",
        "high_danger_goals_against_per_60_minutes",
        "penalty_kill_net_pct",
        "power_play_net_pct",
        "low_danger_goals_for_per_60_minutes",
        "high_danger_shots_for",
        "save_pct",
    ]

    # Melt the DataFrame for dashboard filtering
    df = df.melt(
        id_vars=fixed_columns,  # Columns to keep as-is
        value_vars=columns_to_melt,  # Columns to melt
        var_name="nhl_metrics",  # Name of the melted column containing metric names
        value_name="nhl_metric_values",  # Name of the column containing metric values
    )

    export_path = os.path.abspath(
        os.path.join(
            current_dir, "..", r"Dashboard_Data_In_Use/dashboard_melted_view.csv"
        )
    )

    df.to_csv(export_path, index=False)

    print("Created kPI metled data frame")

    ##############################################################
    # Pivot KPI data
    ##############################################################
    # Reverse the Melt (Convert Back to Wide Format) for dashboard kpi view
    df = df.pivot(
        index=fixed_columns,  # These become the index in the wide format
        columns="nhl_metrics",  # The values in this column become new columns
        values="nhl_metric_values",  # The corresponding values fill the new columns
    ).reset_index()

    # Remove the columns' name (which is set to 'nhl_metrics' by pivot)
    df.columns.name = None

    export_path = os.path.abspath(
        os.path.join(
            current_dir, "..", r"Dashboard_Data_In_Use/dashboard_pivoted_view.csv"
        )
    )

    df.to_csv(export_path, index=False)

    print("Created kPI pivoted data frame")
    print(
        "dashboard_melted_view, dashboard_pivoted_view & dashboard_melted_variance_view have been created as CSV files and ready for dashboard refresh"
    )

    return None


if __name__ == "__main__":
    # Store old dashboard view Excel files
    store_old_views_excel()
    # Pull new analysis_view as an Excel file
    pull_analysis_view()
    # Pull new dashboard_view as an Excel file
    pull_dashboard_views()
