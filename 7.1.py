import RPi.GPIO as GPIO
import time 
from matplotlib import pyplot 
GPIO.setmode(GPIO.BCM) 

leds=[21, 20, 16, 12, 7, 8, 25, 24] 
GPIO.setup(leds, GPIO.OUT) 

dac=[26, 19, 13, 6, 5, 11, 9, 10] 
GPIO.setup(dac, GPIO.OUT, initial = GPIO.HIGH) 

comp=4 
troyka=17 
GPIO.setup(troyka, GPIO.OUT, initial = GPIO.HIGH) 
GPIO.setup(comp, GPIO.IN) 

def tobinery(x):
    return [int (element) for element in bin(x)[2:].zfill(8)]

def adc(): 
    t = 0 
    for i in range(7, -1, -1): 
        t += 2**i 
        GPIO.output(dac, tobinery(t)) 
        time.sleep(0.005) 
        if GPIO.input(comp)==0: 
            t -= 2**i 
    return t 
    
try: 
    voltage = 0 
    result_exp = [] 
    time_start = time.time() 
    point = 0 

    print('Зарядка конденсатора\n') 
    while voltage < 256*0.04: 
        voltage = adc() 
        result_exp.append(voltage) 
        print("volt={}".format(voltage))
        time.sleep(0) 
        point += 1 
        GPIO.output(leds, tobinery(voltage)) 

    GPIO.setup(troyka, GPIO.OUT, initial = GPIO.LOW)
     
    print('Разрядка конденсатора\n') 
    while voltage < 256*0.52: 
        voltage = adc() 
        result_exp.append(voltage) 
        print("vvolt={}".format(voltage))
        time.sleep(0) 
        point += 1 
        GPIO.output(leds, tobinery(voltage)) 

    GPIO.setup(troyka, GPIO.OUT, initial = GPIO.HIGH)
     
    print('Разрядка конденсатора\n') 
    while voltage > 256*0.17: 
        voltage = adc() 
        result_exp.append(voltage) 
        print("vvvolt={}".format(voltage))
        time.sleep(0) 
        point += 1 
        GPIO.output(leds, tobinery(voltage)) 

    time_exp = time.time()-time_start 
        
    print('Запись данных в файл\n') 
    with open('data.txt', 'w') as f: 
        for i in result_exp: 
            f.write(str(i) + '\n') 
    with open('settings.txt', 'w') as f: 
        f.write(str(1/time_exp/point) + '\n')
        f.write('0.01289') 
        
    print('Длительность эксперимента: {}, \nПериод измерения: {}, \nЧастота дискретизации: {}, \nШаг квантования: {}\n'.format(time_exp, time_exp/point, 1/time_exp/point, 0.013)) 
    
    print('Графики\n') 
    y=[i/256*3.3 for i in result_exp] 
    x=[i*time_exp/point for i in range(len(result_exp))] 
    pyplot.plot(x, y) 
    pyplot.show() 

finally: 
    GPIO.output(leds, 0) 
    GPIO.output(dac, 0) 
    GPIO.cleanup()