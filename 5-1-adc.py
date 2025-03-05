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

    start = time.time()

    for value in range(256):
        GPIO.output(dac, dec2bin(value))
        time.sleep(0.05)
        compValue = GPIO.input(comp)

        if compValue == 1:
            ctime = time.time() - start
            return [value, ctime]
    
    ctime = time.time() - start
    return [256, ctime]




try:
    while True:
        results = adc()
        voltage = results[0] * 3.3 / 256

        print(voltage, results[1])
finally:
    GPIO.output(dac, 0)
    GPIO.output(troyk, 0)
    GPIO.cleanup()