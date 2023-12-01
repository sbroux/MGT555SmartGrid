import simpy
import serial
import time
import random

def send_data_to_arduino(ser, data):
    ser.write(data.encode())
    time.sleep(0.1)

def check_and_charge(env, room1_capacity, room2_capacity, room2_soc, arduino_serial):
    while True:
        # Check the SOC of room2
        if room2_soc < 20:
            # If room2 SOC is under 20%, use grid energy to charge room1
            grid_energy = random.randint(10, 20)  # Simulated grid energy (10-20 units)
            room1_capacity += grid_energy
            print(f"Charging room1 with {grid_energy} units of grid energy.")

            # Update the SOC of room2
            room2_soc += grid_energy

            # Send data to Arduino about room1 and room2 status
            data_to_send = f"Room1 SOC: {room1_capacity}, Room2 SOC: {room2_soc}"
            send_data_to_arduino(arduino_serial, data_to_send)

        # Your other charge-related logic goes here

        # Simulate the passage of time for charge checking
        yield env.timeout(0.2)  # Adjust the timeout as needed

def simulation(env, room1_capacity, room2_capacity, room2_soc, arduino_serial):
    while True:
        # Your main simulation logic goes here

        # Simulate the passage of time for the main simulation
        yield env.timeout(0.1)  # Adjust the timeout as needed

# Main function
def main():
    arduino_port = 'COM4'
    arduino_serial = serial.Serial(arduino_port, 9600, timeout=1)
    time.sleep(2)

    env = simpy.rt.RealtimeEnvironment(factor=0.1, strict=False)

    # Initial capacities and SOC values
    room1_capacity = 100
    room2_capacity = 100
    room2_soc = room2_capacity

    # Start the charge checking process
    env.process(check_and_charge(env, room1_capacity, room2_capacity, room2_soc, arduino_serial))

    # Start the main simulation process
    env.process(simulation(env, room1_capacity, room2_capacity, room2_soc, arduino_serial))

    env.run(until=10)

    arduino_serial.close()

if __name__ == "__main__":
    main()
