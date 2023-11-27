import serial
import time

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
simulation_time = 3000  # in seconds

# Define initial battery levels and constraints
room1_battery_level = 100  # Room 1 battery level in percentage
room2_battery_level = 100  # Room 2 battery level in percentage

# Define constants based on assumptions
threshold_room1_low = 10  # Threshold for low battery level in Room 1
threshold_room2_low = 10  # Threshold for low battery level in Room 2

i = 0


# Function to determine the command for Arduino based on conditions
def decide_command():
    global room1_battery_level, room2_battery_level

    if room1_battery_level > threshold_room1_low:
        return arduino.write(grid_room1)
    elif room1_battery_level <= threshold_room1_low and room2_battery_level > 0:
        return arduino.write(room1_room2)
    elif room2_battery_level <= threshold_room2_low:
        return arduino.write(room2_grid)
    else:
        return chargers_grid


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
