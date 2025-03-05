import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

dac = [8, 11, 7, 1, 0, 5, 12, 6]
comp = 14
troyk = 13

GPIO.setup(dac, GPIO.OUT, initial = 0)
GPIO.setup(comp, GPIO.IN)
GPIO.setup(troyk, GPIO.OUT, initial=1)


def dec2bin(num):
    return [int(bn) for bn in bin(num)[2:].zfill(8)]


def adc():
    result = 0
    check = [0 for i in range(8)]
    start = time.time()

    check[0] = 1
    GPIO.output(dac, check)
    time.sleep(0.01)
    if GPIO.input(comp) == 0:
        result += 128
    else:
        check[0] = 0

    check[1] = 1
    GPIO.output(dac, check)
    time.sleep(0.01)
    if GPIO.input(comp) == 0:
        result += 64
    else:
        check[1] = 0
    
    check[2] = 1
    GPIO.output(dac, check)
    time.sleep(0.01)
    if GPIO.input(comp) == 0:
        result += 32
    else:
        check[2] = 0
    
    check[3] = 1
    GPIO.output(dac, check)
    time.sleep(0.01)
    if GPIO.input(comp) == 0:
        result += 16
    else:
        check[3] = 0
    
    check[4] = 1
    GPIO.output(dac, check)
    time.sleep(0.01)
    if GPIO.input(comp) == 0:
        result += 8
    else:
        check[4] = 0
    
    check[5] = 1
    GPIO.output(dac, check)
    time.sleep(0.01)
    if GPIO.input(comp) == 0:
        result += 4
    else:
        check[5] = 0

    check[6] = 1
    GPIO.output(dac, check)
    time.sleep(0.01)
    if GPIO.input(comp) == 0:
        result += 2
    else:
        check[6] = 0
    
    check[7] = 1
    GPIO.output(dac, check)
    time.sleep(0.01)
    if GPIO.input(comp) == 0:
        result += 1
    else:
        check[7] = 0

    ctime = time.time() - start
    return [result, ctime]



try:
    while True: 
        results = adc()
        voltage = results[0] * 3.3 / 256
        print(voltage, results[1])

finally:
    GPIO.output(dac, 0)
    GPIO.output(troyk, 0)
    GPIO.cleanup()
