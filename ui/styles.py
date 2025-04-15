import tkinter as tk
from tkinter import ttk

COLORS = {
    "primary": "#5E81AC",    # Soft blue
    "secondary": "#81A1C1",  # Lighter blue
    "accent": "#88C0D0",     # Teal accent
    "background": "#ECEFF4", # Light gray
    "card": "#E5E9F0",       # Card background
    "text": "#2E3440",       # Dark text
    "text_secondary": "#4C566A",  # Secondary text
    "success": "#A3BE8C",    # Soft green
    "warning": "#EBCB8B",    # Soft yellow
    "error": "#BF616A",      # Soft red
    "border": "#D8DEE9"      # Borders
}

FONTS = {
    "title": ("Segoe UI", 18, "bold"),
    "subtitle": ("Segoe UI", 14),
    "body": ("Segoe UI", 11),
    "caption": ("Segoe UI", 9)
}

def configure_styles():
    style = ttk.Style()
    
    # Base styles
    style.theme_create("nord", parent="alt", settings={
        ".": {
            "configure": {
                "background": COLORS["background"],
                "foreground": COLORS["text"],
                "font": FONTS["body"]
            }
        },
        "TFrame": {
            "configure": {
                "background": COLORS["background"],
                "borderwidth": 0
            }
        },
        "TNotebook": {
            "configure": {
                "background": COLORS["background"],
                "borderwidth": 0,
                "padding": [5, 5, 5, 5]
            }
        },
        "TNotebook.Tab": {
            "configure": {
                "padding": [15, 5],
                "background": COLORS["card"],
                "font": FONTS["subtitle"]
            },
            "map": {
                "background": [("selected", COLORS["background"])],
                "expand": [("selected", [1, 1, 1, 0])]
            }
        },
        "TButton": {
            "configure": {
                "background": COLORS["primary"],
                "foreground": "white",
                "borderwidth": 0,
                "padding": 10,
                "font": FONTS["body"]
            },
            "map": {
                "background": [
                    ("active", COLORS["secondary"]),
                    ("disabled", COLORS["border"])
                ]
            }
        },
        "Hover.TButton": {
            "configure": {
                "background": COLORS["accent"]
            }
        },
        "TEntry": {
            "configure": {
                "fieldbackground": "white",
                "bordercolor": COLORS["border"],
                "lightcolor": COLORS["border"],
                "darkcolor": COLORS["border"],
                "padding": 8,
                "insertwidth": 2
            },
            "map": {
                "bordercolor": [
                    ("focus", COLORS["accent"]),
                    ("!focus", COLORS["border"])
                ]
            }
        },
        "Card.TFrame": {
            "configure": {
                "background": COLORS["card"],
                "borderwidth": 1,
                "relief": "solid"
            }
        },
        "CardTitle.TLabel": {
            "configure": {
                "background": COLORS["card"],
                "font": FONTS["subtitle"],
                "foreground": COLORS["text"]
            }
        },
        "Status.TLabel": {
            "configure": {
                "font": FONTS["caption"],
                "foreground": COLORS["text_secondary"]
            }
        },
        "Success.TLabel": {
            "configure": {
                "foreground": COLORS["success"],
                "font": ("Segoe UI", 24, "bold")
            }
        },
        "Treeview": {
            "configure": {
                "background": "white",
                "fieldbackground": "white",
                "rowheight": 28
            }
        },
        "Treeview.Heading": {
            "configure": {
                "background": COLORS["primary"],
                "foreground": "white",
                "padding": [10, 5],
                "font": FONTS["body"]
            }
        }
    })
    
    style.theme_use("nord")
    
    # Additional custom styles
    style.configure("Horizontal.TSeparator", background=COLORS["border"])

def get_colors():
    return COLORS

def get_fonts():
    return FONTS