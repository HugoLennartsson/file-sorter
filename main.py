import tkinter as tk
from tkinter import messagebox, font
from settings_gui import SettingsApp
from sorter_engine import SorterInstance
import threading
import json


class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Auto File Sorter Pro")
        self.root.geometry("450x500")
        self.root.resizable(False, False)

        # Modern color scheme
        self.colors = {
            "bg": "#f5f5f5",
            "card_bg": "#ffffff",
            "primary": "#2196F3",
            "primary_hover": "#1976D2",
            "success": "#4CAF50",
            "success_hover": "#388E3C",
            "danger": "#f44336",
            "danger_hover": "#d32f2f",
            "text_primary": "#333333",
            "text_secondary": "#666666",
            "border": "#e0e0e0",
        }

        # Set background
        self.root.configure(bg=self.colors["bg"])

        # Modern fonts
        self.font_title = font.Font(family="Segoe UI", size=18, weight="bold")
        self.font_heading = font.Font(family="Segoe UI", size=12, weight="bold")
        self.font_normal = font.Font(family="Segoe UI", size=10)
        self.font_button = font.Font(family="Segoe UI", size=10, weight="bold")

        self.sorter = SorterInstance()

        # Main container with padding
        main_frame = tk.Frame(root, bg=self.colors["bg"])
        main_frame.pack(fill="both", expand=True, padx=30, pady=25)

        # Header
        header_frame = tk.Frame(main_frame, bg=self.colors["bg"])
        header_frame.pack(fill="x", pady=(0, 20))

        tk.Label(
            header_frame,
            text="Auto File Sorter",
            font=self.font_title,
            bg=self.colors["bg"],
            fg=self.colors["text_primary"]
        ).pack(anchor="w")

        tk.Label(
            header_frame,
            text="Organize your files automatically",
            font=self.font_normal,
            bg=self.colors["bg"],
            fg=self.colors["text_secondary"]
        ).pack(anchor="w", pady=(2, 0))

        # Status card
        status_card = tk.Frame(
            main_frame,
            bg=self.colors["card_bg"],
            highlightbackground=self.colors["border"],
            highlightthickness=1
        )
        status_card.pack(fill="x", pady=10)

        self.status_label = tk.Label(
            status_card,
            text="Status: Stopped",
            font=self.font_heading,
            bg=self.colors["card_bg"],
            fg=self.colors["danger"]
        )
        self.status_label.pack(pady=20)

        # Separator line
        tk.Frame(
            status_card,
            height=1,
            bg=self.colors["border"]
        ).pack(fill="x")

        # Button area
        btn_frame = tk.Frame(main_frame, bg=self.colors["bg"])
        btn_frame.pack(fill="x", pady=15)

        # Start/Stop button
        self.start_btn = tk.Button(
            btn_frame,
            text="Start Sorter",
            width=25,
            bg=self.colors["success"],
            fg="white",
            font=self.font_button,
            relief="flat",
            cursor="hand2",
            command=self.toggle_sorter,
            activebackground=self.colors["success_hover"],
            activeforeground="white"
        )
        self.start_btn.pack(fill="x", pady=5)

        # Settings button
        settings_btn = tk.Button(
            btn_frame,
            text="Settings",
            width=25,
            bg=self.colors["card_bg"],
            fg=self.colors["text_primary"],
            font=self.font_button,
            relief="flat",
            cursor="hand2",
            command=self.open_settings,
            activebackground="#e3f2fd",
            activeforeground=self.colors["primary"]
        )
        settings_btn.pack(fill="x", pady=5)

        # Exit button
        exit_btn = tk.Button(
            btn_frame,
            text="Exit",
            width=25,
            bg=self.colors["card_bg"],
            fg=self.colors["text_secondary"],
            font=self.font_button,
            relief="flat",
            cursor="hand2",
            command=root.quit,
            activebackground="#ffebee",
            activeforeground=self.colors["danger"]
        )
        exit_btn.pack(fill="x", pady=5)

        # Footer
        footer = tk.Frame(main_frame, bg=self.colors["bg"])
        footer.pack(fill="x", side="bottom")

        tk.Label(
            footer,
            text="v1.0",
            font=self.font_normal,
            bg=self.colors["bg"],
            fg=self.colors["text_secondary"]
        ).pack(side="right")

    def toggle_sorter(self):
        if not self.sorter.running:
            try:
                # Sort existing files first
                with open("config.json", "r", encoding="utf-8") as f:
                    config = json.load(f)
                folder_path = config["track_path"]
                folder_mapping = config["mappings"]
                self.sorter.sort_existing_files(folder_path, folder_mapping)

                # Then start watching for new files
                self.sorter.start()
                self.status_label.config(text="Status: Running", fg=self.colors["success"])
                self.start_btn.config(text="Stop Sorter", bg=self.colors["danger"])
            except Exception as e:
                messagebox.showerror("Error", f"Could not start: {e}")
        else:
            self.sorter.stop()
            self.status_label.config(text="Status: Stopped", fg=self.colors["danger"])
            self.start_btn.config(text="Start Sorter", bg=self.colors["success"])

    def open_settings(self):
        settings_window = tk.Toplevel(self.root)
        settings_window.attributes("-topmost", True)
        SettingsApp(settings_window)


if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
