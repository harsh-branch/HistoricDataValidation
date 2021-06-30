# HistoricDataValidation
This python script would let you validate the data received by the client's data team for ingestion as per teh requirements and recommendations here: https://help.branch.io/developers-hub/docs/importing-historical-user-data


In order to run this validation script, make sure that you have Python 3+ installed on your machine.



Command to run the script: python validate.py

The script will request the app_id for which you are injesting this data: Enter the Branch App ID

The script will request for the path of the file containing the data dump: Enter the exact file path with the extension of the file





The script can generate 2 CSV files for you to share it with the client. These will be the following:

**nonJsonLines.csv:** Will contain the lines which are NOT in JSON format

**incorrectJsonLines.csv:** Will contain lines which are NOT in the correct format as per the docs
