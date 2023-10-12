### Files in this folder are:

1. pkwin.json
2. main.py
3. csvwrite.py
4. data.csv

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
2. Receives data from the firebase database to the datbase.csv using the csvwrite.py file is real time.
3. Sends messages for emergency stop, Speed change, etc in real time with negligible delay.
4. Is a GUI that shows the graphs of the data that is being received to the database.

## csvwrite.py

This file receives the data from the database file to the data.csv in real time. It also handles sending and recieving messages like speed change, etc. When new data is added to the database file, it is uploaded with negligible delay to the data.csv file. It is a continuously running process that keeps track of the last time data was received and updates this value every time new data is added to the database. 

This file sends a message "process_start" every time this function is called. 

## data.csv

This csv file contains the values of the data that is downloaded from the database. 

## installations 

The list of dependencies are: 
1. Rust
2. Python package Cryptography
3. Python package install firebase-admin
4. All the other packages mentioned in the code (these do not take much time to install.)