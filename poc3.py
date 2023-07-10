import csv
import json
from datetime import datetime
import uuid

def create_basic_vipe_event(row, header, eventdate):
    """
    Function to create the JSON structure based on the row data from the CSV file.

    :param row: A list representing a row from a CSV file.
    :param header: A list representing the header row of the CSV file.
    :return: A dictionary with the JSON structure based on the CSV row.
    """
    myuuid = uuid.uuid4()
    
    event = {
        "reference" : str(myuuid),
        "type": row[0],
        "duration": row[1],
        "name": row[2],
        "assets": [
            {
                "reference": row[3],
                "tcIn": row[4],
                "tcOut": row[5],
                "type": row[6]
            }
        ],
        "startTime": change_date(row[7], eventdate),
        "behaviors": [
            {
                "name": row[8]
            }
        ]
    }

    # Add additional JSON if 'gpi' or 'logo' is in the header
    for i, column_name in enumerate(header):
        if column_name.lower() == 'gpi' and row[i]:
            # new dictionary to be added
            gpi = {
                "name": "SCTE104_OUT",
                "params": {
                    "spliceEventId": row[i],
                    "breakDuration": "00:05:00:00"
                },
                "original": "",
                "disabled": False,
                "rule": False
            }

            # append the new dictionary to the list in 'behaviors'
            event['behaviors'].append(gpi)

        elif column_name.lower() == 'logo' and row[i]:
            event['logo'] = row[i]

    return event


def change_date(input_datetime, new_date):
    # Convert input to datetime object
    input_datetime = datetime.strptime(input_datetime, "%Y-%m-%d %H:%M:%S:%f")

    # Convert new_date to datetime object
    new_date = datetime.strptime(new_date, "%Y-%m-%d")

    # Replace year, month, day in input_datetime with those from new_date
    new_datetime = input_datetime.replace(year=new_date.year, month=new_date.month, day=new_date.day)

    # Convert new_datetime back to string and return it
    return new_datetime.strftime("%Y-%m-%d %H:%M:%S:%f")[:-4]


def read_csv_and_create_json(csv_filename, json_filename, eventdate):
    """
    Function to read data from a CSV file and write it to a JSON file.

    :param csv_filename: The filename of the CSV file to read from.
    :param json_filename: The filename of the JSON file to write to.
    """
    # Open the CSV file
    with open(csv_filename, "r") as csv_file:
        # Create a CSV reader
        reader = csv.reader(csv_file)
        # Read the header
        header = next(reader)
        # Initialize the data
        data = {"events": []}
        # Iterate over the CSV rows
        for row in reader:
            print(row[8])

            if row[8] == "CLP":
                # Call the create_basic_vipe_event function to create the JSON structure
                event_data = create_basic_vipe_event(row, header, eventdate)
                # print(event_data)

                # Append the event data
                data["events"].append(event_data)
            
            # Write the data to the JSON file
            with open(json_filename, "w") as json_file:
                json_file.write(json.dumps(data, indent=4))


    print(f"JSON data has been written to '{json_filename}'")


if __name__ == "__main__":

    SCHEDULE_OUTPUT_DATE = datetime.today().strftime("%Y-%m-%d")
    # Define the CSV and JSON filenames
    csv_filename = "test_sched_with_basic_ads_inter.csv"
    json_filename = "test_sched_with_basic_ads_inter.json"

    # Call the function to read CSV and create JSON
    read_csv_and_create_json(csv_filename, json_filename, SCHEDULE_OUTPUT_DATE)
