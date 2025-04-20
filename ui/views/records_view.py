import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from models.database import get_attendance_records
from ui.styles import COLORS
import datetime

class RecordsView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self._setup_ui()
        self.load_records()

    def _setup_ui(self):
        """Initialize all UI components"""
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Search Frame
        search_frame = ttk.Frame(self, padding=(0, 0, 0, 15))
        search_frame.grid(row=0, column=0, sticky="ew")

        # Search Label and Entry
        ttk.Label(
            search_frame,
            text="Search:",
            style="TLabel"
        ).pack(side="left", padx=(0, 5))

        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(
            search_frame,
            textvariable=self.search_var,
            width=40
        )
        self.search_entry.pack(side="left", expand=True, fill="x", padx=(0, 5))
        self.search_entry.bind("<Return>", lambda e: self.load_records())

        # Search Button
        search_btn = ttk.Button(
            search_frame,
            text="Search",
            command=self.load_records,
            style="TButton"
        )
        search_btn.pack(side="left", padx=(0, 5))

        # Clear Button
        clear_btn = ttk.Button(
            search_frame,
            text="Clear",
            command=self.clear_search,
            style="TButton"
        )
        clear_btn.pack(side="left")

        # Export Button
        export_btn = ttk.Button(
            search_frame,
            text="Export CSV",
            command=self.export_to_csv,
            style="TButton"
        )
        export_btn.pack(side="right")

        # Treeview Frame
        tree_frame = ttk.Frame(self)
        tree_frame.grid(row=1, column=0, sticky="nsew")
        tree_frame.grid_columnconfigure(0, weight=1)
        tree_frame.grid_rowconfigure(0, weight=1)

        # Treeview with Scrollbars
        self.tree = ttk.Treeview(
            tree_frame,
            columns=("roll_no", "first_name", "last_name", "department", "time"),
            show="headings",
            selectmode="extended",
            height=15
        )

        # Configure Columns
        self.tree.heading("roll_no", text="Roll No", anchor="w")
        self.tree.heading("first_name", text="First Name", anchor="w")
        self.tree.heading("last_name", text="Last Name", anchor="w")
        self.tree.heading("department", text="Department", anchor="w")
        self.tree.heading("time", text="Timestamp", anchor="w")

        self.tree.column("roll_no", width=100, stretch=False)
        self.tree.column("first_name", width=150, stretch=False)
        self.tree.column("last_name", width=150, stretch=False)
        self.tree.column("department", width=100, stretch=False)
        self.tree.column("time", width=180, stretch=False)

        # Scrollbars
        y_scroll = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        x_scroll = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)

        # Grid Layout
        self.tree.grid(row=0, column=0, sticky="nsew")
        y_scroll.grid(row=0, column=1, sticky="ns")
        x_scroll.grid(row=1, column=0, sticky="ew")

        # Status Bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(
            self,
            textvariable=self.status_var,
            relief="sunken",
            anchor="w",
            style="Status.TLabel"
        )
        status_bar.grid(row=2, column=0, sticky="ew", pady=(10, 0))

        # Refresh Button
        refresh_btn = ttk.Button(
            self,
            text="Refresh",
            command=self.load_records,
            style="TButton"
        )
        refresh_btn.grid(row=3, column=0, pady=(10, 0))

    def load_records(self):
        """Load attendance records into the treeview"""
        try:
            # Clear existing records
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Get records from database
            records = get_attendance_records(
                search_term=self.search_var.get() or None
            )

            # Add records to treeview
            for record in records:
                self.tree.insert("", "end", values=record)

            # Update status
            count = len(self.tree.get_children())
            self.status_var.set(f"Showing {count} records | Last updated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load records: {str(e)}")

    def clear_search(self):
        """Clear search field and reload records"""
        self.search_var.set("")
        self.load_records()

    def export_to_csv(self):
        """Export attendance records to CSV file"""
        try:
            records = get_attendance_records()
            if not records:
                messagebox.showwarning("Warning", "No records to export")
                return

            filename = f"attendance_export_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            with open(filename, "w") as f:
                # Write header
                f.write("Roll No,First Name,Last Name,Department,Timestamp\n")
                
                # Write records
                for record in records:
                    f.write(f"{record[0]},{record[1]},{record[2]},{record[3]},{record[4]}\n")

            messagebox.showinfo("Success", f"Records exported to {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Export failed: {str(e)}")