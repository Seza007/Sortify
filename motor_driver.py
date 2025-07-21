import RPi.GPIO as GPIO
import time

# Setup GPIO mode
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Define Motor Control Pins
RPWM = 18  # Right PWM
LPWM = 13  # Left PWM
REN = 20   # Right Enable
LEN = 21   # Left Enable

# Set up GPIO pins
GPIO.setup(RPWM, GPIO.OUT)
GPIO.setup(LPWM, GPIO.OUT)
GPIO.setup(REN, GPIO.OUT)
GPIO.setup(LEN, GPIO.OUT)

# Set up PWM with 100 Hz frequency
pwm_r = GPIO.PWM(RPWM, 100)
pwm_l = GPIO.PWM(LPWM, 100)

# Start PWM with 0% duty cycle (stopped)
pwm_r.start(0)
pwm_l.start(0)

# Enable motor driver
GPIO.output(REN, GPIO.HIGH)
GPIO.output(LEN, GPIO.HIGH)

def set_motor_speed(speed):
    """ Control motor speed and direction (range: -100 to 100) """
    if speed > 0:
        pwm_r.ChangeDutyCycle(speed)  # Forward
        pwm_l.ChangeDutyCycle(0)
    elif speed < 0:
        pwm_r.ChangeDutyCycle(0)
        pwm_l.ChangeDutyCycle(abs(speed))  # Reverse
    else:
        pwm_r.ChangeDutyCycle(0)
        pwm_l.ChangeDutyCycle(0)  # Stop

try:
    while True:
        set_motor_speed(50)  # Forward at 50% speed
        time.sleep(2)
        
        set_motor_speed(-50)  # Reverse at 50% speed
        time.sleep(2)
        
        set_motor_speed(0)  # Stop
        time.sleep(1)

except KeyboardInterrupt:
    print("\nStopping motors...")
    pwm_r.stop()
    pwm_l.stop()
    GPIO.cleanup()
