import tkinter as tk
from tkinter import filedialog, messagebox, font
import json
import os


class SettingsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Settings")
        self.root.geometry("600x600")
        self.root.resizable(False, False)

        # Modern color scheme
        self.colors = {
            "bg": "#f5f5f5",
            "card_bg": "#ffffff",
            "primary": "#2196F3",
            "primary_hover": "#1976D2",
            "success": "#4CAF50",
            "text_primary": "#333333",
            "text_secondary": "#666666",
            "border": "#e0e0e0",
            "error": "#f44336",
            "row_bg": "#fafafa",
        }

        self.root.configure(bg=self.colors["bg"])

        # Fonts
        self.font_title = font.Font(family="Segoe UI", size=16, weight="bold")
        self.font_heading = font.Font(family="Segoe UI", size=11, weight="bold")
        self.font_normal = font.Font(family="Segoe UI", size=10)
        self.font_small = font.Font(family="Segoe UI", size=9)
        self.font_button = font.Font(family="Segoe UI", size=9, weight="bold")

        self.config_path = "config.json"
        self.load_settings()

        # Main container
        main_frame = tk.Frame(root, bg=self.colors["bg"])
        main_frame.pack(fill="both", expand=True, padx=25, pady=20)

        # Header
        tk.Label(
            main_frame,
            text="Settings",
            font=self.font_title,
            bg=self.colors["bg"],
            fg=self.colors["text_primary"]
        ).pack(anchor="w", pady=(0, 5))

        tk.Label(
            main_frame,
            text="Configure folder monitoring and file mappings",
            font=self.font_normal,
            bg=self.colors["bg"],
            fg=self.colors["text_secondary"]
        ).pack(anchor="w", pady=(0, 20))

        # Folder to Monitor section
        section_card = tk.Frame(
            main_frame,
            bg=self.colors["card_bg"],
            highlightbackground=self.colors["border"],
            highlightthickness=1
        )
        section_card.pack(fill="x", pady=10)

        inner_frame = tk.Frame(section_card, bg=self.colors["card_bg"])
        inner_frame.pack(fill="both", padx=20, pady=20)

        tk.Label(
            inner_frame,
            text="Folder to Monitor",
            font=self.font_heading,
            bg=self.colors["card_bg"],
            fg=self.colors["text_primary"]
        ).pack(anchor="w", pady=(0, 8))

        tk.Label(
            inner_frame,
            text="Select the folder where files will be monitored and sorted.",
            font=self.font_normal,
            bg=self.colors["card_bg"],
            fg=self.colors["text_secondary"],
            wraplength=500
        ).pack(anchor="w", pady=(0, 15))

        # Path entry with browse button
        path_frame = tk.Frame(inner_frame, bg=self.colors["card_bg"])
        path_frame.pack(fill="x")

        self.path_var = tk.StringVar(value=self.config.get("track_path", ""))
        self.path_entry = tk.Entry(
            path_frame,
            textvariable=self.path_var,
            font=self.font_normal,
            bg=self.colors["bg"],
            fg=self.colors["text_primary"],
            relief="flat",
            highlightbackground=self.colors["border"],
            highlightthickness=1
        )
        self.path_entry.pack(side="left", expand=True, fill="x", ipady=8)

        self.browse_btn = tk.Button(
            path_frame,
            text="Browse",
            font=self.font_button,
            bg=self.colors["primary"],
            fg="white",
            relief="flat",
            cursor="hand2",
            command=self.browse_folder,
            activebackground=self.colors["primary_hover"],
            activeforeground="white",
            padx=20,
            pady=5
        )
        self.browse_btn.pack(side="right", padx=(10, 0))

        # File Mappings section
        mapping_card = tk.Frame(
            main_frame,
            bg=self.colors["card_bg"],
            highlightbackground=self.colors["border"],
            highlightthickness=1
        )
        mapping_card.pack(fill="both", expand=True, pady=10)

        mapping_inner = tk.Frame(mapping_card, bg=self.colors["card_bg"])
        mapping_inner.pack(fill="both", padx=20, pady=20)

        # Header row
        header_frame = tk.Frame(mapping_inner, bg=self.colors["card_bg"])
        header_frame.pack(fill="x", pady=(0, 10))

        tk.Label(
            header_frame,
            text="File Mappings",
            font=self.font_heading,
            bg=self.colors["card_bg"],
            fg=self.colors["text_primary"]
        ).pack(side="left")

        tk.Button(
            header_frame,
            text="+ Add Extension",
            font=self.font_button,
            bg=self.colors["primary"],
            fg="white",
            relief="flat",
            cursor="hand2",
            command=self.add_mapping_row,
            activebackground=self.colors["primary_hover"],
            activeforeground="white",
            padx=15,
            pady=4
        ).pack(side="right")

        tk.Label(
            mapping_inner,
            text="Specify which folder each file type should be moved to.",
            font=self.font_normal,
            bg=self.colors["card_bg"],
            fg=self.colors["text_secondary"]
        ).pack(anchor="w", pady=(0, 15))

        # Scrollable frame for mappings
        self.mappings_frame = tk.Frame(mapping_inner, bg=self.colors["bg"])
        self.mappings_frame.pack(fill="both", expand=True)

        # Canvas for scrolling
        self.canvas = tk.Canvas(
            self.mappings_frame,
            bg=self.colors["card_bg"],
            highlightthickness=0,
            highlightbackground=self.colors["border"]
        )
        self.scrollbar = tk.Scrollbar(
            self.mappings_frame,
            orient="vertical",
            command=self.canvas.yview
        )
        self.scrollable_frame = tk.Frame(self.canvas, bg=self.colors["card_bg"])

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True, padx=(0, 5))
        self.scrollbar.pack(side="right", fill="y")

        # Bind mouse wheel for scrolling
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        # Store mapping rows
        self.mapping_rows = []
        self.load_mappings()

        # Button area
        btn_frame = tk.Frame(main_frame, bg=self.colors["bg"])
        btn_frame.pack(fill="x", pady=20)

        self.save_btn = tk.Button(
            btn_frame,
            text="Save Settings",
            font=self.font_button,
            bg=self.colors["success"],
            fg="white",
            relief="flat",
            cursor="hand2",
            command=self.save_settings,
            activebackground="#388E3C",
            activeforeground="white",
            padx=30,
            pady=8
        )
        self.save_btn.pack(side="right")

        self.cancel_btn = tk.Button(
            btn_frame,
            text="Cancel",
            font=self.font_button,
            bg=self.colors["card_bg"],
            fg=self.colors["text_secondary"],
            relief="flat",
            cursor="hand2",
            command=root.destroy,
            activebackground="#ffebee",
            activeforeground=self.colors["error"],
            padx=20,
            pady=8
        )
        self.cancel_btn.pack(side="right", padx=(0, 10))

        # Handle window close button
        root.protocol("WM_DELETE_WINDOW", self.on_close)

    def load_settings(self):
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                self.config = json.load(f)
        except FileNotFoundError:
            self.config = {"track_path": "", "mappings": {}}

    def browse_folder(self):
        selected_path = filedialog.askdirectory()
        if selected_path:
            self.path_var.set(selected_path)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def add_mapping_row(self, extension="", folder=""):
        """Add a new extension-to-folder mapping row."""
        row_frame = tk.Frame(self.scrollable_frame, bg=self.colors["row_bg"])
        row_frame.pack(fill="x", padx=5, pady=3)

        # Extension field
        ext_frame = tk.Frame(row_frame, bg=self.colors["row_bg"])
        ext_frame.pack(side="left", padx=(5, 10))

        tk.Label(
            ext_frame,
            text="Extension:",
            font=self.font_normal,
            bg=self.colors["row_bg"],
            fg=self.colors["text_primary"]
        ).pack(side="left", padx=(0, 5))

        ext_var = tk.StringVar()
        ext_var.set(extension)
        ext_entry = tk.Entry(
            ext_frame,
            textvariable=ext_var,
            font=self.font_normal,
            width=12,
            bg=self.colors["card_bg"],
            relief="flat",
            highlightbackground=self.colors["border"],
            highlightthickness=1
        )
        ext_entry.pack(side="left", ipady=4)

        # Folder field
        folder_frame = tk.Frame(row_frame, bg=self.colors["row_bg"])
        folder_frame.pack(side="left", padx=10)

        tk.Label(
            folder_frame,
            text="Folder:",
            font=self.font_normal,
            bg=self.colors["row_bg"],
            fg=self.colors["text_primary"]
        ).pack(side="left", padx=(0, 5))

        folder_var = tk.StringVar()
        folder_var.set(folder)
        folder_entry = tk.Entry(
            folder_frame,
            textvariable=folder_var,
            font=self.font_normal,
            width=20,
            bg=self.colors["card_bg"],
            relief="flat",
            highlightbackground=self.colors["border"],
            highlightthickness=1
        )
        folder_entry.pack(side="left", ipady=4)

        # Remove button
        remove_btn = tk.Button(
            row_frame,
            text="X",
            font=self.font_button,
            bg=self.colors["error"],
            fg="white",
            relief="flat",
            cursor="hand2",
            command=lambda: self.remove_mapping_row(row_frame, ext_var, folder_var),
            activebackground="#d32f2f",
            activeforeground="white",
            padx=12,
            pady=2
        )
        remove_btn.pack(side="right", padx=5)

        self.mapping_rows.append({
            "frame": row_frame,
            "ext_var": ext_var,
            "folder_var": folder_var
        })

    def remove_mapping_row(self, row_frame, ext_var, folder_var):
        """Remove a mapping row."""
        for i, row in enumerate(self.mapping_rows):
            if row["ext_var"] is ext_var:
                row["frame"].destroy()
                self.mapping_rows.pop(i)
                break

    def load_mappings(self):
        """Load existing mappings from config."""
        mappings = self.config.get("mappings", {})
        for ext, folder in mappings.items():
            self.add_mapping_row(ext, folder)

    def save_settings(self, show_message=True):
        """Collect all mappings and save."""
        try:
            new_path = self.path_var.get()

            # Collect mappings from rows
            new_mappings = {}
            for row in self.mapping_rows:
                ext = row["ext_var"].get().strip().lower()
                folder = row["folder_var"].get().strip()

                if ext and folder:
                    # Ensure extension starts with dot
                    if not ext.startswith("."):
                        ext = "." + ext
                    new_mappings[ext] = folder

            self.config["track_path"] = new_path
            self.config["mappings"] = new_mappings

            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=4)

            if show_message:
                messagebox.showinfo("Success", "Settings saved successfully!")
            self.root.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Could not save settings: {e}")

    def on_close(self):
        """Auto-save on window close."""
        self.save_settings(show_message=False)


if __name__ == "__main__":
    root = tk.Tk()
    app = SettingsApp(root)
    root.mainloop()
