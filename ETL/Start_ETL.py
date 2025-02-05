import os
import sys

# Get the current working directory (the directory of the running script)
current_dir = os.getcwd()
# Add the target directory to the system path for API extraction
sys.path.append(os.path.abspath(os.path.join(current_dir, "Extract_API_NHL_Data")))
from API_Web_Scraper_NHL import extract

# Add the target directory to the system path for ETL process
sys.path.append(os.path.abspath(os.path.join(current_dir, "Transform_Load")))
from Transform_Load_NHL import transform_load


def main() -> None:
    """
    Runs the interactive pipeline to:
      - Extract NHL season and playoff data from the API.
      - Run the ETL process to transform and load the data into the database.

    The user is prompted whether to run each step.
    """
    ###########################################################################################################################################
    # NEW BLOCK - API & Web Scraper for Season and Playoff Data
    ###########################################################################################################################################
    yesChoice = ["yes", "y"]
    noChoice = ["no", "n"]

    input_1: str = input(
        "Would you like to extract season data from the NHL API & naturalstattrick.com? ['yes','y'] or ['no','n'] "
    )
    input_1 = input_1.lower()

    if input_1 in yesChoice:
        try:
            # Warn and store NHL season and playoff data to data storage directories via CSV
            print(
                "Please wait while we get the data from the NHL API & naturalstattrick.com"
            )
            extract()
            print("Data stored as a CSV")
            input(
                "Press enter to continue to the ETL process or Ctrl+C to end the program"
            )
        except Exception as e:
            print(e)
            input(
                "Please check the error above, then press enter to continue to the ETL process or Ctrl+C to end the program"
            )
    elif input_1 in noChoice:
        print("You have skipped the data extraction process")
    else:
        input(
            "You have entered an incorrect response; please press enter to end the program"
        )
        sys.exit()

    ###########################################################################################################################################
    # NEW BLOCK - ETL Process
    ###########################################################################################################################################
    input_2: str = input(
        "Would you like to run the ETL process? ['yes','y'] or ['no','n'] "
    )
    input_2 = input_2.lower()

    if input_2 in yesChoice:
        try:
            # Run the ETL pipeline to transform and load data into nhldb
            print("Transforming and loading the data")
            transform_load()
            input(
                "ETL process complete. Please press enter or Ctrl+C to end the program"
            )
        except Exception as e:
            print(e)
            input("Please check the error above and press enter to continue")
    elif input_2 in noChoice:
        print("You have skipped the ETL process")
        print("Program complete")
    else:
        input(
            "You have entered an incorrect response; please press enter to end the program"
        )
        sys.exit()


if __name__ == "__main__":
    main()
