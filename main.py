import os
import subprocess
import tkinter as tk
from threading import Thread

class GestureControllerDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Gesture Controller Dashboard")

        # Create buttons
        self.start_button = tk.Button(root, text="Start Gesture Controller", command=self.start_gesture_controller)
        self.start_button.pack(pady=12)

        self.stop_button = tk.Button(root, text="Stop Gesture Controller", command=self.stop_gesture_controller)
        self.stop_button.pack(pady=12)

        self.detected_gesture_label = tk.Label(root, text="Detected Gesture: ")
        self.detected_gesture_label.pack(pady=10)

        self.detected_gesture_text = tk.Label(root, text="", font=("Helvetica", 13))
        self.detected_gesture_text.pack(pady=10)

        # Create a text widget to display gesture actions
        self.gesture_text = tk.Text(root, height=10, width=50)
        self.gesture_text.pack(pady=10)

        # Initialize the process variable
        self.process = None

    def start_gesture_controller(self):
        if self.process is None or self.process.poll() is not None:
            # Start Gesture_Controller.py in a separate thread
            self.process = subprocess.Popen(["python", "Gesture_Controller.py"], stdout=subprocess.PIPE, universal_newlines=True)
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)

            # Start a thread to monitor gesture actions
            self.monitor_thread = Thread(target=self.monitor_detected_gestures)
            self.monitor_thread.start()

    def stop_gesture_controller(self):
        if self.process and self.process.poll() is None:
            # Terminate the Gesture_Controller.py process properly
            self.process.terminate()
            self.process.wait()
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)

    def update_gesture_text(self, gesture):
        # Append detected gesture to the text widget
        self.gesture_text.insert(tk.END, gesture + "\n")
        self.detected_gesture_text.config(text=gesture)
        #self.gesture_text.see(tk.END)

    def monitor_detected_gestures(self):
        while True:
            # Read detected gestures from the text file
            with open("detected_gestures.txt", "r") as file:
                detected_gesture = file.readline().strip()
            if detected_gesture:
                # Append detected gesture to the text widget
                self.gesture_text.insert(tk.END, detected_gesture + "\n")
                self.update_gesture_text(detected_gesture)
                #self.gesture_text.see(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    dashboard = GestureControllerDashboard(root)
    root.mainloop()




