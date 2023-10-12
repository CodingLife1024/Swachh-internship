# this code keeps updating the firebase database
import datetime
import csv
import time
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import os

# Initialize Firebase Admin SDK
cred = credentials.Certificate('pkWin.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://datafirst-5ec83-default-rtdb.firebaseio.com'
})

# Reference to the Firebase Realtime Database
ref = db.reference(datetime.datetime.now().strftime("%Y:%m:%d"))

# Function to push data to the database
def push_data(data):
    custom_push_id = datetime.datetime.now().strftime("%H:%M:%S:%f")
    ref.child(custom_push_id).set(data)

# Check if the CSV file is empty
def is_csv_empty(filename):
    with open(filename, 'r') as file:
        header = file.readline().strip()
        return len(header) == 0

# Read data from CSV file starting from the last processed row and push to the database
def read_csv_and_push(filename, last_processed_row):
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        rows = list(reader)

        for row in rows[last_processed_row:]:
            push_data(row)

    return len(rows)

# Function to continuously monitor the CSV file for changes and push new data
def monitor_csv_changes(csv_filename):
    last_processed_row = 0
    last_modified_time = 0

    while True:
        current_modified_time = os.path.getmtime(csv_filename)

        if current_modified_time > last_modified_time:
            last_modified_time = current_modified_time
            last_processed_row = read_csv_and_push(csv_filename, last_processed_row)

        time.sleep(1)  # Wait for 1 second before checking for changes again

def send_message(key, value):
    data = {key: value}
    push_data(data)

# Function to call when you want to monitor the CSV file and push new data
def process_csv(csv_filename):
    # Start monitoring the CSV file for changes and push new data
    monitor_csv_changes(csv_filename)
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

send_message("process_start", "1")