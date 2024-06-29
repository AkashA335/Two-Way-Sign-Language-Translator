import numpy as np
import cv2
import os

CAPTURE_FLAG = False

directory = 'data'

exit_flag = '**'

try:
    os.mkdir(directory)
except:
    print('Directory already exists!')

subDirectory = input('Enter sub directory name or press ** to exit: ')

if subDirectory == exit_flag:
    print('exit')
else:
    path = os.path.join(directory, subDirectory)
    try:
        os.mkdir(path)
    except:
        print('Sub directory already exists!')

camera = cv2.VideoCapture(0)
print('Now camera window will be open, then \n1) Place your hand gesture in ROI and press c key to start capturing images. \n2) Press esc key to exit.')

count = 0

# Define rectangle coordinates for ROI (adjust as needed)
roi_start = (300, 50)    # Top-left corner of the ROI
roi_end = (700, 350)     # Bottom-right corner of the ROI

cv2.namedWindow('Camera Feed', cv2.WINDOW_NORMAL)
cv2.namedWindow('Edges', cv2.WINDOW_NORMAL)

# Resize the windows
cv2.resizeWindow('Camera Feed', 800, 600)  # Increase size for better view
cv2.resizeWindow('Edges', 300, 300)       # Decrease size for compact display

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

    # Display camera feed
    cv2.imshow('Camera Feed', frame)

    pressedKey = cv2.waitKey(1)
    if pressedKey == 27:
        break
    elif pressedKey == ord('c'):
        CAPTURE_FLAG = not CAPTURE_FLAG

    # Capture and process images if CAPTURE_FLAG is True
    if CAPTURE_FLAG:
        if count < 1200:
            # Display ROI with capturing status on the 'Camera Feed' window
            frame_with_text = frame.copy()
            cv2.putText(frame_with_text, 'Capturing..', (50, 70), cv2.FONT_HERSHEY_SIMPLEX,
                        1.5, (0, 255, 0), 2, cv2.LINE_AA)
            cv2.imshow('Camera Feed', frame_with_text)

            # Resize ROI before saving
            roi_resized = cv2.resize(roi, (100, 100))
            # Save the image with subdirectory name
            filename = f"{subDirectory}_{count}.jpg"
            cv2.imwrite(os.path.join(path, filename), roi_resized)
            count += 1
            print(count)
        else:
            break
    
    # Display count on the 'Camera Feed' window
    cv2.putText(frame, str(count), (50, 450), cv2.FONT_HERSHEY_SIMPLEX,  
                2, (0, 255, 0), 2, cv2.LINE_AA)
    cv2.imshow('Camera Feed', frame)

camera.release()
cv2.destroyAllWindows()

print('Completed!')
