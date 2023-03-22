import RPi.GPIO as GPIO


def decimal2binary(value):
    return [int(bit) for bit in bin(value)[2:].zfill(8)]

GPIO.setmode(GPIO.BCM)
dac = [26, 19, 13, 6, 5, 11, 9, 10]
GPIO.setup(dac, GPIO.OUT)

try:
    num = input("введите число 0...255\n")
    while num != 'q':
        if not num.isdigit():
            print("не число")
        elif int(num) < 0:
            print("меньше 0")
        elif int(num) > 255:
            print("больше 255")
        elif int(num) % 1 != 0:
            print("не целое")
            
        else:
            binary = decimal2binary(int(num))
            print(bin)
            GPIO.output(dac, binary)
            print("напряжение: {:.4f}".format(int(num)/256*3.3))
        num = input("введите число 0...255\n")

finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()

