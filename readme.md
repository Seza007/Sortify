# ♻️ Sortify: Intelligent Waste Collection and Segregation Bot

**Sortify** is a smart, autonomous garbage classifier bot designed to improve solid waste management through real-time object tracking, classification, and segregation — targeting homes, factories, institutions, and urban environments. Powered by **AI/ML**, **IoT**, and robotics, Sortify is an end-to-end robotic solution for sustainable waste recovery.

---

## 🚀 Project Overview

Globally, poor waste segregation and manual collection methods pose risks to health, labor economics, and urban sanitation. Sortify answers this challenge by:

- 🔍 Identifying and tracking waste items on the ground
- 🧠 Classifying them as **biodegradable** or **non-biodegradable**
- 🚚 Collecting and segregating them autonomously
- 📡 Using an IoT application for real-time control & monitoring

> The project aligns with **UN SDG #11 – Sustainable Cities and Communities** and is engineered for scalable use across smart cities, educational campuses, event spaces, and environmental clean-up drives.

---

## 🧠 Key Features

- ✅ **Autonomous Navigation:** Obstacle avoidance, 2D LiDAR-based mapping
- 🧠 **Machine Learning Waste Classification:** Real-time object detection using OpenCV and a trained ML model
- 🧼 **Intelligent Sweeping & Disposal:** Servo-controlled arm with dual waste bins
- 📱 **IoT Integration:** App-based status updates, SOS triggers, and analysis of waste trends
- ☀️ **Solar-powered system** (optional component)

---

## 📁 Project Structure

Sortify/
│
├── code/ # Source code for ML, bot control, and IoT
│ ├── detection/ # Object detection scripts (OpenCV/ML)
│ ├── iot/ # IoT control and reporting architecture
│ ├── navigation/ # Bot movement, mapping and obstacle avoidance
│ └── utils/ # Helper functions, hardware control
│
├── models/ # Pre-trained ML models
│
├── hardware/ # Microcontroller schematics and BOM
│
├── docs/ # Research papers, design concepts
│
├── Sortify-concept-and-design.pdf # Full documentation
└── README.md # This file

---

## 🔧 Installation

### Requirements
- Python 3.8+
- OpenCV
- TensorFlow or PyTorch
- Flask or MQTT library (for IoT)
- Raspberry Pi / ESP32 (for embedded deployment)

### Setup

Clone the repository

git clone https://github.com/Seza007/Sortify.git
cd Sortify/code
Install dependencies (example for Python)

pip install -r requirements.txt

Required precise hardware connections and power delivery systems in place for proper working

### Run Classifier Demo

cd detection
python waste_classifier.py # Sample object detection and classification

text

### IoT App Integration

The bot can optionally send and receive updates via MQTT to a mobile/web dashboard.

---

## 📊 Survey Insights

> Out of 25 participants (77% aged 18–30), only **22.6% segregated waste regularly** and **85.7% had never heard of a smart segregation system**, validating the urgency and market potential of Sortify.

---

## 🎯 Target Use Cases

- 🏠 Residential neighborhoods & gated communities
- 🏫 Educational institutions & campuses
- 🏭 Factories and industrial parks
- 🌊 Beach & park cleanup operations (via NGOs or CSR)
- 🏥 Event spaces, hospitals and public venues

---

## 💡 Technology Stack

| Domain               | Stack/Tools Used                               |
|----------------------|------------------------------------------------|
| Navigation           | Gyroscope, LiDAR, Ultrasonic sensors           |
| Object Classification| OpenCV + ML Model (e.g. CNN-based)            |
| Robotics             | Motor modules, 3D-printed servo disposal arm   |
| IoT and Dashboard    | Flask/MQTT + App for control and alerts        |
| AI Features          | Frame-based multi-threading, waste analysis    |


---

## 🦾 Team Roles (6 Thinking Hats)

- **Blue Hat – Project Management**: Seshadhri (lead, structured implementation)
- **White Hat – Research**: Ajay (logic, feasibility)
- **Yellow Hat – Strategy & Benefits**: Kamalesh
- **Black Hat – Risk Analyst**: Ashwin (feasibility proofs, drawbacks)
- **Green Hat – Innovation**: Seshadhri, Ajay
- **Red Hat – Vision & Emotion-led Design**: Adarsh

---

## 📈 Business & Environmental Impact

- Aims to reduce labor cost (~₹15,000–₹20,000/month saved per deployment)
- Promotes recycling accuracy and environmental safety
- One-time hardware cost: ₹35k–₹50k
- Modular, scalable, and adaptable for future smart city ecosystems

---

## 📄 License & Credits

This project is developed as an open concept and may use third-party components and libraries. Please check individual directories for specific licenses where applicable.

---

## 🤝 Contribution & Future Roadmap

Want to get involved?

- 🧠 Improve the ML model accuracy
- 🦿 Stabilize motion path prediction
- 📲 Build out the IoT app
- 📦 Optimize for mass production

Feel free to fork 📁, clone 💻, and contribute via pull requests!

---

## 📬 Contact

For queries, ideas, or collaborations, please contact:

**Seshadhri A.** — [GitHub](https://github.com/Seza007)  

---

### 🌱 *"One waste at a time, we build cleaner cities."*

