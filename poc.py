import csv
import json
from datetime import datetime

def create_json_structure(row,eventdate):
    """
    Function to create the JSON structure based on the row data from the CSV file.

    :param row: A list representing a row from a CSV file.
    :return: A dictionary with the JSON structure based on the CSV row.
    """
    return {
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
        "startTime": change_date(row[7],eventdate),
        "behaviors": [
            {
                "name": row[8]
            }
        ]
    }


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
        # Skip the header
        next(reader)
        # Initialize the data
        data = {"events": []}
        # Iterate over the CSV rows
        for row in reader:
            # Call the create_json_structure function to create the JSON structure
            event_data = create_json_structure(row, eventdate)
            print(event_data)

            # Append the event data
            data["events"].append(event_data)
        
        # Write the data to the JSON file
        with open(json_filename, "w") as json_file:
            json_file.write(json.dumps(data, indent=4))


    print(f"JSON data has been written to '{json_filename}'")

if __name__ == "__main__":

    SCHEDULE_OUTPUT_DATE = datetime.today().strftime("%Y-%m-%d")
    # Define the CSV and JSON filenames
    csv_filename = "poc2.csv"
    json_filename = "data.json"

    # Call the function to read CSV and create JSON
    read_csv_and_create_json(csv_filename, json_filename,SCHEDULE_OUTPUT_DATE)

    # The below code is currently commented out. 
    # If you wish to add a new behavior to each event in the JSON, 
    # and remove the last behavior if there is more than one, you could uncomment and use it.

    # # Load the created JSON file
    # with open(json_filename, "r") as json_file:
    #     data = json.load(json_file)
    
    # # Add another behavior
    # extra_behavior = "Behavior2"
    # for event in data["events"]:
    #     event["behaviors"].append({"name": extra_behavior})

    # # Remove the last behavior if there is more than one
    # for event in data["events"]:
    #     if len(event["behaviors"]) > 1:
    #         event["behaviors"].pop()

    # # Save the updated JSON data
    # with open(json_filename, "w") as json_file:
    #     json_file.write(json.dumps(data, indent=4))
