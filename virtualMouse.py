import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import tkinter as tk
import threading


class VirtualMouseApp:
    def __init__(self):
        # Initialize variables
        self.cap = None  # Video capture object
        self.hand_detector = mp.solutions.hands.Hands()  # Hand detector object
        self.drawing_utils = mp.solutions.drawing_utils  # Drawing utilities for visualizing hand landmarks
        self.screen_width, self.screen_height = pyautogui.size()  # Screen dimensions
        self.index_y = 0  # Y-coordinate of the index finger
        self.index_x = 0  # X-coordinate of the index finger
        self.root = None  # Tkinter root window
        self.start_button = None  # Start button in the GUI
        self.exit_button = None  # Exit button in the GUI
        self.camera_thread = None  # Thread for camera loop
        self.running = False  # Flag to indicate if the application is running

    def run(self):
        # Create the main application window
        self.create_application_window()
        self.root.mainloop()

    def create_application_window(self):
        # Create the Tkinter root window
        self.root = tk.Tk()
        self.root.title("Virtual Mouse")
        self.root.geometry("350x350")
        self.root.configure(bg="light pink")

        # Add a welcome label to the root window
        self.add_welcome_label()

        # Add a Start button to the root window
        self.add_start_button()

        # Add an Exit button to the root window
        self.add_exit_button()

    def add_welcome_label(self):
        # Create a label widget to display a welcome message
        welcome_label = tk.Label(self.root, text="Welcome to Virtual Mouse", font=("Georgia", 16), bg="pink",
                                 fg="black")
        welcome_label.pack(pady=40)

    def add_start_button(self):
        # Create a Start button widget
        self.start_button = tk.Button(self.root, text="Start", font=("Verdana", 13), bg="light blue", fg="black",
                                      command=self.start_app, width=10)
        self.start_button.pack(pady=20)

    def add_exit_button(self):
        # Create an Exit button widget
        self.exit_button = tk.Button(self.root, text="Exit", font=("Verdana", 11), bg="white", fg="black",
                                     command=self.exit_app, state=tk.DISABLED, width=6)
        self.exit_button.pack(pady=15)

    def start_app(self):
        # Disable the Start button and enable the Exit button
        self.start_button.config(state=tk.DISABLED)
        self.exit_button.config(state=tk.NORMAL)

        # Start the camera loop in a separate thread
        self.camera_thread = threading.Thread(target=self.camera_loop)
        self.camera_thread.start()

    def camera_loop(self):
        # Set the running flag to True and open the camera
        self.running = True
        self.cap = cv2.VideoCapture(0)
        while self.running:
            # Capture a frame from the camera
            _, frame = self.cap.read()
            frame = cv2.flip(frame, 1)  # Flip the frame horizontally for intuitive motion tracking
            frame_height, frame_width, _ = frame.shape
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Process the frame using the hand detector
            output = self.hand_detector.process(rgb_frame)
            hands = output.multi_hand_landmarks
            if hands:
                for hand in hands:
                    # Draw hand landmarks on the frame
                    self.draw_hand_landmarks(frame, hand, frame_width, frame_height)

                    # Perform mouse actions based on hand gestures
                    self.perform_mouse_actions(hand, frame_width, frame_height)

            # Apply thresholding operation to the frame
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            _, thresholded_frame = cv2.threshold(gray_frame, 127, 255, cv2.THRESH_BINARY)

            # Display the thresholded frame
            cv2.imshow('Virtual Mouse', thresholded_frame)

            if cv2.waitKey(1) == ord('q'):
                break

        # Release the camera and close all windows
        self.cap.release()
        cv2.destroyAllWindows()
        self.start_button.config(state=tk.NORMAL)
        self.exit_button.config(state=tk.NORMAL)
        self.root.quit()

    def draw_hand_landmarks(self, frame, hand, frame_width, frame_height):
        # Draw hand landmarks on the frame
        self.drawing_utils.draw_landmarks(frame, hand, mp.solutions.hands.HAND_CONNECTIONS)
        landmarks = hand.landmark

        finger_contours = []
        for id_, landmark in enumerate(landmarks):
            x = int(landmark.x * frame_width)
            y = int(landmark.y * frame_height)
            finger_contours.append((x, y))

    def perform_mouse_actions(self, hand, frame_width, frame_height):
        landmarks = hand.landmark
        for id_, landmark in enumerate(landmarks):
            x = int(landmark.x * frame_width)
            y = int(landmark.y * frame_height)

            if id_ == 8:
                index_x = self.screen_width / frame_width * x
                self.index_y = self.screen_height / frame_height * y
                pyautogui.moveTo(index_x, self.index_y)

            if id_ == 4:
                thumb_y = self.screen_height / frame_height * y
                if abs(self.index_y - thumb_y) < 30:
                    pyautogui.click()
                    pyautogui.sleep(1)
                elif abs(self.index_y - thumb_y) < 100:
                    pyautogui.moveTo(self.index_x, self.index_y)

            if id_ == 12:
                middle_x = self.screen_width / frame_width * x
                middle_y = self.screen_height / frame_height * y
                if abs(self.index_y - middle_y) < 30:
                    pyautogui.scroll(30)

    def exit_app(self):
        # Set the running flag to False, release the camera, close all windows, and destroy the application window
        self.running = False
        self.cap.release()
        cv2.destroyAllWindows()
        self.root.destroy()


if __name__ == '__main__':
    app = VirtualMouseApp()
    app.run()
