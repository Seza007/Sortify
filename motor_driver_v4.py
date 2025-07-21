import RPi.GPIO as io
import time

io.setmode(io.BCM)
io.setwarnings(False)

PWM_MAX = 100

# --- STARTING GPIO PIN ADDRESSING ---

# Left motor pin allocations
L_L_EN = 21  # Left motor forward enable pin  
L_R_EN = 20  # Left motor reverse enable pin 
L_L_PWM = 13 # left motor forward pwm
L_R_PWM = 18 # left motor reverse pwm

# Right motor pin allocations
R_L_EN = 24  # Right motor forward enable pin  
R_R_EN = 25  # Right motor reverse enable pin  
R_L_PWM = 12 # right motor forward pwm
R_R_PWM = 19  # right motor reverse pwm

# Left Motor enable pin initializations 
leftmotor_in1_pin = L_L_EN
leftmotor_in2_pin = L_R_EN

io.setup(leftmotor_in1_pin, io.OUT)
io.setup(leftmotor_in2_pin, io.OUT)

# Right Motor enable pin initializations 
rightmotor_in1_pin = R_L_EN
rightmotor_in2_pin = R_R_EN

io.setup(rightmotor_in1_pin, io.OUT)
io.setup(rightmotor_in2_pin, io.OUT)

# changing the default false to true
io.output(leftmotor_in1_pin, True)
io.output(leftmotor_in2_pin, True)
io.output(rightmotor_in1_pin, True)
io.output(rightmotor_in2_pin, True)

# Left Motor PWM pin initializations
leftmotorpwm_pin_l = L_L_PWM 
leftmotorpwm_pin_r = L_R_PWM

# Right Motor PWM pin initializations
rightmotorpwm_pin_l = R_L_PWM
rightmotorpwm_pin_r = R_R_PWM

# Setup
io.setup(leftmotorpwm_pin_l, io.OUT)
io.setup(leftmotorpwm_pin_r, io.OUT)

io.setup(rightmotorpwm_pin_l, io.OUT)
io.setup(rightmotorpwm_pin_r, io.OUT)

# Define PWM outputs
leftmotorpwm_l = io.PWM(leftmotorpwm_pin_l, 100)
leftmotorpwm_r = io.PWM(leftmotorpwm_pin_r, 100)

rightmotorpwm_l = io.PWM(rightmotorpwm_pin_l, 100)
rightmotorpwm_r = io.PWM(rightmotorpwm_pin_r, 100)

# Initialize motors to stop
leftmotorpwm_l.start(0)
leftmotorpwm_r.start(0)
rightmotorpwm_l.start(0)
rightmotorpwm_r.start(0)

def setMotorMode(motor, mode):
    if motor == "leftmotor":
        if mode == "reverse":
            io.output(leftmotor_in1_pin, True)
            io.output(leftmotor_in2_pin, False)
        elif mode == "forward":
            io.output(leftmotor_in1_pin, False)
            io.output(leftmotor_in2_pin, True)
        else:
            io.output(leftmotor_in1_pin, False)
            io.output(leftmotor_in2_pin, False)
    elif motor == "rightmotor":
        if mode == "reverse":
            io.output(rightmotor_in1_pin, False)
            io.output(rightmotor_in2_pin, True)      
        elif mode == "forward":
            io.output(rightmotor_in1_pin, True)
            io.output(rightmotor_in2_pin, False)
        else:
            io.output(rightmotor_in1_pin, False)
            io.output(rightmotor_in2_pin, False)

def setMotorLeft(power):
    power = int(power * PWM_MAX)
    if power < 0:
        power = -power
        if power > PWM_MAX:
            power = PWM_MAX
        leftmotorpwm_l.ChangeDutyCycle(power)
        leftmotorpwm_r.ChangeDutyCycle(0)
    elif power > 0:
        if power > PWM_MAX:
            power = PWM_MAX
        leftmotorpwm_l.ChangeDutyCycle(0)
        leftmotorpwm_r.ChangeDutyCycle(power)
    else:
        leftmotorpwm_l.ChangeDutyCycle(0)
        leftmotorpwm_r.ChangeDutyCycle(0)

def setMotorRight(power):
    power = int(power * PWM_MAX)
    if power < 0:
        power = -power
        if power > PWM_MAX:
            power = PWM_MAX
        rightmotorpwm_l.ChangeDutyCycle(power)
        rightmotorpwm_r.ChangeDutyCycle(0)
    elif power > 0:
        if power > PWM_MAX:
            power = PWM_MAX
        rightmotorpwm_l.ChangeDutyCycle(0)
        rightmotorpwm_r.ChangeDutyCycle(power)
    else:
        rightmotorpwm_l.ChangeDutyCycle(0)
        rightmotorpwm_r.ChangeDutyCycle(0)

def exit():
    io.output(leftmotor_in1_pin, False)
    io.output(leftmotor_in2_pin, False)
    io.output(rightmotor_in1_pin, False)
    io.output(rightmotor_in2_pin, False)
    io.cleanup()

