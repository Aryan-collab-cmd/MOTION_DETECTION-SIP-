# MOTION_DETECTION-SIP-
A real-time motion detection system built using OpenCV and Python that intelligently adapts to lighting conditions. The system automatically switches between normal and enhanced low-light modes to ensure reliable motion detection even in dark environments.
📌 Motion_Detection

A real-time motion detection system built using OpenCV and Python that intelligently adapts to lighting conditions. The system automatically switches between normal and enhanced low-light modes to ensure reliable motion detection even in dark environments.

⸻

🚀 Features
	•	🎥 Real-time motion detection using frame differencing
	•	🌙 Automatic low-light detection and mode switching
	•	🔍 Noise reduction using Gaussian & Median filtering
	•	📈 Contrast enhancement for better visibility in dark
	•	🟩 Bounding box around detected motion
	•	⚡ Lightweight and fast (runs on webcam)
	•	🧠 Smart preview system (normal + low light mode)

⸻

🧠 How It Works
	1.	Captures frames from webcam
	2.	Converts frames to grayscale
	3.	Detects lighting using average brightness
	4.	Applies enhancement in low light
	5.	Computes frame difference to detect motion
	6.	Filters noise and highlights moving objects

⸻

🛠️ Tech Stack
	•	Python 🐍
	•	OpenCV 🎯
	•	NumPy 🔢

⸻

📂 Use Cases
	•	Security surveillance systems
	•	Smart monitoring in dark environments
	•	Basic computer vision projects
	•	SIP / Academic projects

⸻

▶️ How to Run

pip install opencv-python numpy
python main.py

Press ESC to exit.

⸻

💡 Future Improvements
	•	Night vision mode (green IR effect)
	•	Background subtraction (MOG2)
	•	Motion tracking with labels
	•	UI controls for mode switching

⸻

👨‍💻 Author

Aryan Chavan
