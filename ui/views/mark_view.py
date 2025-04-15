import tkinter as tk
from tkinter import ttk, messagebox
from ui.components.camera_frame import CameraFrame
from services.face_service import FaceService
from models.attendance import mark_attendance
import time

class MarkView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.face_service = FaceService()
        self.last_attendance_time = 0
        self.attendance_cooldown = 5  # seconds
        self._setup_ui()
        
    def _setup_ui(self):
        """Initialize all UI components"""
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
        
        # Camera frame with card styling
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
        
        # Recent attendance card
        recent_card = ttk.Frame(content, style="Card.TFrame", padding=15)
        recent_card.grid(row=2, column=0, sticky="ew")
        
        ttk.Label(
            recent_card,
            text="Recent Attendance",
            style="CardTitle.TLabel"
        ).pack(anchor="w", pady=(0, 10))
        
        # Recent attendance list
        self.recent_list = ttk.Treeview(
            recent_card,
            columns=("name", "time"),
            show="headings",
            height=4
        )
        self.recent_list.heading("name", text="Name")
        self.recent_list.heading("time", text="Time")
        self.recent_list.column("name", width=150, anchor="w")
        self.recent_list.column("time", width=200, anchor="w")
        self.recent_list.pack(fill="x")
        
        # Success animation label
        self.success_label = ttk.Label(
            self,
            style="Success.TLabel",
            text=""
        )
        
    def start_scanning(self):
        """Start the attendance marking process"""
        if not self.camera.start_camera():
            messagebox.showerror(
                "Camera Error", 
                "Could not access camera.\n"
                "1. Make sure camera is connected\n"
                "2. Check if another app is using the camera\n"
                "3. Verify camera permissions"
            )
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
                locations, names = self.face_service.recognize_faces(frame)
                
                for i, name in enumerate(names):
                    if name != "Unknown":
                        # Check cooldown period
                        if current_time - self.last_attendance_time > self.attendance_cooldown:
                            mark_attendance(name)
                            self.last_attendance_time = current_time
                            self._show_success(name)
                            self._update_recent_list(name)
                            break  # Only mark one person per frame
            except Exception as e:
                print(f"Recognition error: {str(e)}")
        
        self.after(100, self._update_attendance)
    
    def _show_success(self, name):
        """Show success animation"""
        self.success_label.config(text=f"{name} marked ✓")
        self.success_label.place(relx=0.5, rely=0.5, anchor="center")
        self.success_label.lift()
        
        # Fade in
        for i in range(0, 101, 10):
            alpha = i/100
            self.success_label.config(foreground=self._interpolate_color(
                "#A3BE8C", alpha
            ))
            self.update()
            self.after(20)
        
        # Hold and fade out
        self.after(800)
        for i in range(100, -1, -10):
            alpha = i/100
            self.success_label.config(foreground=self._interpolate_color(
                "#A3BE8C", alpha
            ))
            self.update()
            self.after(20)
        
        self.success_label.place_forget()
    
    def _interpolate_color(self, hex_color, alpha):
        """Helper for color animation"""
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (1, 3, 5))
        return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}" if alpha == 1 else \
               f"#{int(rgb[0]*alpha):02x}{int(rgb[1]*alpha):02x}{int(rgb[2]*alpha):02x}"
    
    def _update_recent_list(self, name):
        """Update the recent attendance list"""
        self.recent_list.insert("", 0, values=(name, time.strftime("%Y-%m-%d %H:%M:%S")))
        if len(self.recent_list.get_children()) > 5:
            self.recent_list.delete(self.recent_list.get_children()[-1])
    
    def stop_camera(self):
        """Stop the camera when closing"""
        self.stop_scanning()