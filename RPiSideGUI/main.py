from tkinter import *
import tkinter as tk
import customtkinter
import csv
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.backends.backend_tkagg as tkagg
import threading
from csvread import process_csv, receive_message, send_message
import logging
import sys

# Generate a timestamp to include in the log file name
timestamp = datetime.now().strftime("%Y-%m-%d__%H_%M_%S")

# Configure the logging with a unique log file name
log_file_name = f"history_{timestamp}.log"
logging.basicConfig(filename=log_file_name, level=logging.INFO)

# Create a custom StreamHandler to redirect sys.stdout to the log file
class LogStreamHandler(logging.StreamHandler):
    def __init__(self, stream=None):
        super().__init__(stream)

    def emit(self, record):
        msg = self.format(record)
        self.stream.write(f"{record.getMessage()}\n")

# Create the logger and add the custom StreamHandler
logger = logging.getLogger("LogSender")

# Remove existing handlers, if any
for handler in logger.handlers:
    logger.removeHandler(handler)

# Add the custom StreamHandler
logger.addHandler(LogStreamHandler(sys.stdout))

def get_last_non_empty_row(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        last_non_empty_row = None

        for row_number, row in enumerate(reader, start=1):
            if any(row):  # Check if any element in the row is non-empty
                last_non_empty_row = row_number
    return last_non_empty_row

FREQUENCY = 1000 # Frequency of data updates
FILE_PATH = "data.csv"

ALL_TIMES = []
ALL_Y_DATA_AQI = []
ALL_Y_DATA_HUMIDITY = []
ALL_Y_DATA_PRESSURE = []
ALL_Y_DATA_TEMPERATURE = []
ALL_Y_DATA_WIND = []
ALL_Y_DATA_RELATIVE = []
ALL_Y_DATA_VEHICLE = []
LAST_NON_EMPTY_ROW = 0
START_ROW = 0
LOG_ON = 0
NO_NEW_DATA = 0

LAST_AQI_LIST = []
LAST_HUMIDITY_LIST = []
LAST_PRESSURE_LIST = []
LAST_TEMPERATURE_LIST = []
LAST_WIND_LIST = []
LAST_RELATIVE_LIST = []
LAST_VEHICLE_LIST = []

LAST_AQI_VALUE = 0
LAST_HUMIDITY_VALUE = 0
LAST_PRESSURE_VALUE = 0
LAST_TEMPERATURE_VALUE = 0
LAST_WIND_VALUE = 0
LAST_RELATIVE_VALUE = 0
LAST_VEHICLE_VALUE = 0

RECEIVED_MESSAGES = []
LAST_NOTIFICATION_TIMESTAMP=""

# Define a function that will run the process_csv() function in a separate thread
def run_csv_processing():
    process_csv(FILE_PATH)  # Call your process_csv() function here

# Create a new thread for running the csv processing function
csv_thread = threading.Thread(target=run_csv_processing)

# Start the thread
csv_thread.start()

# returns the current time
def add_time():
    return datetime.now().strftime("%H:%M:%S:%f")

# Gets non empty rows after integer row_number from the csv file and adds the values of the time the rows are read to the global list ALL_TIMES and returns a list of the new values under row_name.
def get_non_empty_rows_after(csv_file_path, row_name, row_number, indicator):
    global ALL_TIMES
    non_empty_values = []
    with open(csv_file_path, 'r') as file:
        reader = csv.DictReader(file)

        for current_row_number, row in enumerate(reader, start=1):
            if current_row_number > row_number and row[row_name] != '':
                non_empty_values.append(float(row[row_name]))
            if indicator == 1:
                ALL_TIMES.append(datetime.now().strftime("%H:%M:%S:%f"))
    return non_empty_values

# This function updates the lists so that the latest data is always available.
def update_lists():
    global LAST_NON_EMPTY_ROW
    global START_ROW
    global ALL_Y_DATA_AQI
    global ALL_Y_DATA_HUMIDITY
    global ALL_Y_DATA_PRESSURE
    global ALL_Y_DATA_TEMPERATURE
    global ALL_Y_DATA_WIND
    global ALL_Y_DATA_RELATIVE
    global ALL_Y_DATA_VEHICLE
    global LOG_ON

    global LAST_AQI_LIST
    global LAST_HUMIDITY_LIST
    global LAST_PRESSURE_LIST
    global LAST_TEMPERATURE_LIST
    global LAST_WIND_LIST
    global LAST_RELATIVE_LIST
    global LAST_VEHICLE_LIST

    global LAST_AQI_VALUE
    global LAST_HUMIDITY_VALUE
    global LAST_PRESSURE_VALUE
    global LAST_TEMPERATURE_VALUE
    global LAST_WIND_VALUE
    global LAST_RELATIVE_VALUE
    global LAST_VEHICLE_VALUE

    global ALL_TIMES

    ALL_Y_DATA_AQI = get_non_empty_rows_after(FILE_PATH, 'aqi', LAST_NON_EMPTY_ROW, 1)
    ALL_Y_DATA_HUMIDITY = get_non_empty_rows_after(FILE_PATH, 'humidity', LAST_NON_EMPTY_ROW, 0)
    ALL_Y_DATA_PRESSURE = get_non_empty_rows_after(FILE_PATH, 'pressure', LAST_NON_EMPTY_ROW, 0)
    ALL_Y_DATA_TEMPERATURE = get_non_empty_rows_after(FILE_PATH, 'temperature', LAST_NON_EMPTY_ROW, 0)
    ALL_Y_DATA_WIND = get_non_empty_rows_after(FILE_PATH, 'windVelocity', LAST_NON_EMPTY_ROW, 0)
    ALL_Y_DATA_RELATIVE = get_non_empty_rows_after(FILE_PATH, 'relativeVelocity', LAST_NON_EMPTY_ROW, 0)
    ALL_Y_DATA_VEHICLE = get_non_empty_rows_after(FILE_PATH, 'vehicleVelocity', LAST_NON_EMPTY_ROW, 0)
    START_ROW = 0

    if ALL_Y_DATA_AQI != []:
        LAST_AQI_LIST = ALL_Y_DATA_AQI[-10:] + [0] * (10 - len(ALL_Y_DATA_AQI[-10:]))
        LAST_AQI_VALUE = ALL_Y_DATA_AQI[-1]
        LAST_HUMIDITY_LIST = ALL_Y_DATA_HUMIDITY[-10:] + [0] * (10 - len(ALL_Y_DATA_HUMIDITY[-10:]))
        LAST_HUMIDITY_VALUE = ALL_Y_DATA_HUMIDITY[-1]
        LAST_PRESSURE_LIST = ALL_Y_DATA_PRESSURE[-10:] + [0] * (10 - len(ALL_Y_DATA_PRESSURE[-10:]))
        LAST_PRESSURE_VALUE = ALL_Y_DATA_PRESSURE[-1]
        LAST_TEMPERATURE_LIST = ALL_Y_DATA_TEMPERATURE[-10:] + [0] * (10 - len(ALL_Y_DATA_TEMPERATURE[-10:]))
        LAST_TEMPERATURE_VALUE = ALL_Y_DATA_TEMPERATURE[-1]
        LAST_WIND_LIST = ALL_Y_DATA_WIND[-10:] + [0] * (10 - len(ALL_Y_DATA_WIND[-10:]))
        LAST_WIND_VALUE = ALL_Y_DATA_WIND[-1]
        LAST_RELATIVE_LIST = ALL_Y_DATA_RELATIVE[-10:] + [0] * (10 - len(ALL_Y_DATA_RELATIVE[-10:]))
        LAST_RELATIVE_VALUE = ALL_Y_DATA_RELATIVE[-1]
        LAST_VEHICLE_LIST = ALL_Y_DATA_VEHICLE[-10:] + [0] * (10 - len(ALL_Y_DATA_VEHICLE[-10:]))
        LAST_VEHICLE_VALUE = ALL_Y_DATA_VEHICLE[-1]

    if get_last_non_empty_row(FILE_PATH) != LAST_NON_EMPTY_ROW:
        LAST_NON_EMPTY_ROW = get_last_non_empty_row(FILE_PATH)
    else:
        ALL_Y_DATA_AQI = []
        ALL_Y_DATA_HUMIDITY = []
        ALL_Y_DATA_PRESSURE = []
        ALL_Y_DATA_RELATIVE = []
        ALL_Y_DATA_TEMPERATURE = []
        ALL_Y_DATA_VEHICLE = []
        ALL_TIMES = []
        ALL_Y_DATA_WIND = []

    logger.info("Last non-empty row: %s", LAST_NON_EMPTY_ROW)
    logger.info("Time List is: %s", ALL_TIMES)
    logger.info("Aqi data: %s", ALL_Y_DATA_AQI)
    logger.info("Humidity data: %s", ALL_Y_DATA_HUMIDITY)
    logger.info("Pressure data: %s", ALL_Y_DATA_PRESSURE)
    logger.info("Relative Velocity data: %s", ALL_Y_DATA_RELATIVE)
    logger.info("Temperature Data: %s", ALL_Y_DATA_TEMPERATURE)
    logger.info("Vehicle Velocity data: %s", ALL_Y_DATA_VEHICLE)
    logger.info("Wind Velocity data: %s", ALL_Y_DATA_WIND)
    logger.info("Start row: %s", START_ROW)

    if LOG_ON == 1:
        print(LAST_NON_EMPTY_ROW)
        print(ALL_Y_DATA_AQI)
        print(ALL_Y_DATA_HUMIDITY)
        print(ALL_Y_DATA_PRESSURE)
        print(ALL_Y_DATA_RELATIVE)
        print(ALL_Y_DATA_TEMPERATURE)
        print(ALL_Y_DATA_VEHICLE)
        print(ALL_Y_DATA_WIND)
        print(START_ROW)

    app.after(30000, update_lists)

# This function returns the current x values and y values of the graph "row_name". This function is called whenever the graph that is shown needs to be updated.
def generate_data_from_csv(file_path, row_name, num_data, start_row):

    global LAST_AQI_LIST
    global LAST_HUMIDITY_LIST
    global LAST_PRESSURE_LIST
    global LAST_TEMPERATURE_LIST
    global LAST_WIND_LIST
    global LAST_RELATIVE_LIST
    global LAST_VEHICLE_LIST

    x_data = list(range(0, num_data))
    y_data = []
    less_len = True
    if len(ALL_Y_DATA_AQI) >= num_data:
        less_len = False
    if row_name == 'aqi':
        ll = ALL_Y_DATA_AQI[start_row: start_row + 10] + [0] * (num_data - len(ALL_Y_DATA_AQI[start_row: start_row + 10]))
        if ll[-1] == 0:
            ll = LAST_AQI_LIST
    elif row_name == 'humidity':
        ll = ALL_Y_DATA_HUMIDITY[start_row: start_row + 10] + [0] * (num_data - len(ALL_Y_DATA_HUMIDITY[start_row: start_row + 10]))
        if ll[-1] == 0:
            ll = LAST_HUMIDITY_LIST
    elif row_name == 'pressure':
        ll = ALL_Y_DATA_PRESSURE[start_row: start_row + 10] + [0] * (num_data - len(ALL_Y_DATA_PRESSURE[start_row: start_row + 10]))
        if ll[-1] == 0:
            ll = LAST_PRESSURE_LIST
    elif row_name == 'temperature':
        ll = ALL_Y_DATA_TEMPERATURE[start_row: start_row + 10] + [0] * (num_data - len(ALL_Y_DATA_TEMPERATURE[start_row: start_row + 10]))
        if ll[-1] == 0:
            ll = LAST_TEMPERATURE_LIST
    elif row_name == 'relativeVelocity':
        ll = ALL_Y_DATA_RELATIVE[start_row: start_row + 10] + [0] * (num_data - len(ALL_Y_DATA_RELATIVE[start_row: start_row + 10]))
        if ll[-1] == 0:
            ll = LAST_RELATIVE_LIST
    elif row_name == 'windVelocity':
        ll = ALL_Y_DATA_WIND[start_row: start_row + 10] + [0] * (num_data - len(ALL_Y_DATA_WIND[start_row: start_row + 10]))
        if ll[-1] == 0:
            ll = LAST_WIND_LIST
    elif row_name == 'vehicleVelocity':
        ll = ALL_Y_DATA_VEHICLE[start_row: start_row + 10] + [0] * (num_data - len(ALL_Y_DATA_VEHICLE[start_row: start_row + 10]))
        if ll[-1] == 0:
            ll = LAST_VEHICLE_LIST

    y_data = ll
    return x_data, y_data

# This function plots the graphs using the generated data from the generate_data_from_csv function.
def update_graph(ax, title, ylabel, row_name, lower_end, higher_end, skip_interval, i):
    global LOG_ON
    global START_ROW
    x_data, y_data = generate_data_from_csv(FILE_PATH, row_name, 10, i)
    logger.info(x_data)
    logger.info(y_data)
    if LOG_ON == 1:
        print(x_data)
        print(y_data)
    # Clear the previous graph
    ax.clear()

    # Plot the new data
    ax.plot(x_data, y_data)

    # Customize the graph
    ax.set_xlim(1, 10)  # Set x-axis limits
    ax.set_ylim(lower_end, higher_end + 1)  # Set y-axis limits

    # Set tick frequency
    ax.set_xticks(range(0, 11, 2))  # Show ticks for every integer from 1 to 10 on the x-axis
    ax.set_yticks(range(0, higher_end + 1, skip_interval))  # Show ticks for every 5 units from 1 to 55 on the y-axis

    ax.set_xlabel(datetime.now().strftime("%H:%M:%S:%f"))  # Set x-axis label
    ax.set_ylabel(ylabel)  # Set y-axis label
    ax.set_title(title)

    # Redraw the canvas
    ax.figure.canvas.draw()

# Create the Figure and Axes objects
figure, axes = plt.subplots(2, 3, figsize=(3, 3))

def update_time():
    current_time = datetime.now().strftime("%Y-%m-%d :: %H:%M:%S")
    label.configure(text=current_time)
    label.after(FREQUENCY, update_time)  # Update every 1 second (1000 milliseconds)

# This function updates the statistics that are visible on the left side of the GUI.
def update_statistics():
    global START_ROW
    global LOG_ON
    global LAST_AQI_VALUE
    global LAST_HUMIDITY_VALUE
    global LAST_PRESSURE_VALUE
    global LAST_TEMPERATURE_VALUE
    global LAST_VEHICLE_VALUE
    global LAST_RELATIVE_VALUE
    global LAST_WIND_VALUE

    if START_ROW >= len(ALL_Y_DATA_AQI):
        aqi_value = LAST_AQI_VALUE
        aqi.configure(text=aqi_value)
        humidity_value = LAST_HUMIDITY_VALUE
        hum.configure(text=humidity_value)
        pressure_value = LAST_PRESSURE_VALUE
        pressure.configure(text=pressure_value)
        temp_value = LAST_TEMPERATURE_VALUE
        temp.configure(text=temp_value)
        vehicle_velocity_value = LAST_VEHICLE_VALUE
        vehicle_velocity.configure(text=vehicle_velocity_value)
        relative_velocity_value = LAST_RELATIVE_VALUE
        relative_velocity.configure(text=relative_velocity_value)
        wind_velocity_value = LAST_WIND_VALUE
        wind_velocity.configure(text=wind_velocity_value)
    else:
        aqi_value = ALL_Y_DATA_AQI[START_ROW]
        aqi.configure(text=aqi_value)
        humidity_value = ALL_Y_DATA_HUMIDITY[START_ROW]
        hum.configure(text=humidity_value)
        pressure_value = ALL_Y_DATA_PRESSURE[START_ROW]
        pressure.configure(text=pressure_value)
        temp_value = ALL_Y_DATA_TEMPERATURE[START_ROW]
        temp.configure(text=temp_value)
        vehicle_velocity_value = ALL_Y_DATA_VEHICLE[START_ROW]
        vehicle_velocity.configure(text=vehicle_velocity_value)
        relative_velocity_value = ALL_Y_DATA_RELATIVE[START_ROW]
        relative_velocity.configure(text=relative_velocity_value)
        wind_velocity_value = ALL_Y_DATA_WIND[START_ROW]
        wind_velocity.configure(text=wind_velocity_value)

customtkinter.set_appearance_mode("Dark") # Dark mode is Life
customtkinter.set_default_color_theme("blue") # This is the theme

# Beginning of the GUI part of the code
app = customtkinter.CTk()
width= app.winfo_screenwidth()
height= app.winfo_screenheight()
app.geometry("{0}x{1}+0+0".format(width, height))
app.title("CAQM Bus")

tabview = customtkinter.CTkTabview(master=app)
tabview.pack(padx=20, pady=20)

tabview.add("Main")  # add tab at the end
tabview.add("Notifications")
tabview.set("Main")  # set currently visible tab

# title = customtkinter.CTkLabel(master=tabview.tab("Main"), text="Real-time statistics")
# title.pack()

label = customtkinter.CTkLabel(master=tabview.tab("Main"), font=("Arial", 18), text="")
label.pack(pady=20)

grid_frame = customtkinter.CTkFrame(master=tabview.tab("Main"))
grid_frame.pack(fill="both", expand=True, padx=20, pady=20)

update_time()

# Left Section : the values of are visible
left_section = customtkinter.CTkFrame(master=grid_frame)  # Set the width to 250 pixels
left_section.grid(row=0, column=0, padx=10, pady=20)

aqiLabel = customtkinter.CTkLabel(master=left_section, font=("Courier", 18, "bold"), text="AQI:") # AQI
aqiLabel.pack()

aqi = customtkinter.CTkLabel(master=left_section, font=("Courier", 18), text="")
aqi.pack()

tempLabel = customtkinter.CTkLabel(master=left_section, font=("Courier", 18, "bold"), text="Temperature (°C):") # Temperature
tempLabel.pack()

temp = customtkinter.CTkLabel(master=left_section, font=("Courier", 18), text="")
temp.pack()

humLabel = customtkinter.CTkLabel(master=left_section, font=("Courier", 18, "bold"), text="Humidity:") # Humidity
humLabel.pack()

hum = customtkinter.CTkLabel(master=left_section, font=("Courier", 18), text="")
hum.pack()

vehicleLabel = customtkinter.CTkLabel(master=left_section, font=("Courier", 18, "bold"), text="Vehicle Velocity (kmph):") # Vehicle Velocity
vehicleLabel.pack()

vehicle_velocity = customtkinter.CTkLabel(master=left_section, font=("Courier", 18), text="")
vehicle_velocity.pack()

relativeLabel = customtkinter.CTkLabel(master=left_section, font=("Courier", 18, "bold"), text="Relative Velocity (kmph):") # Relative Velocity
relativeLabel.pack()

relative_velocity = customtkinter.CTkLabel(master=left_section, font=("Courier", 18), text="")
relative_velocity.pack()

windLabel = customtkinter.CTkLabel(master=left_section, font=("Courier", 18, "bold"), text="Wind Velocity (kmph):") # Wind Velocity
windLabel.pack()

wind_velocity = customtkinter.CTkLabel(master=left_section, font=("Courier", 18), text="")
wind_velocity.pack()

pressureLabel = customtkinter.CTkLabel(master=left_section, font=("Courier", 18, "bold"), text="Pressure (atm):") # Pressure
pressureLabel.pack()

pressure = customtkinter.CTkLabel(master=left_section, font=("Courier", 18), text="")
pressure.pack()

# This code shows a popup messagebox every time a message is sent or received
def show_custom_messagebox(title, message):
    top = tk.Toplevel()
    top.title(title)

    # Configure the style of the messagebox
    top.configure(bg="black")  # Set the background color to black

    # Create labels for the title and message
    title_label = tk.Label(top, text=title, font=("Arial", 16), pady=10, fg="white", bg="black", highlightthickness=0)
    title_label.pack()
    message_label = tk.Label(top, text=message, font=("Arial", 12), fg="white", bg="black", highlightthickness=0)
    message_label.pack()

    # Create a button to close the messagebox
    close_button = tk.Button(top, text="Close", command=top.destroy, bg="white", fg="black")
    close_button.pack(pady=10)

    # Auto-close the messagebox after 3 seconds
    top.after(3000, top.destroy)

    # Set the fixed width and height of the messagebox window
    window_width = 400
    window_height = 200
    top.geometry(f"{window_width}x{window_height}")

    top.update_idletasks()
    screen_width = top.winfo_screenwidth()
    screen_height = top.winfo_screenheight()
    x = screen_width - window_width - 50  # 50 pixels offset from the right edge
    y = screen_height - window_height - 150  # 150 pixels offset from the bottom edge
    top.geometry(f"+{x}+{y}")

# Submits an emergency stop message.
def submit_emergency_stop():
    send_message("emergencystop", "1")
    show_custom_messagebox("Notification", "Emergency stop submitted successfully.")

stopButton = customtkinter.CTkButton(master=left_section, text="Emergency Stop", command=submit_emergency_stop)
stopButton.pack(side="bottom", padx=20, pady=25)

# Right Section : This part contains all the graphs.
right_section = customtkinter.CTkFrame(master=grid_frame)
right_section.grid(row=0, column=1, padx=10, pady=20)

figure1 = plt.figure(figsize=(4, 4))
subplot1 = figure1.add_subplot(111)

figure2 = plt.figure(figsize=(4, 4))
subplot2 = figure2.add_subplot(111)

figure3 = plt.figure(figsize=(4, 4))
subplot3 = figure3.add_subplot(111)

figure4 = plt.figure(figsize=(4, 4))
subplot4 = figure4.add_subplot(111)

figure5 = plt.figure(figsize=(4, 4))
subplot5 = figure5.add_subplot(111)

figure6 = plt.figure(figsize=(4, 4))
subplot6 = figure6.add_subplot(111)

figure7 = plt.figure(figsize=(4, 4))
subplot7 = figure7.add_subplot(111)

# canvas1 = tkagg.FigureCanvasTkAgg(figure3, master=right_section)
# canvas1.get_tk_widget().grid(row=0, column=0, padx=10, pady=10)

# This part of the code schedules the graphs to be updated at global variable FREQUENCY.
def schedule_graph_update(subplot, title, unit, rowname, start, end, gap):
    global START_ROW
    global LOG_ON
    update_graph(subplot, title, unit, rowname, start, end, gap, START_ROW)
    START_ROW += 1
    logger.info("Start Row: %s", START_ROW)
    if LOG_ON == 1:
        print(START_ROW)
    app.after(FREQUENCY, lambda: schedule_graph_update(subplot, title, unit, rowname, start, end, gap))  # Update every 1 second (1000 milliseconds)

update_lists()

# super Right Section: This contains the settings of the main page of the GUI. This contains a dropdown menu to change the frequency of updating the graph.
def change_graph(selection):
    logger.info("Selected graph: %s", selection)
    print("Selected graph:", selection)
    if selection == "AQI":
        canvas1 = tkagg.FigureCanvasTkAgg(figure1, master=right_section)
        canvas1.get_tk_widget().grid(row=0, column=0, padx=10, pady=10)
        schedule_graph_update(subplot1, "AQI", "", "aqi", 0, 500, 100)
    elif selection == "Temperature":
        canvas1 = tkagg.FigureCanvasTkAgg(figure2, master=right_section)
        canvas1.get_tk_widget().grid(row=0, column=0, padx=10, pady=10)
        schedule_graph_update(subplot2, "Temperature (°C)", "Celcius", "temperature", -5, 55, 10)
    elif selection == "Humidity":
        canvas1 = tkagg.FigureCanvasTkAgg(figure3, master=right_section)
        canvas1.get_tk_widget().grid(row=0, column=0, padx=10, pady=10)
        schedule_graph_update(subplot3, "Humidity", "liter", "humidity", 0, 100, 20)
    elif selection == "Vehicle Velocity":
        canvas1 = tkagg.FigureCanvasTkAgg(figure4, master=right_section)
        canvas1.get_tk_widget().grid(row=0, column=0, padx=10, pady=10)
        schedule_graph_update(subplot4, "Vehicle Velocity (kmph):", "liter", "vehicleVelocity", 0, 100, 20)
    elif selection == "Relative Velocity":
        canvas1 = tkagg.FigureCanvasTkAgg(figure5, master=right_section)
        canvas1.get_tk_widget().grid(row=0, column=0, padx=10, pady=10)
        schedule_graph_update(subplot5, "Relative Velocity (kmph)", "liter", "relativeVelocity", 0, 180, 36)
    elif selection == "Wind Velocity":
        canvas1 = tkagg.FigureCanvasTkAgg(figure6, master=right_section)
        canvas1.get_tk_widget().grid(row=0, column=0, padx=10, pady=10)
        schedule_graph_update(subplot6, "Wind Velocity (kmph)", "liter", "windVelocity", 0, 70, 14)
    elif selection == "Pressure":
        canvas1 = tkagg.FigureCanvasTkAgg(figure7, master=right_section)
        canvas1.get_tk_widget().grid(row=0, column=0, padx=10, pady=10)
        schedule_graph_update(subplot7, "Pressure (hPa)", "liter", "pressure", 300, 1100, 160)

def change_frequency(selection):
    global FREQUENCY
    if selection == "1 second":
        FREQUENCY = 1000
    elif selection == "10 seconds":
        FREQUENCY = 10000
    elif selection == "30 seconds":
        FREQUENCY = 30000
    elif selection == "1 minute":
        FREQUENCY = 60000
    elif selection == "5 minute":
        FREQUENCY = 30000
    elif selection == "10 minute":
        FREQUENCY = 600000
    logger.info(FREQUENCY)

super_right_section = customtkinter.CTkFrame(master=grid_frame)
super_right_section.grid(row=0, column=2, padx=10, pady=20)

label_frequency = customtkinter.CTkLabel(master=super_right_section, text="Frequency:", font=("Courier", 18, "bold"))
label_frequency.grid(row=0, column=0, padx=10, pady=(10, 0))

frequency_var = customtkinter.StringVar(value="1 second")
frequency = customtkinter.CTkOptionMenu(master=super_right_section,
                         values=["1 second", "10 seconds", "30 seconds", "1 minute", "5 minutes", "10 minutes"],
                         variable=frequency_var,
                         command=change_frequency)
frequency.grid(row=1, column=0, padx=10, pady=10)

label_graph = customtkinter.CTkLabel(master=super_right_section, text="Graph:", font=("Courier", 18, "bold"))
label_graph.grid(row=2, column=0, padx=10, pady=(10, 0))

graph_var = customtkinter.StringVar(value="AQI")
graph = customtkinter.CTkOptionMenu(master=super_right_section, values=["AQI", "Temperature", "Humidity", "Pressure", "Relative Velocity", "Vehicle Velocity", "Wind Velocity"], variable=graph_var, command=change_graph)
graph.grid(row=3, column=0, padx=10, pady=10)

change_graph("AQI") # By default, the AQI graph is visible.

#notifications
my_frame = customtkinter.CTkScrollableFrame(master=tabview.tab("Notifications"), width=500, height=600)
my_frame.grid(row=0, column=0, padx=20, pady=0)

# This controls the notifications page of the GUI.
def update_messages():
    global RECEIVED_MESSAGES
    for i in range(len(RECEIVED_MESSAGES)):
        frame = customtkinter.CTkFrame(master=my_frame, width=500, height=600)
        frame.grid(row=i, column=0, padx=50, pady=10)

        sub_frame1 = customtkinter.CTkFrame(master=frame, width=500, height=33, fg_color='blue', bg_color='blue')
        sub_frame1.grid(row=0, column=0, sticky="nsew", padx=20, pady=10)

        label1 = customtkinter.CTkLabel(master=sub_frame1, font=("Arial", 20), text=RECEIVED_MESSAGES[i][0])
        label1.pack(fill="both", expand=True, padx=50, anchor='center')

        sub_frame2 = customtkinter.CTkFrame(master=frame, width=500, height=33)
        sub_frame2.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)

        if RECEIVED_MESSAGES[i][1] == "emergencystop":
            title = "Emergency Stop Request at "
        elif RECEIVED_MESSAGES[i][1] == "fanspeedchange":
            title = "Fan Speed Changed to: "
        elif RECEIVED_MESSAGES[i][1] == "changespeed":
            title = "Wind Speed Changed to: "
        elif RECEIVED_MESSAGES[i][1] == "restart":
            title = "restart request recieved: "
        elif RECEIVED_MESSAGES[i][1] == "process_start":
            title = "Process started: "
        elif RECEIVED_MESSAGES[i][1] == "process_end":
            title = "Process ended: "

        label2 = customtkinter.CTkLabel(master=sub_frame2, font=("Courier", 18), text=title)
        label2.pack(fill="both", expand=True, padx=50, anchor='center')

        sub_frame3 = customtkinter.CTkFrame(master=frame, width=500, height=34)
        sub_frame3.grid(row=2, column=0, sticky="nsew", padx=20, pady=10)

        label3 = customtkinter.CTkLabel(master=sub_frame3, font=("Courier", 18), text=RECEIVED_MESSAGES[i][2])
        label3.pack(fill="both", expand=True, padx=50, anchor='center')

        # Align subframes to the center
        sub_frame1.grid_columnconfigure(0, weight=1)
        sub_frame1.grid_rowconfigure(0, weight=1)

        sub_frame2.grid_columnconfigure(0, weight=1)
        sub_frame2.grid_rowconfigure(0, weight=1)

        sub_frame3.grid_columnconfigure(0, weight=1)
        sub_frame3.grid_rowconfigure(0, weight=1)

update_messages()

# This function fetches the latest message if is freshly uploaded to the database.
def run_receive_message():
    global LAST_NOTIFICATION_TIMESTAMP
    global RECEIVED_MESSAGES
    global LOG_ON

    message = receive_message()
    logger.info("Messages: %s", RECEIVED_MESSAGES)
    if LOG_ON == 1:
        print("notiflist", RECEIVED_MESSAGES)

    if message is not  None:
        pass
    if message is None or message[0] != LAST_NOTIFICATION_TIMESTAMP:
        LAST_NOTIFICATION_TIMESTAMP = message[0]
        RECEIVED_MESSAGES.insert(0, message)
        update_messages()
        # show_custom_messagebox("Message sent", "323")
        logger.info("Messages: %s", RECEIVED_MESSAGES)
        if LOG_ON == 1:
            print("notiflist", RECEIVED_MESSAGES)

    app.after(FREQUENCY, run_receive_message)

# Call the function initially to start the process
run_receive_message()

def update_data():
    update_statistics()
    app.after(FREQUENCY, update_data)

update_data()
app.mainloop()
