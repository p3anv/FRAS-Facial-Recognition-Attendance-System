import tkinter as tk
from tkinter import ttk, messagebox
import time
from ui.components.camera_frame import CameraFrame
from services.face_service import FaceService
from models.database import mark_attendance

class MarkView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.face_service = FaceService()
        self.last_attendance_time = 0
        self.attendance_cooldown = 5  # seconds
        self._setup_ui()
        
    def _setup_ui(self):
        """Initialize UI components"""
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Header
        header = ttk.Frame(self, padding=(0, 0, 0, 10))
        header.grid(row=0, column=0, sticky="ew")
        
        ttk.Label(
            header,
            text="Mark Attendance",
            font=("Segoe UI", 16, "bold"),
            foreground="#2E3440"
        ).pack(side="left")
        
        # Status indicator
        self.status_var = tk.StringVar(value="Ready")
        ttk.Label(
            header,
            textvariable=self.status_var,
            style="Status.TLabel"
        ).pack(side="right")
        
        # Main content
        content = ttk.Frame(self)
        content.grid(row=1, column=0, sticky="nsew")
        content.grid_columnconfigure(0, weight=1)
        content.grid_rowconfigure(0, weight=1)
        
        # Camera frame
        cam_card = ttk.Frame(content, style="Card.TFrame", padding=10)
        cam_card.grid(row=0, column=0, sticky="nsew", pady=(0, 15))
        cam_card.grid_columnconfigure(0, weight=1)
        cam_card.grid_rowconfigure(0, weight=1)
        
        self.camera = CameraFrame(cam_card)
        self.camera.grid(row=0, column=0, sticky="nsew")
        
        # Control buttons
        btn_frame = ttk.Frame(content)
        btn_frame.grid(row=1, column=0, sticky="ew", pady=(0, 15))
        
        self.start_btn = ttk.Button(
            btn_frame,
            text="Start Scanning",
            command=self.start_scanning,
            style="TButton"
        )
        self.start_btn.pack(side="left", padx=(0, 5))
        
        self.stop_btn = ttk.Button(
            btn_frame,
            text="Stop",
            command=self.stop_scanning,
            state="disabled",
            style="TButton"
        )
        self.stop_btn.pack(side="left")
        
        # Recent attendance list
        recent_card = ttk.Frame(content, style="Card.TFrame", padding=15)
        recent_card.grid(row=2, column=0, sticky="ew")
        
        ttk.Label(
            recent_card,
            text="Recent Attendance",
            style="CardTitle.TLabel"
        ).pack(anchor="w", pady=(0, 10))
        
        self.recent_list = ttk.Treeview(
            recent_card,
            columns=("roll_number", "name", "time"),
            show="headings",
            height=4
        )
        self.recent_list.heading("roll_number", text="Roll Number")
        self.recent_list.heading("name", text="Name")
        self.recent_list.heading("time", text="Time")
        self.recent_list.column("roll_number", width=100, anchor="w")
        self.recent_list.column("name", width=150, anchor="w")
        self.recent_list.column("time", width=120, anchor="w")
        self.recent_list.pack(fill="x")
    
    def start_scanning(self):
        """Start the attendance marking process"""
        if not self.camera.start_camera():
            messagebox.showerror("Error", "Could not start camera")
            return
            
        self.start_btn.config(state="disabled")
        self.stop_btn.config(state="normal")
        self.status_var.set("Scanning for faces...")
        self._update_attendance()
    
    def stop_scanning(self):
        """Stop the attendance marking process"""
        self.start_btn.config(state="normal")
        self.stop_btn.config(state="disabled")
        self.camera.stop_camera()
        self.status_var.set("Ready")
    
    def _update_attendance(self):
        """Continuously check for faces and mark attendance"""
        if self.stop_btn["state"] == "disabled":
            return
            
        current_time = time.time()
        frame = self.camera.get_current_frame()
        
        if frame is not None:
            try:
                locations, roll_numbers, names = self.face_service.recognize_faces(frame)
                
                for i, roll_number in enumerate(roll_numbers):
                    if roll_number != "Unknown":
                        if current_time - self.last_attendance_time > self.attendance_cooldown:
                            mark_attendance(roll_number, names[i])
                            self.last_attendance_time = current_time
                            self._show_success(names[i])
                            self._update_recent_list(roll_number, names[i])
                            break
            except Exception as e:
                print(f"Recognition error: {str(e)}")
        
        self.after(100, self._update_attendance)
    
    def _show_success(self, name):
        """Show success animation"""
        self.status_var.set(f"{name} marked present")
        self.after(2000, lambda: self.status_var.set("Scanning for faces..."))
    
    def _update_recent_list(self, roll_number, name):
        """Update the recent attendance list"""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        self.recent_list.insert("", 0, values=(roll_number, name, timestamp))
        if len(self.recent_list.get_children()) > 5:
            self.recent_list.delete(self.recent_list.get_children()[-1])
    
    def stop_camera(self):
        """Clean up camera resources"""
        self.stop_scanning()