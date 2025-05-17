# 🖱️ Virtual Mouse

Control your computer using hand gestures! This Python-based virtual mouse uses your webcam to track hand movements and simulate mouse actions like move, click, and scroll — all without touching a physical mouse.

## 🚀 Features

* Hand gesture recognition using **MediaPipe**
* Real-time webcam input via **OpenCV**
* Mouse control with **PyAutoGUI**
* GUI interface with **Tkinter**
* Supports:

  * Cursor movement
  * Left click (thumb + index)
  * Scroll gesture

## 🛠️ Technologies Used

* Python 3
* OpenCV
* MediaPipe
* PyAutoGUI
* NumPy
* Tkinter

## 📦 Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/virtual-mouse.git
   cd virtual-mouse
   ```

2. **Install dependencies:**

   ```bash
   pip install opencv-python mediapipe pyautogui numpy
   ```

3. **Run the application:**

   ```bash
   python virtualMouse.py
   ```

## 📷 Usage

1. Click **Start** to activate your webcam.
2. Use hand gestures to move the cursor.
3. Pinch (thumb + index) to click, or raise your middle finger close to the index to scroll.
4. Press `q` or click **Exit** to stop.

## 🧠 How It Works

* Uses MediaPipe to detect hand landmarks.
* Maps the index finger’s tip to screen coordinates.
* Detects finger distance to trigger mouse actions.

## 📌 Notes

* Make sure your webcam is working.
* Run in a well-lit environment for best accuracy.
