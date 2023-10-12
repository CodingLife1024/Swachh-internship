import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import csv
import os
import time

# Initialize Firebase Admin SDK
cred = credentials.Certificate('pkWin.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://datafirst-5ec83-default-rtdb.firebaseio.com'
})

# Get a database reference
ref = db.reference(datetime.datetime.now().strftime("%Y:%m:%d"))

def push_data(data):
    custom_push_id = datetime.datetime.now().strftime("%H:%M:%S:%f")
    ref.child(custom_push_id).set(data)

# Specify the CSV file name
csv_filename = 'data.csv'

def update_csv_file(event):
    # Retrieve data
    header_row = ['time', 'aqi', 'humidity', 'pressure', 'relativeVelocity', 'temperature', 'vehicleVelocity', 'windVelocity']
    data = event.data
    messages = ["fanspeedchange", "speedchange", "emergencystop", "restart", "changespeed", "process_start", "process_end"]
    # Check if data exists
    if data:
        is_csv_empty = os.stat(csv_filename).st_size == 0

        # Get the last processed key
        last_key = ''

        with open(csv_filename, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if len(row) > 0:
                    last_key = row[0]

        with open(csv_filename, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)

            if is_csv_empty:
                writer.writerow(header_row)

            for key, value in data.items():
                if key > last_key:  # Write only the new lines
                    if isinstance(value, dict) and all(message not in value for message in messages):
                        row_values = [key]
                        for inner_key in header_row[1:]:  # Preserve column order
                            row_values.append(value.get(inner_key, ""))
                        writer.writerow(row_values)

            # Update the last processed key
            if data:
                last_key = max(data.keys())

    else:
        print("No data available")

def send_message(key, value):
    data = {key: value}
    push_data(data)

def process_csv():
    while True:
        try:
            # Listen for changes in the database
            ref.listen(update_csv_file)
        except Exception as e:
            print(f"An error occurred: {e}")

        # Wait for a specific interval before listening again
        time.sleep(3)  # Adjust the interval as needed

def receive_message():
    latest_timestamp = ""
    latest_message_value = None

    messages = ["fanspeedchange", "speedchange", "emergencystop", "restart", "changespeed", "process_start", "process_end"]

    while True:
        snapshot = ref.get()

        if snapshot is not None and isinstance(snapshot, dict):
            for timestamp, data in reversed(snapshot.items()):
                for message in messages:
                    message_value = data.get(message)
                    if message_value is not None:
                        latest_timestamp = timestamp
                        latest_message_value = message_value
                        break  # Exit the loop after finding the last instance
                if latest_message_value is not None:
                    break  # Exit the loop after finding the most recent message

        if latest_message_value is not None:
            return [timestamp, message, latest_message_value]

# Call the function to start the process
# update_csv_file
send_message("process_start", "1")
