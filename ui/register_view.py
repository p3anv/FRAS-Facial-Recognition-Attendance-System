import tkinter as tk
from tkinter import ttk, messagebox
import os
import cv2
import time
from ui.components.camera_frame import CameraFrame
from services.face_service import FaceService
from models.database import get_db_connection
from models.database import get_db_connection

class RegisterView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.face_service = FaceService()
        self.capture_count = 0
        self.MAX_CAPTURES = 25  # Number of images to capture
        self._setup_ui()
        
    def _setup_ui(self):
        """Initialize all UI components"""
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Form Frame
        form_frame = ttk.Frame(self, style="Card.TFrame", padding=15)
        form_frame.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        
        # Student Information
        ttk.Label(form_frame, text="Student Information", style="CardTitle.TLabel").grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 10))
        
        # First Name
        ttk.Label(form_frame, text="First Name:").grid(row=1, column=0, sticky="w", padx=(0, 10), pady=5)
        self.first_name = ttk.Entry(form_frame)
        self.first_name.grid(row=1, column=1, sticky="ew", pady=5)
        
        # Last Name
        ttk.Label(form_frame, text="Last Name:").grid(row=2, column=0, sticky="w", padx=(0, 10), pady=5)
        self.last_name = ttk.Entry(form_frame)
        self.last_name.grid(row=2, column=1, sticky="ew", pady=5)
        
        # Roll Number
        ttk.Label(form_frame, text="Roll Number:").grid(row=3, column=0, sticky="w", padx=(0, 10), pady=5)
        self.roll_number = ttk.Entry(form_frame)
        self.roll_number.grid(row=3, column=1, sticky="ew", pady=5)
        
        # Department
        ttk.Label(form_frame, text="Department:").grid(row=4, column=0, sticky="w", padx=(0, 10), pady=5)
        self.department = ttk.Combobox(form_frame, values=["CSE", "ESE", "MECH", "CIVIL"])
        self.department.current(0)  # Default to CSE
        self.department.grid(row=4, column=1, sticky="ew", pady=5)
        
        # Camera Frame
        cam_card = ttk.Frame(self, style="Card.TFrame", padding=10)
        cam_card.grid(row=1, column=0, sticky="nsew")
        cam_card.grid_columnconfigure(0, weight=1)
        cam_card.grid_rowconfigure(0, weight=1)
        
        self.camera = CameraFrame(cam_card)
        self.camera.grid(row=0, column=0, sticky="nsew")
        
        # Control Buttons
        btn_frame = ttk.Frame(self)
        btn_frame.grid(row=2, column=0, sticky="ew", pady=(15, 0))
        
        self.start_btn = ttk.Button(
            btn_frame,
            text="Start Camera",
            command=self.start_camera
        )
        self.start_btn.pack(side="left", padx=(0, 5))
        
        self.stop_btn = ttk.Button(
            btn_frame,
            text="Stop Camera",
            command=self.stop_camera,
            state="disabled"
        )
        self.stop_btn.pack(side="left", padx=(0, 5))
        
        self.capture_btn = ttk.Button(
            btn_frame,
            text="Capture Face (0/25)",
            command=self.capture_face,
            state="disabled"
        )
        self.capture_btn.pack(side="left")
        
        # Progress Bar
        self.progress = ttk.Progressbar(
            btn_frame,
            orient="horizontal",
            mode="determinate",
            maximum=self.MAX_CAPTURES
        )
        self.progress.pack(side="left", padx=(10, 0), fill="x", expand=True)
        
        # Status Label
        self.status = ttk.Label(self, style="Status.TLabel")
        self.status.grid(row=3, column=0, sticky="ew", pady=(10, 0))
    
    def start_camera(self):
        """Start the camera feed"""
        if not self.camera.start_camera():
            messagebox.showerror("Error", "Could not start camera")
            return
            
        self.start_btn.config(state="disabled")
        self.stop_btn.config(state="normal")
        self.capture_btn.config(state="normal")
        self.capture_count = 0
        self._update_capture_button()
        self.status.config(text="Camera started - Face the camera directly")
    
    def stop_camera(self):
        """Stop the camera feed"""
        self.camera.stop_camera()
        self.start_btn.config(state="normal")
        self.stop_btn.config(state="disabled")
        self.capture_btn.config(state="disabled")
        self.status.config(text="Camera stopped")
    
    def capture_face(self):
        """Capture multiple face samples"""
        # Validate form
        if not all([
            self.first_name.get(),
            self.last_name.get(),
            self.roll_number.get()
        ]):
            messagebox.showerror("Error", "Please fill all fields")
            return
            
        frame = self.camera.get_current_frame()
        if frame is None:
            messagebox.showerror("Error", "Could not capture frame")
            return
            
        # Create student directory
        student_id = f"{self.roll_number.get()}_{self.first_name.get()}_{self.last_name.get()}"
        os.makedirs(f"faces/{student_id}", exist_ok=True)
        
        # Save image with timestamp
        timestamp = int(time.time() * 1000)
        img_path = f"faces/{student_id}/{timestamp}_{self.capture_count}.jpg"
        cv2.imwrite(img_path, frame)
        
        # Update progress
        self.capture_count += 1
        self._update_capture_button()
        self.progress["value"] = self.capture_count
        
        # Provide feedback
        self.status.config(text=f"Captured sample {self.capture_count}/{self.MAX_CAPTURES}")
        
        # Auto-stop when done
        if self.capture_count >= self.MAX_CAPTURES:
            self._save_student_data()
            self.stop_camera()
            messagebox.showinfo("Success", f"Successfully registered {self.first_name.get()}")
            self._reset_form()
    
    def _update_capture_button(self):
        """Update capture button text"""
        self.capture_btn.config(text=f"Capture Face ({self.capture_count}/{self.MAX_CAPTURES})")
    
    def _save_student_data(self):
        """Save student info to database"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS students
                       (id INTEGER PRIMARY KEY AUTOINCREMENT,
                        first_name TEXT,
                        last_name TEXT,
                        roll_number TEXT UNIQUE,
                        department TEXT)''')
        
        cursor.execute('''INSERT INTO students 
                       (first_name, last_name, roll_number, department)
                       VALUES (?, ?, ?, ?)''',
                       (self.first_name.get(),
                        self.last_name.get(),
                        self.roll_number.get(),
                        self.department.get()))
        conn.commit()
        conn.close()
    
    def _reset_form(self):
        """Reset the registration form"""
        self.first_name.delete(0, tk.END)
        self.last_name.delete(0, tk.END)
        self.roll_number.delete(0, tk.END)
        self.department.current(0)
        self.capture_count = 0
        self._update_capture_button()
        self.progress["value"] = 0
        self.status.config(text="Ready for new registration")
    
    def stop_camera(self):
        """Clean up camera resources"""
        self.camera.stop_camera()
        self.start_btn.config(state="normal")
        self.stop_btn.config(state="disabled")
        self.capture_btn.config(state="disabled")