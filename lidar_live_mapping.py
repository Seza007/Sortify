import serial
import struct
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# 🚀 LiDAR Serial Connection
PORT = "/dev/ttyUSB0"  # Change if needed
BAUDRATE = 115200
ser = serial.Serial(PORT, BAUDRATE, timeout=1)

# 🚀 Live Data Storage
angles = []
distances = []

def decode_lidar_data(data):
    """Decodes LiDAR packet to extract valid angle & distance readings"""
    if len(data) >= 5:
        try:
            angle = struct.unpack("<H", data[0:2])[0] / 64.0  # Convert to degrees
            distance = struct.unpack("<H", data[2:4])[0]  # Extract distance in mm
            quality = data[4]  # Quality value
            
            # ❌ Ignore garbage angles outside 0-360°
            if angle < 0 or angle > 360:
                return None
            
            # ❌ Ignore invalid distance values (too close / too far)
            if distance == 0 or distance > 12000:  
                return None
            
            return angle, distance, quality
        except struct.error:
            return None

def read_lidar():
    """Reads LiDAR data & updates global storage"""
    global angles, distances
    
    data = ser.read(5)  # Read 5-byte packet
    result = decode_lidar_data(data)

    if result:
        angle, distance, quality = result
        print(f"📍 Angle: {angle:.1f}° | 📏 Distance: {distance} mm | ⭐ Quality: {quality}")

        angles.append(np.radians(angle))  # Convert to radians
        distances.append(distance / 1000)  # Convert to meters

        # Keep only latest 360 points (1 full rotation)
        if len(angles) > 360:
            angles.pop(0)
            distances.pop(0)

def update_plot(frame):
    """Updates Matplotlib plot in real-time"""
    ax.clear()
    ax.set_theta_zero_location("N")  # 0° at the top
    ax.set_theta_direction(-1)  # Clockwise rotation
    ax.set_rlim(0, 12)  # Max range (12m)

    ax.scatter(angles, distances, c="lime", s=10, alpha=0.7)  # Plot points
    ax.set_title("Real-Time LiDAR Mapping", fontsize=14, color="white")

def run_lidar():
    """Continuously reads LiDAR data and updates plot"""
    while True:
        read_lidar()

# 🚀 Matplotlib Setup
plt.style.use("dark_background")
fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
ani = animation.FuncAnimation(fig, update_plot, interval=50)

# 🚀 Run LiDAR & Visualization in Parallel
from threading import Thread
lidar_thread = Thread(target=run_lidar, daemon=True)
lidar_thread.start()

print("\n🔍 LiDAR Live Mapping Started... (Ctrl+C to stop)\n")
plt.show()
