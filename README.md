📷 Smart Camera Motion Detection System

🚀 Overview

This project is a real-time motion detection system built using OpenCV (Python). It is designed to work efficiently in both normal lighting and low-light environments using advanced image processing techniques.

⸻

✨ Features

🎯 Motion Detection
	•	Uses MOG2 Background Subtraction
	•	Detects moving objects in real-time
	•	Filters out noise using contour area threshold

🌙 Low Light Enhancement
	•	CLAHE (Adaptive Histogram Equalization) for contrast improvement
	•	Brightness enhancement using scaling
	•	Median filtering to reduce noise
	•	Adaptive thresholding for better detection

🟨 Enhanced Bounding Boxes
	•	High-visibility motion boxes in low light
	•	Semi-transparent overlay
	•	Bold borders + corner highlights
	•	Motion label with background

🎥 Recording System
	•	Clickable REC/STOP button
	•	Saves video in .mov format
	•	Auto filename with timestamp
	•	Stored in recordings/ folder

🕒 Timestamp
	•	Displays real-time date and time on video

⸻

🧠 Technologies Used
	•	Python
	•	OpenCV (cv2)
	•	NumPy

⸻

⚙️ How It Works
	1.	Capture frames from webcam
	2.	Convert to grayscale
	3.	Enhance using CLAHE
	4.	Detect brightness → activate low-light mode if needed
	5.	Apply background subtraction (MOG2)
	6.	Apply threshold + morphology
	7.	Detect contours (motion areas)
	8.	Draw bounding boxes
	9.	Display output / record if enabled

⸻

🖥️ Controls

Key / Action	Function
Mouse Click (REC button)	Start/Stop recording
r key	Toggle recording
q key	Quit application


⸻

📂 Project Structure

SIP/
│── main.py
│── recordings/
│── README.md


⸻

📸 Output Modes

🌞 Normal Mode
	•	Shows original frame
	•	Green bounding boxes

🌙 Low Light Mode
	•	Shows enhanced grayscale frame
	•	High-visibility motion boxes
	•	Better detection sensitivity

⸻

🔧 Future Improvements
	•	Object tracking (reduce flickering boxes)
	•	Sound alert on motion detection
	•	AI-based object classification
	•	Mobile notification system
	•	GUI improvements

⸻

👨‍💻 Author

Aryan Chavan

⸻

⭐ Notes

This project is ideal for:
	•	Mini projects (SIP / college)
	•	Surveillance system basics
	•	Learning OpenCV and computer vision

⸻

🏁 Run the Project

python main.py

Make sure you have installed:

pip install opencv-python numpy


⸻ Patil

🎉 Done!

Your smart motion detection system is ready 🚀
