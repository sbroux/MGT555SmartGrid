import pyfirmata

comport = "COM3" # change with the port u are using

board = pyfirmata.Arduino(comport)

#Reçoit en input un tableau binaire, 
# 0 ou 1 pour dire si une led strip/ indicateur Leds est allumé ou pas. Output, illumine les Leds.

led_1 = board.get_pin("d:8:o") # on choisis le pin


def led(light):
    if light == [0]:
        led_1.write(1)

    elif light == [1]:
       led_1.write(0)