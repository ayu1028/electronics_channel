from machine import Pin
from time import sleep_ms

# For Raspberry pi pico/pico2
LED_pin = Pin(25, Pin.OUT)

# For Raspberry pi pico W/2W
# LED_pin = Pin("LED", Pin.OUT)

while True:
    LED_pin.toggle()
    sleep_ms(500)
    