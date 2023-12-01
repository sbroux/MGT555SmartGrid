import serial
import time
from serial import Serial


# comport = "/dev/tty.usbserial-1110"  # change with the port u are using
comport = 'COM4'
arduino = serial.Serial(comport, 9600)
time.sleep(2)
i = 0
while i < 10:
    arduino.write(b"r")  # Command to turn on first LEDs in red
    # Delay for a certain duration (for example, 2 seconds)
    time.sleep(2)
    # Send command to Arduino to turn on next LEDs in blue
    arduino.write(b"b")
    time.sleep(2)
    i +=1  # Command to turn on next LEDs in blue


# Close the serial connection
arduino.close()
print("connection closed")
# Close the serial connection
