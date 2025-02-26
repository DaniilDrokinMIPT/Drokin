import RPi.GPIO as GPIO
import time


dac = [8, 11, 7, 1, 8, 5, 12, 6]
GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT)


def dec2bin(val):
    return [int(x) for x in bin(val)[2:].zfill(8)]


try:
    p = float(input('Enter interval'))

    while True:
        for num in range(256):
            num2 = dec2bin(num)
            GPIO.output(dac, num2)
            time.sleep(p / 512)
        for num in range(255, -1, -1):
            num2 = dec2bin(num)
            GPIO.output(dac, num2)
            time.sleep(p / 512)
        
finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()
