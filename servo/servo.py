from machine import Pin, PWM
from time import sleep_ms

# ピン割り当て
pwm_pin = Pin(28)

# パラメータ設定
period = 20 #ms
min_pulse = 0.5 #ms pulse @ −90 deg
max_pulse = 2.4 #ms pulse @ +90 deg

# サーボモータ定義
servo = PWM(pwm_pin)
servo.freq(1/period*1000)
duty_base = 65535/period

# 関数定義
def rotate_servo(deg):
    pulse = min_pulse+(max_pulse-min_pulse)*((deg+90)/180)
    servo.duty_u16(int(duty_base * pulse))

# Main loop
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
