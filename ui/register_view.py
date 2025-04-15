# attendance_system/ui/views/register_view.py
import tkinter as tk
from tkinter import ttk, messagebox
from ui.components.camera_frame import CameraFrame
from services.face_service import FaceService

class RegisterView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.face_service = FaceService()
        
        # Paste the camera initialization code here:
        self.camera = CameraFrame(self)
        self.camera.pack(pady=10)

        self.btn_start_cam = ttk.Button(
            self, 
            text="Start Camera", 
            command=self._start_camera
        )
        self.btn_start_cam.pack(pady=5)
        
        # Rest of your existing code (name entry, capture button, etc.)
        self.name_entry = ttk.Entry(self, width=30)
        self.name_entry.pack(pady=5)
        
        self.capture_btn = ttk.Button(
            self,
            text="Capture Face",
            command=self._register_face,
            state="disabled"  # Disabled until camera starts
        )
        self.capture_btn.pack(pady=5)

    # Paste the _start_camera method here:
    def _start_camera(self):
        if not self.camera.start_camera():
            messagebox.showerror(
                "Camera Error", 
                "Could not access camera.\n"
                "1. Make sure camera is connected\n"
                "2. Check if another app is using the camera\n"
                "3. Verify camera permissions"
            )
        else:
            self.capture_btn.config(state="normal")  # Enable capture button

    # Keep your existing _register_face method
    def _register_face(self):
        """Handle face registration"""
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showerror("Error", "Please enter a name")
            return

        frame = self.camera.get_current_frame()
        if frame is None:
            messagebox.showerror("Error", "Could not capture frame")
            return

        try:
            self.face_service.register_face(name, frame)
            messagebox.showinfo("Success", f"Face registered for {name}")
            self.name_entry.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to register face: {str(e)}")

    def stop_camera(self):
        """Stop the camera feed"""
        self.camera.stop_camera()
        self.capture_btn.config(state="disabled")  # Disable capture button