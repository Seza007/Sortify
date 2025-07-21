import RPi.GPIO as io
import time
import motor_driver_v4  # Use your existing motor driver functions

# === Ultrasonic Sensor Pins ===
TRIG_FRONT = 5
ECHO_FRONT = 6

TRIG_LEFT = 16
ECHO_LEFT = 26

TRIG_RIGHT = 23
ECHO_RIGHT = 17

io.setmode(io.BCM)
io.setwarnings(False)

# === Ultrasonic Setup ===
def setup_ultrasonic():
    sensors = [(TRIG_FRONT, ECHO_FRONT), (TRIG_LEFT, ECHO_LEFT), (TRIG_RIGHT, ECHO_RIGHT)]
    
    for trig, echo in sensors:
        io.setup(trig, io.OUT)
        io.setup(echo, io.IN)
        io.output(trig, False)

# === Ultrasonic Distance Measurement ===
def get_distance(trig, echo):
    # Trigger pulse
    io.output(trig, True)
    time.sleep(0.00001)
    io.output(trig, False)

    # Wait for echo start
    start = time.time()
    while io.input(echo) == 0:
        start = time.time()

    # Wait for echo end
    stop = time.time()
    while io.input(echo) == 1:
        stop = time.time()

    time_elapsed = stop - start
    distance = (time_elapsed * 34300) / 2  # in cm

    return distance

# === Autonomous Navigation ===
def autonomous_navigation():
    setup_ultrasonic()
    print("🤖 Autonomous mode started. Power: 0.6, Obstacle distance: 10 cm\n")

    try:
        while True:
            # Read distances
            front_distance = get_distance(TRIG_FRONT, ECHO_FRONT)
            left_distance = get_distance(TRIG_LEFT, ECHO_LEFT)
            right_distance = get_distance(TRIG_RIGHT, ECHO_RIGHT)

            print(f"📏 Front: {front_distance:.1f} cm | Left: {left_distance:.1f} cm | Right: {right_distance:.1f} cm")

            # === Movement Logic ===
            if front_distance < 10 and left_distance < 10 and right_distance < 10:
                print("🔄 All sides blocked! Turning 180°")
                motor_driver_v4.setMotorLeft(0)
                motor_driver_v4.setMotorRight(0)
                time.sleep(0.5)

                motor_driver_v4.setMotorLeft(0.6)
                motor_driver_v4.setMotorRight(-0.6)
                time.sleep(1.5)

            elif front_distance < 10:
                print("⬆️ Obstacle in front! Moving back")
                motor_driver_v4.setMotorLeft(0)
                motor_driver_v4.setMotorRight(0)
                time.sleep(0.5)

                motor_driver_v4.setMotorLeft(-0.6)
                motor_driver_v4.setMotorRight(-0.6)
                time.sleep(1)

            elif left_distance < 10:
                print("⬅️ Obstacle left! Turning right")
                motor_driver_v4.setMotorLeft(0)
                motor_driver_v4.setMotorRight(0)
                time.sleep(0.5)

                motor_driver_v4.setMotorLeft(0.6)
                motor_driver_v4.setMotorRight(-0.6)
                time.sleep(0.5)

            elif right_distance < 10:
                print("➡️ Obstacle right! Turning left")
                motor_driver_v4.setMotorLeft(0)
                motor_driver_v4.setMotorRight(0)
                time.sleep(0.5)

                motor_driver_v4.setMotorLeft(-0.6)
                motor_driver_v4.setMotorRight(0.6)
                time.sleep(0.5)

            else:
                print("✅ Path clear! Moving forward")
                motor_driver_v4.setMotorLeft(-0.6)
                motor_driver_v4.setMotorRight(-0.6)

            time.sleep(0.2)

    except KeyboardInterrupt:
        print("🛑 Autonomous navigation stopped by user")
        motor_driver_v4.setMotorLeft(0)
        motor_driver_v4.setMotorRight(0)
        io.cleanup()

# === Control Start/Stop from Serial ===
if __name__ == "__main__":
    while True:
        user_input = input("\n▶️ Type 'start' to begin autonomous mode or 'stop' to exit: ").strip().lower()

        if user_input == 'start':
            autonomous_navigation()

        elif user_input == 'stop':
            print("💤 Exiting program...")
            motor_driver_v4.setMotorLeft(0)
            motor_driver_v4.setMotorRight(0)
            io.cleanup()
            break

        else:
            print("❓ Invalid input. Type 'start' or 'stop'.")
