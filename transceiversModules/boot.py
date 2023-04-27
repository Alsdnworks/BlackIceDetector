# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()
import machine
import time
from main import main
import conn
print('booted')
# Set up PWM output pin
buzzer_pin = machine.Pin(15, machine.Pin.OUT)
pwm = machine.PWM(buzzer_pin)

try:
    # Set up PWM output pin
    conn.connect()
    buzzer_pin = machine.Pin(15, machine.Pin.OUT)
    pwm = machine.PWM(buzzer_pin)
    pwm.duty(10)
    pwm.freq(1000)
    time.sleep(1)
    pwm.deinit()
    
    print('no error')
except:
    pwm.duty(3)
    pwm.freq(3000)
    time.sleep(1)
    pwm.deinit()
    
main()

#print ('cpl')

