"""
We may add the constants here and do the decision in this section
"""


def swap_batteries(room1_battery_level, vehicle_battery_level):
    """
    We swap the battery of the vehicule with battery in room1
    thus the room1 battery level decreases by the power of the vehicle(constant)

    room1_battery_level: battery level of room1
    vehicle_battery_level: battery level of the vehicle

    return: room1_battery_level
    """
    room1_battery_level -= vehicle_battery_level
    return room1_battery_level


def charge_with_room2(room2_battery_level, vehicle_battery_level):
    """
    We charge the vehicle with the battery in room2 by using the parking chargers
    thus the room2 battery level decreases by the power of the vehicle(constant)

    room2_battery_level: battery level of room2
    vehicle_battery_level: battery level of the vehicle

    return: room2_battery_level
    """
    room2_battery_level -= vehicle_battery_level
    return room2_battery_level
