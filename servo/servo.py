from machine import Pin, PWM
from time import sleep_ms

# ピン割り当て
pwm_pin = Pin(28)

# パラメータ設定
period = 20 #ms(周期)
min_pulse, min_deg = 0.5, -90 #ms(パルス幅), −90 deg
max_pulse, max_deg = 2.4,  90 #ms(パルス幅), +90 deg

# サーボモータ定義
servo = PWM(pwm_pin)
servo.freq(int(1/period*1000))
duty_base = 65535/period

# 関数定義
def rotate_servo(deg):
    pulse = min_pulse+(max_pulse-min_pulse)*((deg-min_deg)/(max_deg-min_deg))
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
