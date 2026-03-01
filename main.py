import tkinter as tk
from tkinter import messagebox
from settings_gui import SettingsApp # Import your existing GUI class
from sorter_engine import SorterInstance
import threading

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Auto File Sorter Pro")
        self.root.geometry("400x300")
        self.sorter = SorterInstance()
        
        # UI Elements
        tk.Label(root, text="File Sorter Control Panel", font=("Arial", 16, "bold")).pack(pady=20)
        
        self.status_label = tk.Label(root, text="Status: Stopped", fg="red", font=("Arial", 12))
        self.status_label.pack(pady=10)

        self.start_btn = tk.Button(root, text="Start Sorter", width=20, bg="#4CAF50", fg="white", command=self.toggle_sorter)
        self.start_btn.pack(pady=5)

        tk.Button(root, text="Settings", width=20, command=self.open_settings).pack(pady=5)
        tk.Button(root, text="Exit", width=20, command=root.quit).pack(pady=5)
    
    def toggle_sorter(self):
        if not self.sorter.running:
            try:
                self.sorter.start()
                self.status_label.config(text="Status: Running...", fg="green")
                self.start_btn.config(text="Stop Sorter", bg="#f44336")
            except Exception as e:
                messagebox.showerror("Error", f"Could not start: {e}")
        else:
            self.sorter.stop()
            self.status_label.config(text="Status: Stopped", fg="red")
            self.start_btn.config(text="Start Sorter", bg="#4CAF50")

    def open_settings(self):
        # Open the settings window as a popup
        settings_window = tk.Toplevel(self.root)
        SettingsApp(settings_window)

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()