import RPi.GPIO as GPIO


dac = [8, 11, 7, 1, 8, 5, 12, 6]
GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT)
pin = 21
GPIO.setup(pin, GPIO.OUT)
pwm = GPIO.PWM(pin, 100)

pwm.start(0)
try:
    while True:
        num = input()
        if num.lower() == 'q':
            print('Interrupt')
            break
        try:
            cycle = float(num)
            if cycle < 0 or cycle > 100:
                print("limit")
                continue
            pwm.ChangeDutyCycle(cycle)

            u = cycle * 3.3 / 100
            print(u)
        except ValueError:   
            print('No num')
finally:
    pwm.stop()
    GPIO.cleanup()

