import RPi.GPIO as GPIO
import time

def decimal2binary(value):
    return [int(bit) for bit in bin(value)[2:].zfill(8)]

GPIO.setmode(GPIO.BCM)
dac = [26, 19, 13, 6, 5, 11, 9, 10]
bits = len(dac)
comp = 4
troyka = 17
levels = 2**bits
max_volt = 3.3

GPIO.setup(dac, GPIO.OUT)
GPIO.setup(comp, GPIO.IN)
GPIO.setup(troyka, GPIO.OUT, initial = GPIO.HIGH)

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


try:
    while True:
        value = adc()
        volt = value/levels * max_volt
        print("IN value = {:^3}, OUT volt = {:.2f}".format(value, volt))


finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()

