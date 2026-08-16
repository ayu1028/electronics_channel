from machine import Pin
import time

# Pin
button = Pin(11, Pin.IN, Pin.PULL_UP)

wait = 4e4

def current():
    return time.ticks_us()

def scanSignal():
    buffer = [0.0]*1024
    current_time = 0.0
    current_state = 0
    last_state = 0
    offset = 0
    
    last_state = button.value()
    
    print("scanning start")
    while True:
        current_time = current()
        if offset and current_time > buffer[offset - 1] + wait:
            break

        current_state = button.value()
        if current_state != last_state:
            buffer[offset] = current_time
            offset += 1
            last_state = current_state
            last_time = current()

    print("Scanning end")

    data = []
    for i in range(1, offset):
        data_n = int(buffer[i] - buffer[i - 1])
        data.append(data_n)
    
    print(data)
        
while True:
    scanSignal()
    