import cv2
import numpy as np

# Define model paths
model_path = "/home/sesha/Documents/bot/ssd_mobilenet_v2_320x320_coco17_tpu-8/frozen_inference_graph.pb"
config_path = "/home/sesha/Documents/bot/ssd_mobilenet_v2_320x320_coco17_tpu-8/pipeline.config"
labels_path = "/home/sesha/Documents/bot/mscoco_label_map.pbtxt"

# Load the pre-trained model
net = cv2.dnn.readNetFromTensorflow(model_path, config_path)

# Load COCO labels
with open(labels_path, 'r') as f:
    labels = [line.strip() for line in f if 'name:' in line][::2]
    labels = [label.split(': ')[1].strip("'") for label in labels]

# Define waste categories
e_waste = ['electronics', 'cell phone', 'laptop']  # Add more as needed
medical_waste = ['bottle', 'cup']  # Proxy for syringes, gloves (limited by COCO)

# Open the camera (Raspberry Pi Camera or USB)
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 320)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        break

    # Prepare image for detection
    blob = cv2.dnn.blobFromImage(frame, size=(320, 320), swapRB=True)
    net.setInput(blob)
    detections = net.forward()

    # Process detections
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.5:  # Confidence threshold
            class_id = int(detections[0, 0, i, 1])
            label = labels[class_id - 1]  # Adjust for 1-based indexing

            # Categorize waste
            if label in e_waste:
                category = "E-Waste"
            elif label in medical_waste:
                category = "Medical Waste"
            else:
                category = "Other"

            # Draw bounding box and label
            box = detections[0, 0, i, 3:7] * np.array([frame.shape[1], frame.shape[0], frame.shape[1], frame.shape[0]])
            (startX, startY, endX, endY) = box.astype("int")
            cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)
            cv2.putText(frame, f"{category}: {label}", (startX, startY - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Display result
    cv2.imshow("Waste Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
