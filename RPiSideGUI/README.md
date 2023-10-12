### Files in this folder are:

1. pkwin.json
2. main.py
3. csvread.py
4. data.csv
5. installation.sh

## pkwin.json

This is the security key of the Realtime Firebase Database. This enables us to communicate send and receive data from the [realtime database](https://datafirst-5ec83-default-rtdb.firebaseio.com/).

The data is stored in the database in the following format:

Database/
├── date/
│ ├── time/
│ │ ├── aqi
│ │ ├── humidity
│ │ ├── temperature
│ │ ├── pressure
│ │ ├── relativeVelocity
│ │ ├── windVelocity
│ │ ├── vehicleVelocity
│ │ ├── messages

[Link](https://www.youtube.com/watch?v=DCaH4bQ4DxA) to create and use a realtime firebase database. The present database does not have any security configurations or users added for convienence of coding. It is recommended to add some security configuration to the final database. 

## main.py

This file does the following actions:

1. Creates a log file of all actions done by the process every time it is run.
2. Sends data from data.csv to the Firebase database using the csvread.py file is real time.
3. Sends messages for emergency stop, Speed change, etc in real time with negligible delay.
4. Is a GUI that shows the graphs of the data that is being sent to the database.

## csvread.py

This file sends the data from the data.csv file to the database in real time. It also handles sending and recieving messages like speed change, etc. When new data is added to the data.csv file, it is uploaded with negligible delay to the database. It is a continuously running process that keeps track of the last time data was sent and updates this value every time new data is added to the csv file. 

This file sends a message "process_start" every time this function is called. 

## data.csv

This csv file contains the values of the data that is to be uploaded to the database. 

## installation.sh

Running this script would install all the necessary dependencies to the Raspberry Pi system. However it will take a long time to finish downloading all the necessary installations. It is recommended to get a disk copy of the system that already has all the dependencies installed and use this to install all the things needed for this system to run well. 

The list of dependencies are: 
1. Rust
2. Python package Cryptography
3. Python package install firebase-admin "grpcio <= 1.40.0" (if 1.40.0 fails, try 1.39.0)
4. All the other packages mentioned in the code (these do not take much time to install.)