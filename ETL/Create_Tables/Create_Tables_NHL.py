import os
import sys

import psycopg2 as ps

current_dir = os.getcwd()
# Add the target directory to the system path
sys.path.append(os.path.abspath(os.path.join(current_dir, "..", "SQL_Queries")))
from dotenv import load_dotenv
from SQL_Queries import *

load_dotenv()
DB_PASSWORD = os.getenv("DB_PASSWORD")

###########################################################################################################################################
# NEW CODE BLOCK - Create nhldb
###########################################################################################################################################


def create_database(password=DB_PASSWORD):
    """
    - Creates and connects to the nhldb
    - Returns the connection and cursor to nhldb

    Args:
        password: The database password.
    """

    # connect to default database port: 5432
    conn = ps.connect(
        f"""
    
        host=localhost
        dbname=postgres
        user=postgres
        password={password}
        
    """
    )

    conn.set_session(autocommit=True)
    cur = conn.cursor()

    # create nhldb database with UTF8 encoding
    cur.execute("DROP DATABASE IF EXISTS nhldb;")
    cur.execute("CREATE DATABASE nhldb WITH ENCODING 'utf8' TEMPLATE template0;")

    # close connection to default database
    conn.close()

    # connect to nhldb database
    conn = ps.connect(
        f"""
    
        host=localhost
        dbname=nhldb
        user=postgres
        password={password}
        
    """
    )

    cur = conn.cursor()

    # Create schema raw
    cur.execute("CREATE SCHEMA IF NOT EXISTS raw;")
    # Create Season Stats Type
    cur.execute(create_season_stats_type_raw)
    # Create schema analytics
    cur.execute("CREATE SCHEMA IF NOT EXISTS analytics;")
    # Create Season Stats Type
    cur.execute(create_season_stats_type_analytics)
    conn.commit()

    return cur, conn


###########################################################################################################################################
# NEW CODE BLOCK - Create tables in nhldb
###########################################################################################################################################


def drop_tables(cur, conn) -> None:
    """
    Drops each table using the queries in `drop_table_queries` list

    Args:
        conn (ps.extensions.connection): The database connection.
        cur (ps.extensions.cursor): The database cursor.
    """
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()

    return None


def create_tables(cur, conn) -> None:
    """
    Creates each table using the queries in `create_table_queries` list

    Args:
        conn (ps.extensions.connection): The database connection.
        cur (ps.extensions.cursor): The database cursor.
    """
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()

    return None


def create_view(cur, conn) -> None:
    """
    Creates nhl view

    Args:
        conn (ps.extensions.connection): The database connection.
        cur (ps.extensions.cursor): The database cursor.
    """
    cur.execute(nhl_view_create)
    conn.commit()

    return None


###########################################################################################################################################
# NEW CODE BLOCK - Team names and IDs from NHL API
###########################################################################################################################################


def main() -> None:
    """
    - Drops (if exists) and creates the nhldb database
    - Establishes connection with the nhldb database and gets cursor to it
    - Drops all the tables
    - Creates all tables needed
    - Finally, closes the connection
    """

    try:
        cur, conn = create_database()

        # Drop tables
        drop_tables(cur=cur, conn=conn)

        # Create tables
        create_tables(cur=cur, conn=conn)

        print(
            """
        Tables in nhldb have been created: 
        - teams
        - season
        - game_type
        - season_stats
        - team_stats_regular_season
        - team_stats_playoffs
        """
        )

        conn.close()

    except ps.Error as e:
        print("\n Error:")
        print(e)

    return None


if __name__ == "__main__":
    main()
