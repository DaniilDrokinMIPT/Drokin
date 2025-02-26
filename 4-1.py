import RPi.GPIO as GPIO


dac = [8, 11, 7, 1, 8, 5, 12, 6]
GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT)
GPIO.output(dac, 0)


def dec2bin(val):
    return [int(x) for x in bin(val)[2:].zfill(8)]


try:
    while True:
        num = input('введите целое число')
        if num == 'q':
            print("Interrupt")
            break
        try:
            if int(num) < 0:
                print("Negative")
            elif int(num) > 255:
                print("Limit")
            elif '.' in num:
                print("It is float")
            else:
                num2 = dec2bin(int(num))
                GPIO.output(dac, num2)
                u = num2 * 3.3 / 255
                print(u)
        except ValueError:
            print('No num')
finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()
