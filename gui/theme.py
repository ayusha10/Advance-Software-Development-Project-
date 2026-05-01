import tkinter as tk
from tkinter import ttk

class Theme:
    # Color Palette (Catppuccin Mocha inspired)
    BG_DARK = "#1e1e2e"
    BG_LIGHT = "#313244"
    FG_MAIN = "#cdd6f4"
    ACCENT_BLUE = "#89b4fa"
    ACCENT_GREEN = "#a6e3a1"
    ACCENT_RED = "#f38ba8"
    ACCENT_YELLOW = "#f9e2af"
    ACCENT_MAUVE = "#cba6f7"
    
    FONT_MAIN = ("Segoe UI", 10)
    FONT_BOLD = ("Segoe UI", 10, "bold")
    FONT_TITLE = ("Segoe UI", 18, "bold")

    @staticmethod
    def apply(root):
        style = ttk.Style(root)
        style.theme_use('clam')

        # Global Colors
        root.configure(bg=Theme.BG_DARK)

        # Frame Style
        style.configure("TFrame", background=Theme.BG_DARK)
        
        # Label Style
        style.configure("TLabel", 
                        background=Theme.BG_DARK, 
                        foreground=Theme.FG_MAIN, 
                        font=Theme.FONT_MAIN,
                        anchor="center")
        
        style.configure("Header.TLabel", 
                        font=Theme.FONT_TITLE, 
                        foreground=Theme.ACCENT_BLUE,
                        anchor="center")

        # Button Style
        style.configure("TButton", 
                        background=Theme.BG_LIGHT, 
                        foreground=Theme.FG_MAIN, 
                        font=Theme.FONT_BOLD,
                        borderwidth=0,
                        focuscolor=Theme.ACCENT_BLUE)
        
        style.map("TButton", 
                  background=[('active', Theme.ACCENT_BLUE)],
                  foreground=[('active', Theme.BG_DARK)])

        # Accent Buttons
        style.configure("Accent.TButton", background=Theme.ACCENT_BLUE, foreground=Theme.BG_DARK)
        style.configure("Danger.TButton", background=Theme.ACCENT_RED, foreground=Theme.BG_DARK)
        style.configure("Success.TButton", background=Theme.ACCENT_GREEN, foreground=Theme.BG_DARK)

        # Notebook (Tabs) Style
        style.configure("TNotebook", background=Theme.BG_DARK, borderwidth=0)
        style.configure("TNotebook.Tab", 
                        background=Theme.BG_LIGHT, 
                        foreground=Theme.FG_MAIN, 
                        padding=[15, 5],
                        font=Theme.FONT_BOLD)
        style.map("TNotebook.Tab", 
                  background=[('selected', Theme.ACCENT_BLUE)],
                  foreground=[('selected', Theme.BG_DARK)])

        # Treeview (Table) Style
        style.configure("Treeview", 
                        background=Theme.BG_LIGHT, 
                        foreground=Theme.FG_MAIN, 
                        fieldbackground=Theme.BG_LIGHT,
                        rowheight=30,
                        font=Theme.FONT_MAIN,
                        borderwidth=0)
        style.configure("Treeview.Heading", 
                        background=Theme.BG_DARK, 
                        foreground=Theme.ACCENT_BLUE, 
                        font=Theme.FONT_BOLD,
                        borderwidth=1)
        style.map("Treeview", 
                  background=[('selected', Theme.ACCENT_BLUE)],
                  foreground=[('selected', Theme.BG_DARK)])

        # Entry Style
        style.configure("TEntry", 
                        fieldbackground=Theme.BG_LIGHT, 
                        foreground=Theme.FG_MAIN, 
                        borderwidth=0)

        # Combobox Style
        style.configure("TCombobox", 
                        fieldbackground=Theme.BG_LIGHT, 
                        background=Theme.BG_LIGHT, 
                        foreground=Theme.FG_MAIN)
