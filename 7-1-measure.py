import RPi.GPIO as GPIO
import time
import matplotlib.pyplot as plt
GPIO.setmode(GPIO.BCM)
dac = [8, 11, 7, 1, 0, 5, 12, 6]
leds = [2, 3, 4, 17, 27, 22, 10, 9]

# НАСТРАИВАЕМ
GPIO.setup(leds, GPIO.OUT)
GPIO.setup(dac, GPIO.OUT)
comp = 14
troyka = 13
GPIO.setup(troyka, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(comp, GPIO.IN)

def dec_bin(N):
    return [int(X) for X in bin(N)[2:].zfill(8)]   


def update_leds(x):
    b = dec_bin(int(x/3.3 * 255))
    GPIO.output(leds, b)


def adc():
    # ИНДУССКИЙ КОД
    start = time.time()
    value = 128
    GPIO.output(dac, dec_bin(value + 64))
    time.sleep(0.001)
    if GPIO.input(comp) == 0:
        value += 64
    else:
        value -= 64

    GPIO.output(dac, dec_bin(value + 32))
    time.sleep(0.001)
    if GPIO.input(comp) == 0:
        value += 32
    else:
        value -= 32

    GPIO.output(dac, dec_bin(value + 16))
    time.sleep(0.001)
    if GPIO.input(comp) == 0:
        value += 16
    else:
        value -= 16


    GPIO.output(dac, dec_bin(value + 8))
    time.sleep(0.001)
    if GPIO.input(comp) == 0:
        value += 8
    else:
        value -= 8


    GPIO.output(dac, dec_bin(value + 4))
    time.sleep(0.001)
    if GPIO.input(comp) == 0:
        value += 4
    else:
        value -= 4

    GPIO.output(dac, dec_bin(value + 2))
    time.sleep(0.001)
    if GPIO.input(comp) == 0:
        value += 2
    else:
        value -= 2

    GPIO.output(dac, dec_bin(value + 1))
    time.sleep(0.001)
    if GPIO.input(comp) == 0:
        value += 1
    else:
        value -= 1
    

    end = time.time()
    res = end - start
    return value, res

try:
    measured = []
    start = time.time()
    GPIO.output(troyka, 1)
    # иЗМЕРЯЕМ ЗАРЯДКУ
    while True:
        value, _ = adc()
        v = value * 3.3/256
        measured.append(v)
        update_leds(v)
        if v >= 0.97 * 3.3:
            break

    GPIO.output(troyka, 0)
    # ИЗМЕРЯЕМ РАЗРЯДКУ
    while True:
        value, _ = adc()
        v = value * 3.3/256
        measured.append(v)
        update_leds(v)
        if v <= 0.02 * 3.3:
            break
    

    final = time.time()
    Time = final - start
    # СТРОИМ ГРАФИК
    plt.plot(measured)
    plt.grid()
    plt.show()

    # ЗАПИСЫВАЕМ В ФАЙЛ
    with open('data.txt', 'w') as outfile:
        outfile.write('\n'.join(map(str, measured)))    
    
    
    Quant = 3.3/256
    Vd = 1/(Time/len(measured))
    a = [str(Quant), str(Vd)]
    with open('setting.txt', 'w') as outfile1:
        outfile1.write('\n'.join(a))  
    
    
    print('Общая продолжительность эксперимента: ', Time)
    print('Период: ', Time/len(measured))
    print('Частота дискретизации ', Vd)
    print('Шаг квантования ', Quant)

    


# ОБРАБОТКА ИСКЛЮЧЕНИЙ        
except KeyboardInterrupt:
            print('Stopped')


finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()