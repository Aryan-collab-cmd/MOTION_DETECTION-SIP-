import cv2
import numpy as np
from datetime import datetime
import os

# Background subtractor (MOG2)
bg_subtractor = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=50, detectShadows=True)

# CLAHE for adaptive contrast enhancement
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))

video = cv2.VideoCapture(0)

# Video writer setup (initialized later correctly)
fourcc = cv2.VideoWriter_fourcc(*'avc1')  # better for .mov
out = None
recording = False

def draw_button(frame):
    # Draw red button
    cv2.rectangle(frame, (10, 400), (150, 460), (0, 0, 255), -1)
    label = "STOP" if recording else "REC"
    cv2.putText(frame, label, (30, 440),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

def mouse_callback(event, x, y, flags, param):
    global recording
    # Check if click is inside the REC button area
    if event == cv2.EVENT_LBUTTONDOWN:
        if 10 <= x <= 150 and 400 <= y <= 460:
            recording = not recording

            if recording:
                # Initialize writer when recording starts
                height, width, _ = frame1.shape
                global out
                os.makedirs("recordings", exist_ok=True)
                filename = datetime.now().strftime("recordings/recording_%Y-%m-%d_%H-%M-%S.mov")
                out = cv2.VideoWriter(filename, fourcc, 20.0, (width, height))
                print(f"Saved as: {filename}")
                print("Recording: ON")
            else:
                # Release file when stopped
                if out:
                    out.release()
                print("Recording: OFF")

ret, frame1 = video.read()
ret, frame2 = video.read()

while video.isOpened():
    cv2.setMouseCallback("Smart Camera Preview", mouse_callback)

    draw_button(frame1)

    # Convert frames to grayscale
    gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

    # Apply CLAHE for better contrast in low light
    gray1 = clahe.apply(gray1)
    gray2 = clahe.apply(gray2)

    # Detect brightness BEFORE enhancement
    brightness = np.mean(gray1)
    low_light = brightness < 60

    # Increase brightness for low light
    gray1 = cv2.convertScaleAbs(gray1, alpha=2, beta=40)
    gray2 = cv2.convertScaleAbs(gray2, alpha=2, beta=40)

    # Reduce noise
    gray1 = cv2.medianBlur(gray1, 5)
    gray2 = cv2.medianBlur(gray2, 5)


    # Use enhanced grayscale for better detection in low light
    if low_light:
        fg_mask = bg_subtractor.apply(gray1)
    else:
        fg_mask = bg_subtractor.apply(frame1)

    # Reduce noise in mask
    fg_mask = cv2.GaussianBlur(fg_mask, (5,5), 0)

    # Adaptive threshold for low light
    thresh_val = 180 if low_light else 200
    _, motion_mask = cv2.threshold(fg_mask, thresh_val, 255, cv2.THRESH_BINARY)

    # Stronger morphology for cleaner detection
    kernel = np.ones((5,5), np.uint8)
    dilated = cv2.morphologyEx(motion_mask, cv2.MORPH_CLOSE, kernel, iterations=2)
    dilated = cv2.dilate(dilated, kernel, iterations=2)

    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    motion_detected = False
    boxes = []

    for contour in contours:

        # Lower threshold in low light to catch subtle motion
        min_area = 800 if low_light else 1500
        if cv2.contourArea(contour) < min_area:
            continue

        motion_detected = True

        x,y,w,h = cv2.boundingRect(contour)
        boxes.append((x, y, w, h))

        cv2.rectangle(frame1,(x,y),(x+w,y+h),(0,255,0),2)

    # Display motion status text
    if motion_detected:
        cv2.putText(frame1,"Motion: YES",(10,30),
                    cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
        cv2.putText(frame1, "MOTION DETECTED", (10, 90),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)
    else:
        cv2.putText(frame1,"Motion: NO",(10,30),
                    cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)

    # Smart preview based on lighting
    if low_light:
        # In low light, show processed view for better visibility
        display_frame = cv2.cvtColor(gray1, cv2.COLOR_GRAY2BGR)
        display_frame = cv2.convertScaleAbs(display_frame, alpha=0.9, beta=-20)
        cv2.putText(display_frame, "LOW LIGHT MODE", (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,255), 2)

        # Draw ULTRA visible motion boxes in low light mode
        for (x, y, w, h) in boxes:
            # Create overlay for transparency effect
            overlay = display_frame.copy()

            # Draw filled rectangle (semi-transparent)
            cv2.rectangle(overlay, (x, y), (x+w, y+h), (0, 255, 255), -1)

            # Blend overlay with original (transparency)
            cv2.addWeighted(overlay, 0.3, display_frame, 0.7, 0, display_frame)

            # Draw bold border
            cv2.rectangle(display_frame, (x, y), (x+w, y+h), (0,255,255), 4)

            # Draw corner highlights (better visibility)
            cv2.line(display_frame, (x, y), (x+20, y), (255,255,255), 3)
            cv2.line(display_frame, (x, y), (x, y+20), (255,255,255), 3)

            cv2.line(display_frame, (x+w, y), (x+w-20, y), (255,255,255), 3)
            cv2.line(display_frame, (x+w, y), (x+w, y+20), (255,255,255), 3)

            cv2.line(display_frame, (x, y+h), (x+20, y+h), (255,255,255), 3)
            cv2.line(display_frame, (x, y+h), (x, y+h-20), (255,255,255), 3)

            cv2.line(display_frame, (x+w, y+h), (x+w-20, y+h), (255,255,255), 3)
            cv2.line(display_frame, (x+w, y+h), (x+w, y+h-20), (255,255,255), 3)

            # Add clearer label with background
            cv2.rectangle(display_frame, (x, y-25), (x+80, y), (0,255,255), -1)
            cv2.putText(display_frame, "MOTION", (x+5, y-5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 2)
    else:
        # Normal lighting → show original frame
        display_frame = frame1

    # Add real-time timestamp
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cv2.putText(frame1, current_time, (10, 470),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    # Record EVERYTHING when recording is ON
    if recording and out is not None:
        out.write(display_frame)

    cv2.imshow("Smart Camera Preview", display_frame)

    frame1 = frame2
    ret, frame2 = video.read()

    key = cv2.waitKey(1) & 0xFF

    # Press 'q' to quit
    if key == ord('q'):
        break

    # Press 'r' to toggle recording
    if key == ord('r'):
        recording = not recording
        print("Recording:", "ON" if recording else "OFF")

video.release()
if out:
    out.release()
cv2.destroyAllWindows()
