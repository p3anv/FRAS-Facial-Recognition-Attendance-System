import tkinter as tk
from tkinter import ttk
from ui.register_view import RegisterView
from ui.views.mark_view import MarkView
from ui.views.records_view import RecordsView
from ui.styles import configure_styles, get_colors
from models.database import init_db
from models.database import init_db

class AttendanceApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # Initialize database
        init_db()
        
        # Configure styles
        configure_styles()
        colors = get_colors()
        
        # Main window setup
        self.title("Facial Recognition Attendance System")
        self.geometry("1200x800")
        self.minsize(1000, 700)
        self.configure(background=colors["background"])
        
        # Main container
        self.main_container = ttk.Frame(self)
        self.main_container.pack(fill="both", expand=True, padx=20, pady=20)
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_rowconfigure(1, weight=1)
        
        # Header
        header = ttk.Frame(self.main_container)
        header.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        
        ttk.Label(
            header,
            text="Facial Recognition Attendance",
            font=("Segoe UI", 24, "bold"),
            foreground=colors["text"]
        ).pack(side="left")
        
        # Tab control
        self.tab_control = ttk.Notebook(self.main_container)
        self.tab_control.grid(row=1, column=0, sticky="nsew")
        
        # Create tabs
        self.register_view = RegisterView(self.tab_control)
        self.mark_view = MarkView(self.tab_control)
        self.records_view = RecordsView(self.tab_control)
        
        # Add tabs with icons
        self.tab_control.add(self.register_view, text=" Register Face ")
        self.tab_control.add(self.mark_view, text=" Mark Attendance ")
        self.tab_control.add(self.records_view, text=" View Records ")
        
        # Status bar
        self.status_bar = ttk.Frame(self.main_container, height=25)
        self.status_bar.grid(row=2, column=0, sticky="ew", pady=(10, 0))
        
        ttk.Label(
            self.status_bar,
            text="Ready",
            style="Status.TLabel"
        ).pack(side="left", padx=5)
        
        # Handle window closing
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def on_closing(self):
        """Clean up resources when closing"""
        self.register_view.stop_camera()
        self.mark_view.stop_camera()
        self.destroy()

if __name__ == "__main__":
    app = AttendanceApp()
    app.mainloop()