import serial
import time


# comport = "/dev/tty.usbserial-1110"  # change with the port u are using
# arduino = serial.Serial(comport, 9600)
# time.sleep(2)
"""
We may add the constants here and do the decision in this section
"""
# Defintion of constants
grid_room1 = "gR1"
room2_room1 = "R2R1"
grid_room2 = "gR2"
room2_grid = "R2g"
solar_room2 = "SR2"
room2_chargers = "R2C"
chargers_grid = "CR2g"
grid_chargers = "gCR2"

energy_price_grid = 0.2  # in euro/kWh


def charge_vehicle(
    current_time,
    total_room1_battery_level,
    room1_battery_level,
    room2_battery_level,
    vehicle_battery_level,
    energy_price_grid,
):
    """
    We charge the vehicle :
    Two cases :
        (1) We charge the vehicle with the swapping batteries in room1
        (2) We charge the vehicle with the chargers in the parking
    return : room1_battery_level, room2_battery_level, energy_cost
    """
    if room1_battery_level < 0.1 * total_room1_battery_level:
        _, room2_battery_level, energy_cost = charge_vehicle_with_chargers(
            current_time, room2_battery_level, vehicle_battery_level, energy_price_grid
        )
        print("charging with chargers")
    else:
        energy_cost = 0
        room1_battery_level = swap_batteries(
            current_time, room1_battery_level, vehicle_battery_level
        )
        print("charging with swapping room")
    return room1_battery_level, room2_battery_level, energy_cost


def charge_room1(
    current_time,
    room1_battery_level,
    total_room1_battery_level,
    room2_battery_level,
    energy_price_grid,
):
    """
    We charge the swapping batteries in room1 :
    Two cases :
        (1) We charge the swapping batteries with the stockage room (room2) depending on the battery level of room2
        (2) We charge the swapping batteries with the grid and we pay the energy price

    The threshold for the battery level in room2 is 30%

    return : energy trajectory, room1_battery_level, room2_battery_level, energy_cost
    """
    energy_cost = 0
    if room2_battery_level > 30:
        room1_battery_level_empty = total_room1_battery_level - room1_battery_level
        for i in range(room1_battery_level_empty):
            room1_battery_level += (
                1  # add the charging time for the simulation in real time
            )
            room2_battery_level -= 1

        return room2_room1, room1_battery_level, room2_battery_level, energy_cost
    else:
        room1_battery_level_empty = total_room1_battery_level - room1_battery_level
        for i in range(room1_battery_level_empty):
            room1_battery_level += 1
            energy_cost += energy_price_grid / 1000
        return (
            grid_room1,
            room1_battery_level,
            room2_battery_level,
            energy_cost,
        )  # 1 is the power of the battery


def charge_room2(
    current_time,
    room2_battery_level,
    total_room2_battery_level,
    solar_panel_power,
    energy_price_grid,
):
    """
    We charge the stocakge room (room2) :
    Two cases :
        (1) We charge the stockage room with the solar panels
        (2) We charge the stockage room with the grid and we pay the energy price

    return : energy trajectory, room2_battery_level, energy_cost"""
    room2_battery_level_empty = total_room2_battery_level - room2_battery_level
    energy_cost = 0
    # this threshold should be defined
    if solar_panel_power > 0.2 * total_room2_battery_level:
        for i in range(room2_battery_level_empty):
            room2_battery_level += 1
        return solar_room2, room2_battery_level, energy_cost
    else:
        for i in range(room2_battery_level_empty):
            room2_battery_level += 1
            energy_cost += energy_price_grid / 1000
        return grid_room2, room2_battery_level, energy_cost


def charge_vehicle_with_chargers(
    current_time, room2_battery_level, vehicle_battery_level, energy_price_grid
):
    """
    We charge the vehicle with the chargers in the parking:
    Two cases :
        (1) We charge the vehicle with the stockage room (room2) depending on the battery level of room2
        (2) We charge the vehicle with the grid and we pay the energy price

    return : energy trajectory, room2_battery_level, energy_cost"""

    if room2_battery_level >= vehicle_battery_level:
        room2_battery_level -= vehicle_battery_level
        return room2_chargers, room2_battery_level, 0
    else:
        energy_cost = energy_price_grid / 1000 * vehicle_battery_level
        return grid_chargers, room2_battery_level, energy_cost


def swap_batteries(current_time, room1_battery_level, vehicle_battery_level):
    """
    We swap the battery of the vehicule with battery in room1
    thus the room1 battery level decreases by the power of the vehicle(constant)

    room1_battery_level: battery level of room1
    vehicle_battery_level: battery level of the vehicle

    return: room1_battery_level
    """
    room1_battery_level -= vehicle_battery_level
    return room1_battery_level


def decision_making(
    current_time,
    vehicle_arrival_data,
    vehicle_battery_level,
    room1_battery_level,
    room2_battery_level,
    energy_price_grid,
):
    for index, row in vehicle_arrival_data.iterrows():
        vehicle_id = row[
            "Vehicle ID"
        ]  # Replace with the actual column name for vehicle ID
        arrival_time = row[
            "Date Time"
        ]  # Replace with the actual column name for arrival time

    while True:
        # Compare the arrival time in the dataset with the current simulation time
        if arrival_time == current_time:
            charge_vehicle(
                current_time,
                room1_battery_level,
                room2_battery_level,
                vehicle_battery_level,
                energy_price_grid,
            )
            print(
                f"Making time-sensitive decisions for Vehicle {vehicle_id} at time {arrival_time} "
                f"with current simulation time {current_time}"
            )

    # Your time-sensitive decision-making algorithm goes here
    print(
        f"Making time-sensitive decisions for Vehicle {vehicle_id} at time {current_time}"
    )
