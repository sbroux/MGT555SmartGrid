from pyfirmata import Arduino

# import time


board = Arduino("/dev/tty.usbserial-1110")
print(board.get_firmata_version())
# led_1 = board.get_pin("d:8:o")  # on choisis le pin
# pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, auto_write=False)
# pixels[9] = (0, 10, 0)
# pixels[0] = (10, 0, 0)

# while True:
#     board.digital[13].write(1)
#     time.sleep(0.1)
#     board.digital[13].write(0)
#     time.sleep(0.1)
