import socket
import time
import threading
import motor_driver_v4
import autonomous_mode

UDP_IP = "0.0.0.0"
UDP_PORT = 5005
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print("✅ UDP server listening on port", UDP_PORT)

motorPower = 0.8
mode = "manual"

autonomous_thread = None

def run_autonomous_mode():
    global autonomous_thread
    if autonomous_thread is None or not autonomous_thread.is_alive():
        autonomous_thread = threading.Thread(target=autonomous_mode.autonomous_navigation)
        autonomous_thread.daemon = True
        autonomous_thread.start()  # starts navigation loop
        print("autonomous thread started")
def stop_autonomous_mode():
    global autonomous_thread
    if autonomous_thread and autonomous_thread.is_alive():
        autonomous_mode.stop()
        autonomous_thread.join()
        print("🛑 Autonomous thread stopped")
    autonomous_thread = None

def parseCommand(command):
    global motorPower, mode, autonomous_thread
    parts = command.split(":")
    action = parts[0].strip().lower()

    if len(parts) > 1 and action != "mode":
        try:
            motorPower = float(parts[1])
            print(f"⚡ Motor power updated: {motorPower * 100}%")
        except ValueError:
            print("❌ Invalid power value received")

    if action == "mode":
        if parts[1] == "auto" and mode != "auto":
            mode = "auto"
            print("🤖 Switched to Autonomous Mode")
            stop_autonomous_mode()  # Safety stop if already running
            autonomous_thread = threading.Thread(target=run_autonomous_mode)
            autonomous_thread.daemon = True
            autonomous_thread.start()
        elif parts[1] == "manual" and mode != "manual":
            mode = "manual"
            print("🎮 Switched to Controlled Mode")
            stop_autonomous_mode()

    elif mode == "manual":
        handle_manual_command(action)

def handle_manual_command(action):
    if action == "w":
        motor_driver_v4.setMotorLeft(-motorPower)
        motor_driver_v4.setMotorRight(-motorPower)
        time.sleep(1)
    elif action == "s":
        motor_driver_v4.setMotorLeft(motorPower)
        motor_driver_v4.setMotorRight(motorPower)
        time.sleep(1)
    elif action == "a":
        motor_driver_v4.setMotorLeft(-motorPower)
        motor_driver_v4.setMotorRight(motorPower)
        time.sleep(0.5)
    elif action == "d":
        motor_driver_v4.setMotorLeft(motorPower)
        motor_driver_v4.setMotorRight(-motorPower)
        time.sleep(0.5)
    elif action == "q":
        motor_driver_v4.setMotorLeft(0)
        motor_driver_v4.setMotorRight(0)
        print("⏹️ Stopped bot")

    motor_driver_v4.setMotorLeft(0)
    motor_driver_v4.setMotorRight(0)

try:
    while True:
        data, addr = sock.recvfrom(1024)
        command = data.decode().strip()
        print(f"📩 Received command: {command}")
        parseCommand(command)

except KeyboardInterrupt:
    print("\n🛑 Server shutting down")
    stop_autonomous_mode()
    sock.close()
    motor_driver_v4.exit()

