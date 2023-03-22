import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
dac = [26, 19, 13, 6, 5, 11, 9, 10]
GPIO.setup(dac, GPIO.OUT, initial = GPIO.HIGH)
GPIO.setup(22, GPIO.OUT)

pwm = GPIO.PWM(22, 1000)     #частота
pwm.start(0)

try:
    while True:
        duty_cycle = int(input())
        pwm.ChangeDutyCycle(duty_cycle) 
        print("{:.2f}".format(duty_cycle*(3.3/100)))

finally:
    GPIO.output(dac, 0)
    GPIO.output(22, 0)
    GPIO.cleanup() 