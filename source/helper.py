from datetime import datetime, timedelta
import serial
import time
import pandas as pd
import numpy as np
import asyncio


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

MAX_CAPACITY = 500 * 9

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
        for i, slot in enumerate(swapping_room_slots):
            if slot == 1:
                swapping_room_slots[i] = 0
                number_of_battery_charged -= 1
                print("charging with swapping room")

                # (
                #     traject,
                #     stockage_room_level,
                #     number_of_battery_charged,
                #     swapping_room_slots,
                # ) = charge_swapping_room(
                #     current_time,
                #     stockage_room_level,
                #     swapping_room_slots,
                #     number_of_battery_charged,
                # )

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

    if stockage_room_level >= 100 / 9 * MAX_CAPACITY:
        stockage_room_level -= 100 / 9 * MAX_CAPACITY
        print(
            "charging with chargers + room2 , current room2 level: ",
            stockage_room_level,
        )
        return room2_chargers, stockage_room_level, energy_cost
    else:
        energy_cost += energy_price_grid * vehicle_battery_capacity / 100
        print("charging with chargers + grid , current energy cost: ", energy_cost)
        return grid_chargers, stockage_room_level, energy_cost


async def charge_stockage_room(
    env,
    solar_pannel_power,
    threshold_pannel_power,
    charging_time,
    energy_price_grid,
    stockage_room_level,
    energy_cost,
):
    """
    We charge the stockage room with the solar pannel or the grid
    return : energy trajectory, stockage_room_level, energy_cost
    """
    # yield env.timeout(1)
    if solar_pannel_power > 0:
        trajectory, stockage_room_level = await charge_stockage_room_with_solar_pannel(
            solar_pannel_power, stockage_room_level, charging_time * 9
        )
    else:
        (
            trajectory,
            stockage_room_level,
            energy_cost,
        ) = await charge_stockage_room_with_grid(
            energy_price_grid, stockage_room_level, energy_cost
        )
    return trajectory, stockage_room_level, energy_cost


def charge_swapping_room(
    env, stockage_room_level, swapping_room_slots, number_of_battery_charged
):
    """We charge the swapping room with the stockage room or the grid"""

    if stockage_room_level > 500:
        (
            traject,
            stockage_room_level,
            number_of_battery_charged,
            swapping_room_slots,
        ) = charge_swapping_with_stockage(
            env, number_of_battery_charged, swapping_room_slots, stockage_room_level
        )
        print("charging swapping room with stockage room")

    else:
        (
            traject,
            number_of_battery_charged,
            swapping_room_slots,
            energy_cost,
        ) = charge_swapping_with_grid(
            env,
            number_of_battery_charged,
            swapping_room_slots,
            energy_price_grid,
            stockage_room_level,
            energy_cost,
        )
        print("charging swapping room with grid")
    return traject, stockage_room_level, number_of_battery_charged, swapping_room_slots


async def charge_stockage_room_with_solar_pannel(
    current_time, solar_pannel_power, stockage_room_level, charging_time
):
    """
    We charge the stockage room with the solar pannel ,
      the stockage room level is incremented depending on the charging time
    """
    # yield current_time.timeout(1)
    while stockage_room_level < MAX_CAPACITY:
        stockage_room_level += solar_pannel_power * charging_time / 3600
    print("charging with solar panel, current room2 level: ", stockage_room_level)
    return solar_room2, stockage_room_level


async def charge_stockage_room_with_grid(
    current_time, energy_price_grid, stockage_room_level, energy_cost
):
    """
    We charge the stockage room with the grid
    energy cost is incremented
    """
    # yield current_time.timeout(1)
    if stockage_room_level >= MAX_CAPACITY:
        return "No", stockage_room_level, energy_cost
    else:
        while stockage_room_level < MAX_CAPACITY:
            if energy_price_grid < 15:
                energy_cost += energy_price_grid / 100 * MAX_CAPACITY / 9
                stockage_room_level += 100 / 9
        print("Charging with grid. Current room level:", stockage_room_level)
        return "grid_room2", stockage_room_level, energy_cost


async def charge_swapping_with_stockage(
    env, number_of_battery_charged, swapping_room_slots, stockage_room_level
):
    """
    We charge the swapping room with the stockage room
    return : trajectory, swapping_room_slots, number_of_battery_charged, stockage_room_level
    """
    # yield env.timeout(1)

    if number_of_battery_charged < 9:
        number_of_battery_charged += 1
        swapping_room_slots[number_of_battery_charged] = 1
        stockage_room_level -= 100 / 9
        print(
            "charging swapping room with stockage room, current swapping room level: ",
            swapping_room_slots,
        )
        charge_stockage_room(
            env,
            stockage_room_level,
            swapping_room_slots,
            number_of_battery_charged,
        )
        return (
            room2_room1,
            stockage_room_level,
            number_of_battery_charged,
            swapping_room_slots,
        )
    else:
        print("No need to charge the swapping room with the stockage room")
        return "No", stockage_room_level, number_of_battery_charged, swapping_room_slots


def charge_swapping_with_grid(
    env,
    number_of_battery_charged,
    swapping_room_slots,
    energy_price_grid,
    stockage_room_level,
    energy_cost,
):
    """
    We charge the swapping room with the grid"""

    # yield env.timeout(1)
    while number_of_battery_charged < 9:
        energy_cost += energy_price_grid * 100 / 9
        number_of_battery_charged += 1
        swapping_room_slots[number_of_battery_charged] = 1
    print(
        "charging swapping room with grid, current swapping room level: ",
        swapping_room_slots,
    )
    return grid_room1, stockage_room_level, number_of_battery_charged, energy_cost


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
    arduino,
):
    # Define initial battery levels and constraints
    # prendre la valeur dnans le data frame au temps current et check si ya solar energy

    sim_time_datetime = datetime.utcfromtimestamp(env.now)
    if sim_time_datetime.minute % 30 == 0 and sim_time_datetime.second == 0:
        print("env.now", sim_time_datetime)
        arriving_vehicles = vehicle_arrival_data[
            vehicle_arrival_data["Date Time"]
            == sim_time_datetime.strftime("%Y-%m-%d %H:%M:%S")
        ]
        # if arriving_vehicles.empty:
        #     if stockage_room_level < 500 * 9 * 0.8:
        #         # Call the function to charge the storage room
        #         # Replace 'charge_storage_room' with the actual function name
        #         traject, stockage_room_level, energy_cost = charge_stockage_room(
        #             env,
        #             solar_pannel_power,
        #             100,
        #             charging_time,
        #             energy_price_grid,
        #             stockage_room_level,
        #             energy_cost,
        #         )

        #     elif number_of_battery_charged < 9:
        #         (
        #             traject,
        #             stockage_room_level,
        #             number_of_battery_charged,
        #             swapping_room_slots,
        #         ) = charge_swapping_room(
        #             env,
        #             stockage_room_level,
        #             swapping_room_slots,
        #             number_of_battery_charged,
        #         )
        #     else:
        #         None
        # else:
        arduino.write(grid_room1.encode("ascii"))
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
                arduino.write(grid_room1.encode("ascii"))
                print("charging vehicle", vehicle_id)
