from machine import Pin, PWM
from time import sleep_ms

# Power on wait time for sensor
power_pin = Pin(25, Pin.OUT)
power_pin.value(0)

# power LED pin
power_pin.value(1)

# PWM Pin
pwm_pin = Pin(28)

servo = PWM(pwm_pin)
servo.freq(50)
duty_base = 65535/20

def rotate_servo(deg):
    duty = 1.45+0.0105*deg
    servo.duty_u16(int(duty_base * duty))

try:
    while True:
        rotate_servo(0)
        sleep_ms(1000)
        rotate_servo(85)
        sleep_ms(1000)
        rotate_servo(0)
        sleep_ms(1000)
        rotate_servo(-85)
        sleep_ms(1000)

except KeyboardInterrupt:
    print('finish')
