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
        self.start_button.pack(pady=10)

        self.stop_button = tk.Button(root, text="Stop Gesture Controller", command=self.stop_gesture_controller)
        self.stop_button.pack(pady=10)

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
            self.monitor_thread = Thread(target=self.monitor_gesture_actions)
            self.monitor_thread.start()

    def stop_gesture_controller(self):
        if self.process and self.process.poll() is None:
            # Terminate the Gesture_Controller.py process properly
            self.process.terminate()
            self.process.wait()
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)

    def monitor_gesture_actions(self):
         while True:
            line = self.process.stdout.readline().strip()
            if not line:
                break
            # Append detected gesture to the text widget
            self.gesture_text.insert(tk.END, line + "\n")
            self.gesture_text.see(tk.END)

            # Get detected gestures from the GestureController and display them
            detected_gestures = self.gesture_controller.detected_gestures
            self.gesture_text.insert(tk.END, f"Detected Gestures: {', '.join(detected_gestures)}\n")
            self.gesture_text.see(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    dashboard = GestureControllerDashboard(root)
    root.mainloop()





