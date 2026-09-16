from machine import Pin, PWM
import time

# Pin
scan = Pin(15, Pin.IN, Pin.PULL_UP)
pwm = PWM(Pin(16))
pwm.freq(38000)

wait = 40000

def current():
    return time.ticks_us()

def scanSignal():
    buffer = [0]*1024
    current_time = 0.0
    current_state = 0
    last_state = 0
    offset = 0
    
    last_state = scan.value()
    
    print("scanning start")
    while True:
        current_time = current()
        if offset and time.ticks_diff(current_time, buffer[offset - 1]) > wait:
            break

        current_state = scan.value()
        if current_state != last_state:
            buffer[offset] = current_time
            offset += 1
            last_state = current_state
            
        if offset >= len(buffer):
            break

    print("Scanning end")

    data = []
    for i in range(1, offset):
        data_n = time.ticks_diff(buffer[i], buffer[i-1])
        data.append(data_n)
    
    print(data)
        
while True:
    scanSignal()
    