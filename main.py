import cv2
import numpy as np

video = cv2.VideoCapture(0)

ret, frame1 = video.read()
ret, frame2 = video.read()

while video.isOpened():

    # Convert frames to grayscale
    gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

    # Detect brightness BEFORE enhancement
    brightness = np.mean(gray1)
    low_light = brightness < 60

    # Increase brightness for low light
    gray1 = cv2.convertScaleAbs(gray1, alpha=2, beta=40)
    gray2 = cv2.convertScaleAbs(gray2, alpha=2, beta=40)

    # Reduce noise
    gray1 = cv2.medianBlur(gray1, 5)
    gray2 = cv2.medianBlur(gray2, 5)

    # Enhance contrast for low light
    gray1 = cv2.equalizeHist(gray1)
    gray2 = cv2.equalizeHist(gray2)

    # Frame differencing directly on grayscale images
    diff = cv2.absdiff(gray1, gray2)


    # Remove noise
    blur = cv2.GaussianBlur(diff, (5,5), 0)

    # Binary threshold again to clean motion areas
    _, motion_mask = cv2.threshold(blur, 40, 255, cv2.THRESH_BINARY)

    # Dilate to strengthen motion regions
    dilated = cv2.dilate(motion_mask, None, iterations=3)

    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    motion_detected = False

    for contour in contours:

        if cv2.contourArea(contour) < 2000:
            continue

        motion_detected = True

        x,y,w,h = cv2.boundingRect(contour)

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
        cv2.putText(display_frame, "LOW LIGHT MODE", (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,255), 2)
    else:
        # Normal lighting → show original frame
        display_frame = frame1

    cv2.imshow("Smart Camera Preview", display_frame)

    frame1 = frame2
    ret, frame2 = video.read()

    if cv2.waitKey(1) & 0xFF == 27:
        break

video.release()
cv2.destroyAllWindows()