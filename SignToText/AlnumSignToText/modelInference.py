import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
import time
import pickle

# Load the trained model
model = load_model('./model/sign_language_model.h5')

# Load the label encoder
with open('pickle/label_encoder.pkl', 'rb') as f:
    label_encoder = pickle.load(f)

# Define rectangle coordinates for ROI (adjust as needed)
roi_start = (300, 50)    # Top-left corner of the ROI
roi_end = (700, 350)     # Bottom-right corner of the ROI

camera = cv2.VideoCapture(0)
cv2.namedWindow('Camera Feed', cv2.WINDOW_NORMAL)
cv2.namedWindow('Edges', cv2.WINDOW_NORMAL)

# Resize the windows
cv2.resizeWindow('Camera Feed', 800, 600)  # Increase size for better view
cv2.resizeWindow('Edges', 300, 300)        # Decrease size for compact display

last_prediction = None
last_prediction_time = time.time()
prediction_duration_threshold = 3  # seconds

while True:
    ret, frame = camera.read()
    frame = cv2.flip(frame, 1)

    # Draw rectangle for ROI on the camera feed
    cv2.rectangle(frame, roi_start, roi_end, (0, 255, 0), 2)

    # Extract the ROI
    roi = frame[roi_start[1]:roi_end[1], roi_start[0]:roi_end[0]]
    
    # Convert ROI to grayscale
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    # Perform Canny edge detection on the blurred image
    edges = cv2.Canny(blurred, 50, 150)
    # Convert single-channel edges to 3-channel image
    edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

    # Resize edges for display
    edges_resized = cv2.resize(edges, (300, 300))

    # Display edges in the 'Edges' window
    cv2.imshow('Edges', edges_resized)

    # Preprocess the ROI for prediction
    roi_resized = cv2.resize(roi, (100, 100))
    roi_resized = roi_resized.astype('float32') / 255.0
    roi_resized = np.expand_dims(roi_resized, axis=0)

    # Make predictions
    predictions = model.predict(roi_resized)
    confidence = np.max(predictions)
    predicted_class = np.argmax(predictions)

    if confidence > 0.8:  # Confidence threshold
        predicted_label = label_encoder.inverse_transform([predicted_class])[0]
        current_time = time.time()
        if predicted_label == last_prediction:
            if (current_time - last_prediction_time) >= prediction_duration_threshold:
                with open('../output.txt', 'a') as f:
                    f.write(predicted_label + '      ')
                last_prediction_time = current_time  # Reset the timer after writing
        else:
            last_prediction = predicted_label
            last_prediction_time = current_time
        cv2.putText(frame, f'Prediction: {predicted_label} ({confidence:.2f})', 
                    (50, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    else:
        cv2.putText(frame, 'Uncertain', (50, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        last_prediction = None  # Reset prediction if confidence is low

    # Display camera feed
    cv2.imshow('Camera Feed', frame)

    pressedKey = cv2.waitKey(1)
    if pressedKey == 27:  # ESC key to exit
        break

camera.release()
cv2.destroyAllWindows()

print("Inference ended.")
