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


def decide_trajectory(room1_charge, room2_charge, solar_active, vehicle_arrival):
    if vehicle_arrival:
        if room1_charge > 10:
            room1_charge -= 10
            return "R1R2"
        else:
            if room2_charge > 0:
                return "R2C"
            else:
                return "gCR2"
    else:
        if room1_charge <= 0:
            if room2_charge > 0:
                return "R1R2"
            else:
                return "gR1"
        elif room2_charge <= 0:
            if solar_active:
                return "SR2"
            else:
                return "gR2"
    return None


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
