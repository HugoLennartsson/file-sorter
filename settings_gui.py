import tkinter as tk
from tkinter import filedialog, messagebox
import json
import os

class SettingsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Sorter Settings")
        self.root.geometry("500x400")

        self.config_path = "config.json"
        self.load_settings()


        tk.Label(root, text="Folder to Monitor:", font=('Arial', 10, 'bold')).pack(pady=5)
        self.path_var = tk.StringVar(value=self.config.get("track_path", ""))
        
        path_frame = tk.Frame(root)
        path_frame.pack(pady=5, fill='x', padx=20)
        
        tk.Entry(path_frame, textvariable=self.path_var).pack(side='left', expand=True, fill='x')
        tk.Button(path_frame, text="Browse", command=self.browse_folder).pack(side='right', padx=5)

        # Mappings Section
        tk.Label(root, text="File Mappings (Extension: Folder Name):", font=('Arial', 10, 'bold')).pack(pady=10)
        
        self.text_area = tk.Text(root, height=10, width=50)
        self.text_area.pack(padx=20, pady=5)
        
        # Format mapping dict into the text area
        mappings_str = json.dumps(self.config.get("mappings", {}), indent=4)
        self.text_area.insert("1.0", mappings_str)

        # Save Button
        tk.Button(root, text="Save Settings", bg="#4CAF50", fg="white", 
                  command=self.save_settings, height=2, width=20).pack(pady=20)
        
    def load_settings(self):
        try:
            with open(self.config_path, "r") as f:
                self.config = json.load(f)
        except FileNotFoundError:
            self.config = {"track_path": "", "mappings": {}}
    
    def browse_folder(self):
        selected_path = filedialog.askdirectory()
        if selected_path:
            self.path_var.set(selected_path)
    
    def save_settings(self):
        try:
            new_path = self.path_var.get()
            new_mappings = json.loads(self.text_area.get("1.0", "end-1c"))
            
            self.config["track_path"] = new_path
            self.config["mappings"] = new_mappings

            with open(self.config_path, "w") as f:
                json.dump(self.config, f, indent=4)
            
            messagebox.showinfo("Success", "Settings saved successfully!")
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Invalid JSON format in mappings.")
    

if __name__ == "__main__":
    root = tk.Tk()
    app = SettingsApp(root)
    root.mainloop()