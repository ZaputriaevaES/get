import RPi.GPIO as GPIO
import time

def decimal2binary(value):
    return [int(bit) for bit in bin(value)[2:].zfill(8)]

GPIO.setmode(GPIO.BCM)
dac = [26, 19, 13, 6, 5, 11, 9, 10]
leds = [21, 20, 16, 12, 7, 8, 25, 24]
bits = len(dac)
comp = 4
troyka = 17
levels = 2**bits
max_volt = 3.3

GPIO.setup(dac, GPIO.OUT)
GPIO.setup(comp, GPIO.IN)
GPIO.setup(troyka, GPIO.OUT, initial = GPIO.HIGH)
GPIO.setup(leds, GPIO.OUT)

def adc():
    value = 0
    for i in range(7, -1, -1):  #7, 6, 5, 4, 3, 2, 1, 0
        value += 2**i
        signal = decimal2binary(value)
        GPIO.output(dac, signal)
        time.sleep(0.01)
        comp_value = GPIO.input(comp)
        if comp_value == 0: value -= 2**i
    return value


def volume(value):
    if value == 0: GPIO.output(leds, decimal2binary(0))
    elif 0 < value & value < 27: GPIO.output(leds, decimal2binary(1))
    elif 27 <= value & value < 54: GPIO.output(leds, decimal2binary(3))
    elif 54 <= value & value < 81: GPIO.output(leds, decimal2binary(7))
    elif 81 <= value & value < 108: GPIO.output(leds, decimal2binary(15))
    elif 108 <= value & value < 135: GPIO.output(leds, decimal2binary(31))
    elif 135 <= value & value < 162: GPIO.output(leds, decimal2binary(63))
    elif 162 <= value & value < 189: GPIO.output(leds, decimal2binary(127))
    else: GPIO.output(leds, 255)

try:
    while True:
        value = adc()
        #signal = decimal2binary(value)
        #GPIO.output(leds, signal)
        volume(value)
        volt = value/levels * max_volt
        print("IN value = {:^3}, OUT volt = {:.2f}".format(value, volt))


finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()

