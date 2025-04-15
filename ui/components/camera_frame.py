import tkinter as tk
from PIL import Image, ImageTk
import cv2
import time

class CameraFrame(tk.Label):
    def __init__(self, parent, width=640, height=480, **kwargs):
        super().__init__(parent, **kwargs)
        self.width = width
        self.height = height
        self.cap = None
        self.video_running = False
        self.backends = [
            cv2.CAP_DSHOW,  # DirectShow (Windows)
            cv2.CAP_MSMF,   # Microsoft Media Foundation
            cv2.CAP_V4L2,   # Linux
            cv2.CAP_ANY     # Auto-detect
        ]
        self._setup_blank_frame()
        
    def _setup_blank_frame(self):
        blank = Image.new("RGB", (self.width, self.height), "black")
        self.blank_img = ImageTk.PhotoImage(blank)
        self.config(image=self.blank_img)
        
    def start_camera(self, camera_index=0):
        self.stop_camera()
        
        # Try different backends until one works
        for backend in self.backends:
            self.cap = cv2.VideoCapture(camera_index, backend)
            if self.cap.isOpened():
                break
        
        if not self.cap or not self.cap.isOpened():
            print("All camera backends failed")
            return False
            
        # Set camera properties
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        self.cap.set(cv2.CAP_PROP_FPS, 30)
        
        self.video_running = True
        self._update_frame()
        return True
        
    def stop_camera(self):
        self.video_running = False
        if self.cap:
            self.cap.release()
        self.cap = None
        self._setup_blank_frame()
        
    def _update_frame(self):
        if not self.video_running:
            return
            
        try:
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.resize(frame, (self.width, self.height))
                img = Image.fromarray(frame)
                imgtk = ImageTk.PhotoImage(image=img)
                self.imgtk = imgtk  # Keep reference
                self.config(image=imgtk)
        except Exception as e:
            print(f"Camera error: {str(e)}")
            self.stop_camera()
            return
            
        self.after(10, self._update_frame)
        
    def get_current_frame(self):
        if self.cap and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                return frame
        return None