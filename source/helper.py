from datetime import datetime, timedelta
import serial
import time
import pandas as pd

time_scaling_factor = 3600 / 10
start_time = pd.Timestamp("2023-12-01 00:00:00")
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

# To use when everything works
electricity_price = pd.read_csv("data/electricity_price.csv")  # in euro/kWh

# Define constants based on assumptions
energy_price_grid = 11  # in ct/kW


def charge_vehicle(
    current_time,
    energy_price_grid,
    swapping_room_slots,
    number_of_battery_charged,
    stockage_room_level,
    vehicle_battery_capacity,
    charging_time,
    energy_cost,
):
    """
    We charge the vehicle :
    Two cases :
        (1) We charge the vehicle with the swapping batteries in room1
        (2) We charge the vehicle with the chargers in the parking
    return :
    """
    if number_of_battery_charged > 0:
        for i in range(swapping_room_slots):
            if swapping_room_slots[i] == 1:
                swapping_room_slots[i] = 0
                number_of_battery_charged -= 1
                # swap batteries
                print("charging with swapping room")
                break
    else:
        charge_vehicle_with_chargers(
            current_time,
            energy_price_grid,
            stockage_room_level,
            vehicle_battery_capacity,
            charging_time,
            energy_cost,
        )
        print("charging with chargers")
    return swapping_room_slots, number_of_battery_charged


def charge_vehicle_with_chargers(
    current_time,
    energy_price_grid,
    stockage_room_level,
    vehicle_battery_capacity,
    charging_time,
    energy_cost,
):
    """
    We charge the vehicle with the chargers in the parking:
    Two cases :
        (1) We charge the vehicle with the stockage room (room2) depending on the battery level of room2
        (2) We charge the vehicle with the grid and we pay the energy price

    return : energy trajectory"""

    if stockage_room_level >= 100 / 9:
        yield current_time.timeout(charging_time)
        stockage_room_level -= 100 / 9
        print(
            "charing with chargers + room2 , current room2 level: ", stockage_room_level
        )
        return room2_chargers
    else:
        yield current_time.timeout(charging_time)
        energy_cost += energy_price_grid * vehicle_battery_capacity / 100
        print("charing with chargers + grid , current energy cost: ", energy_cost)
        return grid_chargers


def charge_stockage_room_with_solar_pannel(
    current_time, solar_pannel_power, stockage_room_level
):
    """
    We charge the stockage room with the solar pannel
    """
    # yield current_time.timeout(1)
    stockage_room_level += solar_pannel_power
    print("charging with solar pannel, current room2 level: ", stockage_room_level)
    return stockage_room_level


def charge_stockage_room_with_grid(
    current_time, energy_price_grid, stockage_room_level, energy_cost
):
    """
    We charge the stockage room with the grid
    energy cost is incremented
    """
    # yield current_time.timeout(1)

    stockage_room_level += 100 / 9
    print("charging with grid, current room2 level: ", stockage_room_level)
    return stockage_room_level


def decision_making(
    env,
    vehicle_arrival_data,
    swapping_room_slots,
    number_of_battery_charged,
    stockage_room_level,
    energy_price_grid,
    vehicle_battery_capacity,
    charging_time,
    energy_cost,
    solar_pannel_power,
):
    # Define initial battery levels and constraints

    while env.now:
        threshold = 10

        if solar_pannel_power > threshold:
            stockage_room_level = charge_stockage_room_with_solar_pannel(
                env, solar_pannel_power
            )
        else:
            stockage_room_level, energy_cost = charge_stockage_room_with_grid(
                env, energy_price_grid, stockage_room_level, energy_cost
            )

        if stockage_room_level > threshold:
            (
                number_of_battery_charged,
                swapping_room_slots,
            ) = charge_swapping_with_stockage(
                env, number_of_battery_charged, swapping_room_slots, stockage_room_level
            )
        else:
            number_of_battery_charged, swapping_room_slots = charge_swapping_with_grid(
                env,
                number_of_battery_charged,
                swapping_room_slots,
                energy_price_grid,
                stockage_room_level,
            )

        sim_time_datetime = datetime.utcfromtimestamp(env.now)
        if sim_time_datetime.minute % 30 == 0 and sim_time_datetime.second == 0:
            print("env.now", sim_time_datetime)
            for index, row in vehicle_arrival_data.iterrows():
                vehicle_id = row["Vehicle_ID"]
                arrival_time = row["Date Time"]

                arrival_time = datetime.strptime(arrival_time, "%Y-%m-%d %H:%M:%S")
                # print("sim_time_datetime", sim_time_datetime)
                if arrival_time == sim_time_datetime:
                    print("arrival time", arrival_time)
                    print("current time", sim_time_datetime)
                    # Compare the arrival time in the dataset with the current simulation time
                    charge_vehicle(
                        env,
                        energy_price_grid,
                        swapping_room_slots,
                        number_of_battery_charged,
                        stockage_room_level,
                        vehicle_battery_capacity,
                        charging_time,
                        energy_cost,
                    )
                    print("charging vehicle", vehicle_id)
