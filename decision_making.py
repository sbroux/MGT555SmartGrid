# Smart Grid Simulation
import serial
import time
import simpy
import random
import statistics
import simpy.rt


# Arrive at the station
# get in line to charge
# charge with room1
# go
class Station(object):
    def __init__(self, env):
        self.env = env
        self.charge = simpy.Resource(env, capacity=2)

    def charge():
        yield self.env.timeout(1)


def slow_proc(env):
    time.sleep(0.02)  # Heavy computation :-)
    yield env.timeout(1)


env = simpy.rt.RealtimeEnvironment(factor=0.01)
proc = env.process(slow_proc(env))
# Initialize the serial connection
comport = "/dev/tty.usbserial-1110"  # change with the port u are using
arduino = serial.Serial(comport, 9600)
time.sleep(2)
# Define the different energy trajectories
"""
(1) grid -> Room 1
(2) room2 -> room 1
(3) grid -> room2
(4) room2 -> grid
(5) Solar Panels -> Room2
(6) Room 2 -> Chargers for vehicule(Parking)
(7) Chargers for vehicule(Parking) -> grid to perform a vehicule to grid
(8) grid -> Chargers for vehicule(Parking)
"""

grid_room1 = "gR1"
room1_room2 = "R1R2"
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

i = 0
while i < simulation_time:
    arduino.write(b"r")  # Command to turn on first LEDs in red
    # Delay for a certain duration (for example, 2 seconds)
    time.sleep(2)
    # Send command to Arduino to turn on next LEDs in blue
    arduino.write(b"b")
    time.sleep(2)
    ++i  # Command to turn on next LEDs in blue


# Close the serial connection
arduino.close()
print("connection closed")
# Close the serial connection
