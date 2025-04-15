import tkinter as tk
from tkinter import ttk
from models.attendance import get_attendance_records

class RecordsView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self._setup_ui()
        self.load_records()
        
    def _setup_ui(self):
        """Initialize all UI components"""
        # Search frame
        search_frame = ttk.Frame(self)
        search_frame.pack(fill="x", pady=10)
        
        self.search_entry = ttk.Entry(search_frame)
        self.search_entry.pack(side=tk.LEFT, padx=5, expand=True, fill="x")
        
        search_btn = ttk.Button(
            search_frame,
            text="Search",
            command=self.load_records
        )
        search_btn.pack(side=tk.LEFT, padx=5)
        
        # Treeview with scrollbars
        tree_frame = ttk.Frame(self)
        tree_frame.pack(fill="both", expand=True)
        
        self.tree = ttk.Treeview(
            tree_frame,
            columns=("ID", "Name", "Time"),
            show="headings"
        )
        self.tree.pack(side=tk.LEFT, fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Configure columns
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Time", text="Time")
        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Name", width=150)
        self.tree.column("Time", width=200)
        
        # Refresh button
        refresh_btn = ttk.Button(
            self,
            text="Refresh",
            command=self.load_records
        )
        refresh_btn.pack(pady=10)
    
    def load_records(self):
        """Load attendance records into the treeview"""
        # Clear existing records
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Get search term if any
        search_term = self.search_entry.get().strip() or None
        
        # Fetch and display records
        records = get_attendance_records(search_term)
        for record in records:
            self.tree.insert("", "end", values=record)