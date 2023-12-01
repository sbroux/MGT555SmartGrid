# Smart Grid Simulation
import serial
import time
import simpy
import simpy.rt
import pandas as pd
from helper import *

# Initialize the serial connection
# comport = "/dev/tty.usbserial-1110"  # change with the port u are using
# arduino = serial.Serial(comport, 9600)
# time.sleep(2)

# Define the different energy trajectories as constants
grid_room1 = "gR1"
room1_room2 = "R2R1"
grid_room2 = "gR2"
room2_grid = "R2g"
solar_room2 = "SR2"
room2_chargers = "R2C"
chargers_grid = "CR2g"
grid_chargers = "gCR2"

# Define the time of the simulation
simulation_time = 3600  # in seconds
# Define initial battery levels and constraints
room1_battery_level = 100  # Room 1 battery level in percentage
room2_battery_level = 100  # Room 2 battery level in percentage
# Define constants based on assumptions
threshold_room1_low = 10  # Threshold for low battery level in Room 1
threshold_room2_low = 10  # Threshold for low battery level in Room 2
# Vehicle battery level
vehicle_battery_level = 10  # Vehicle battery level in percentage
# Energy price as a constant per hour
energy_price_grid = 0.2  # in euro/kWh

i = 0

# read vehicul arrival data
file_path = "data/vehicle_arrival.csv"
df_vehicle = pd.read_csv(file_path)
time_scaling_factor = 1 / 1200
start_time = pd.Timestamp("2023-12-01 00:00:00")
# Initialize the simulation environment with the specified start time
env = simpy.rt.RealtimeEnvironment(
    initial_time=start_time.timestamp(), factor=time_scaling_factor
)


def my_simulation():
    print(f"Simulation time: {env.now}")
    yield env.timeout(3 * time_scaling_factor)  # 3 seconds in real life
    print(f"Simulation time after timeout: {env.now}")
    # 30 seconds in real life
    decision_making(
        env.now,
        df_vehicle,
        vehicle_battery_level,
        room1_battery_level,
        room2_battery_level,
        energy_price_grid,
    )
    # Start the simulation with all the battery fully charged


simulation_duration = env.now + 86400 * time_scaling_factor
env.process(my_simulation())  # Run the simulation for a full day
env.run(
    until=simulation_duration
)  # 48 hours in simulation time where 1 hour = 30 seconds


# Close the serial connection
# arduino.close()
# print("connection closed")
# Close the serial connection
