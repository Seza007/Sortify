#!/usr/bin/env python
import RPi.GPIO as io
import sys

io.setmode(io.BCM)

PWM_MAX = 100

# setting warnings off for reducing the annoyance
io.setwarnings(False)

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

# The two variables leftmotorpwm_pin and rightmotorpwm_pin are 
# additionally defined as "PWM" outputs.
leftmotorpwm_l = io.PWM(leftmotorpwm_pin_l, 100)
leftmotorpwm_r = io.PWM(leftmotorpwm_pin_r, 100)

rightmotorpwm_l = io.PWM(rightmotorpwm_pin_l, 100)
rightmotorpwm_r = io.PWM(rightmotorpwm_pin_r, 100)

# The left motors are stationary because the PWM signals 
# are set to 0 with ChangeDutyCycle(0).
leftmotorpwm_l.start(0)
leftmotorpwm_r.start(0)

leftmotorpwm_l.ChangeDutyCycle(0)
leftmotorpwm_r.ChangeDutyCycle(0)

# The right motors are stationary because the PWM signals 
# are set to 0 with ChangeDutyCycle(0).
rightmotorpwm_l.start(0)
rightmotorpwm_r.start(0)

rightmotorpwm_l.ChangeDutyCycle(0)
rightmotorpwm_r.ChangeDutyCycle(0)

# The function setMotorMode(motor, mode) sets the direction of rotation of 
# the motors.
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
    else:
        io.output(leftmotor_in1_pin, False)
        io.output(leftmotor_in2_pin, False)
        io.output(rightmotor_in1_pin, False)
        io.output(rightmotor_in2_pin, False)

# The function setMotorLeft(power) sets the speed of the left motors.
def setMotorLeft(power):
    power = int(power * PWM_MAX)  # Convert power (-1 to 1) to PWM value
    if power < 0:
        # Reverse mode for the left motor
        power = -power
        if power > PWM_MAX:
            power = PWM_MAX
        leftmotorpwm_l.ChangeDutyCycle(power)  # Reverse PWM active
        leftmotorpwm_r.ChangeDutyCycle(0)      # Ensure forward PWM is OFF
    elif power > 0:
        # Forward mode for the left motor
        if power > PWM_MAX:
            power = PWM_MAX
        leftmotorpwm_l.ChangeDutyCycle(0)      # Ensure reverse PWM is OFF
        leftmotorpwm_r.ChangeDutyCycle(power)  # Forward PWM active
    else:
        # Stop mode for the left motor
        leftmotorpwm_l.ChangeDutyCycle(0)
        leftmotorpwm_r.ChangeDutyCycle(0)

# The function setMotorRight(power) sets the speed of the right motors.
def setMotorRight(power):
    power = int(power * PWM_MAX)  # Convert power (-1 to 1) to PWM value
    if power < 0:
        # Reverse mode for the right motor
        power = -power
        if power > PWM_MAX:
            power = PWM_MAX
        rightmotorpwm_l.ChangeDutyCycle(power)  # Reverse PWM active
        rightmotorpwm_r.ChangeDutyCycle(0)      # Ensure forward PWM is OFF
    elif power > 0:
        # Forward mode for the right motor
        if power > PWM_MAX:
            power = PWM_MAX
        rightmotorpwm_l.ChangeDutyCycle(0)      # Ensure reverse PWM is OFF
        rightmotorpwm_r.ChangeDutyCycle(power)  # Forward PWM active
    else:
        # Stop mode for the right motor
        rightmotorpwm_l.ChangeDutyCycle(0)
        rightmotorpwm_r.ChangeDutyCycle(0)
# Stop the motors and cleanup GPIO
def exit():
    io.output(leftmotor_in1_pin, False)
    io.output(leftmotor_in2_pin, False)
    io.output(rightmotor_in1_pin, False)
    io.output(rightmotor_in2_pin, False)
    io.cleanup()

# # Function for controlled mode using keyboard input
# def controlledMode():
#     power = 0.8
#     while True:
#         key = input("Enter command (w/a/s/d/q): ").strip().lower()
#         if key == 'w':
#             setMotorLeft(-power)
#             setMotorRight(-power)
#         elif key == 'a':
#             setMotorLeft(-power)
#             setMotorRight(power)
#         elif key == 's':
#             setMotorLeft(power)
#             setMotorRight(power)
#         elif key == 'd':
#             setMotorLeft(power)
#             setMotorRight(-power)
#         elif key == 'q':
#             setMotorLeft(0)
#             setMotorRight(0)
#             break
#         else:
#             setMotorLeft(0)
#             setMotorRight(0)
# 
# # Function for autonomous mode
# def autonomousMode():
#     power = 0.5
#     setMotorLeft(power)
#     setMotorRight(power)
# 
# # Main function
# def main():
#     mode = input("Enter mode (1 for controlled/2 for autonomous): ").strip().lower()
#     if mode == "1":
#         controlledMode()
#     elif mode == "2":
#         autonomousMode()
#     else:
#         print("Invalid mode selected. Exiting...")
#         exit()
# 
# if __name__ == "__main__":
#     main()
