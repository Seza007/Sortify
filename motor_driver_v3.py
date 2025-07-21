import socket
import RPi.GPIO as io
import time

# GPIO Setup
io.setmode(io.BCM)
io.setwarnings(False)

# Left Motor Pins
L_L_EN = 21  
L_R_EN = 20  
L_L_PWM = 13 
L_R_PWM = 18 

# Right Motor Pins
R_L_EN = 24  
R_R_EN = 25  
R_L_PWM = 12 
R_R_PWM = 19  

# Setup GPIO
for pin in [L_L_EN, L_R_EN, L_L_PWM, L_R_PWM, R_L_EN, R_R_EN, R_L_PWM, R_R_PWM]:
    io.setup(pin, io.OUT)

# Setup PWM
leftmotorpwm_l = io.PWM(L_L_PWM, 100)
leftmotorpwm_r = io.PWM(L_R_PWM, 100)
rightmotorpwm_l = io.PWM(R_L_PWM, 100)
rightmotorpwm_r = io.PWM(R_R_PWM, 100)

for pwm in [leftmotorpwm_l, leftmotorpwm_r, rightmotorpwm_l, rightmotorpwm_r]:
    pwm.start(0)

def setMotorMode(motor, mode):
    if motor == "leftmotor":
        io.output(L_L_EN, mode == "forward")
        io.output(L_R_EN, mode == "reverse")
    elif motor == "rightmotor":
        io.output(R_L_EN, mode == "forward")
        io.output(R_R_EN, mode == "reverse")

def move(command):
    power = 80  
    print(f"🔹 Executing command: {command}")  

    if command == "w":  # Forward
        setMotorMode("leftmotor", "forward")
        setMotorMode("rightmotor", "forward")
    elif command == "s":  # Backward
        setMotorMode("leftmotor", "reverse")
        setMotorMode("rightmotor", "reverse")
    elif command == "a":  # Left
        setMotorMode("leftmotor", "reverse")
        setMotorMode("rightmotor", "forward")
    elif command == "d":  # Right
        setMotorMode("leftmotor", "forward")
        setMotorMode("rightmotor", "reverse")
    elif command == "q":  # Stop
        print("⏹ STOP command received")
        setMotorMode("leftmotor", "stop")
        setMotorMode("rightmotor", "stop")
    else:
        print(f"❌ Unknown command: {command}")
        return

    leftmotorpwm_l.ChangeDutyCycle(power if command in ["a", "w"] else 0)
    leftmotorpwm_r.ChangeDutyCycle(power if command in ["s"] else 0)
    rightmotorpwm_l.ChangeDutyCycle(power if command in ["d", "w"] else 0)
    rightmotorpwm_r.ChangeDutyCycle(power if command in ["s"] else 0)

    if command != "q":  
        time.sleep(2)
        move("q")  # Auto-stop after 2 seconds

# UDP Server
UDP_IP = "0.0.0.0"
UDP_PORT = 5005
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print(f"✅ UDP server listening on port {UDP_PORT}")

while True:
    data, addr = sock.recvfrom(1024)
    command = data.decode().strip().lower()
    print(f"📥 Received command: {command} from {addr}")
    move(command)
