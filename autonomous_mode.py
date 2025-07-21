import RPi.GPIO as io
import time
import motor_driver_v4  # Using your existing motor driver module

io.setmode(io.BCM)
io.setwarnings(False)

# Sensor Pins (use these in ultrasonic setup)
TRIG_FRONT = 5
ECHO_FRONT = 6

TRIG_LEFT = 16
ECHO_LEFT = 26

TRIG_RIGHT = 23
ECHO_RIGHT = 17

# Ultrasonic setup function
def setup_ultrasonic_pins():
    sensors = [
        (TRIG_FRONT, ECHO_FRONT),
        (TRIG_LEFT, ECHO_LEFT),
        (TRIG_RIGHT, ECHO_RIGHT)
    ]
    
    for trig, echo in sensors:
        io.setup(trig, io.OUT)
        io.setup(echo, io.IN)
        io.output(trig, False)

# Distance measurement function
def get_distance(trig_pin, echo_pin):
    # Send trigger pulse
    io.output(trig_pin, True)
    time.sleep(0.00001)
    io.output(trig_pin, False)

    # Wait for echo start
    start_time = time.time()
    while io.input(echo_pin) == 0:
        start_time = time.time()

    # Wait for echo end
    stop_time = time.time()
    while io.input(echo_pin) == 1:
        stop_time = time.time()

    # Time difference
    time_elapsed = stop_time - start_time
    distance = (time_elapsed * 34300) / 2  # in cm
    return distance

def autonomous_navigation():
    setup_ultrasonic_pins()
    print("🤖 Autonomous Mode Activated")

    try:
        while True:
            front_distance = get_distance(TRIG_FRONT, ECHO_FRONT)
            left_distance = get_distance(TRIG_LEFT, ECHO_LEFT)
            right_distance = get_distance(TRIG_RIGHT, ECHO_RIGHT)

            print(f"📏 Front: {front_distance:.1f} cm | Left: {left_distance:.1f} cm | Right: {right_distance:.1f} cm")

            # Movement decision logic
            if front_distance < 15 and left_distance < 15 and right_distance < 15:
                print("🚧 All sides blocked. Turning 180°")
                motor_driver_v4.setMotorLeft(0)
                motor_driver_v4.setMotorRight(0)
                time.sleep(1)
                motor_driver_v4.setMotorLeft(0.6)
                motor_driver_v4.setMotorRight(-0.6)
                time.sleep(1.5)

            elif front_distance < 15:
                print("⚠️ Obstacle ahead! Moving backward")
                motor_driver_v4.setMotorLeft(0)
                motor_driver_v4.setMotorRight(0)
                time.sleep(1)
                motor_driver_v4.setMotorLeft(-0.6)
                motor_driver_v4.setMotorRight(-0.6)
                time.sleep(1)

            elif left_distance < 15:
                print("⬅️ Obstacle on left! Turning right")
                motor_driver_v4.setMotorLeft(0)
                motor_driver_v4.setMotorRight(0)
                time.sleep(1)
                motor_driver_v4.setMotorLeft(0.6)
                motor_driver_v4.setMotorRight(-0.6)
                time.sleep(0.5)

            elif right_distance < 15:
                print("➡️ Obstacle on right! Turning left")
                motor_driver_v4.setMotorLeft(0)
                motor_driver_v4.setMotorRight(0)
                time.sleep(1)
                motor_driver_v4.setMotorLeft(-0.6)
                motor_driver_v4.setMotorRight(0.6)
                time.sleep(0.5)

            else:
                print("✅ Path clear! Moving forward")
                motor_driver_v4.setMotorLeft(-0.6)
                motor_driver_v4.setMotorRight(-0.6)

            time.sleep(0.1)

    except KeyboardInterrupt:
        print("⛔ Stopping Autonomous Mode")
        motor_driver_v4.setMotorLeft(0)
        motor_driver_v4.setMotorRight(0)
        io.cleanup()

def stop():
    print("🛑 Autonomous Mode Stopped")
    motor_driver_v4.setMotorLeft(0)
    motor_driver_v4.setMotorRight(0)
    io.cleanup()

# Debugging / Direct Run
if __name__ == "__main__":
    autonomous_navigation()
    