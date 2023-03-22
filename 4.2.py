import RPi.GPIO as GPIO
import time

def decimal2binary(value):
    return [int(bit) for bit in bin(value)[2:].zfill(8)]

GPIO.setmode(GPIO.BCM)
dac = [26, 19, 13, 6, 5, 11, 9, 10]
GPIO.setup(dac, GPIO.OUT)

try:
    while True:
        per = input("введите период: ")
        if not per.isdigit():
            print("не число")
        else:
            period = int(per)/(256*2)
            for i in range(256):                #заполнение
                GPIO.output(dac, decimal2binary(i))
                time.sleep(period)
            for i in range(255, -1, -1):        #очищение
                GPIO.output(dac, decimal2binary(i))
                time.sleep(period)

finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()