# file-sorter

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A desktop application that automatically organizes files into subfolders based on file extension. Features both real-time monitoring and bulk sorting of existing files.

## 🚀 Features

* **Real-time Monitoring:** Instantly detects and sorts new files using the `watchdog` library.
* **Existing File Sorting:** Automatically sorts all existing files when starting the sorter.
* **Modern Graphical User Interface:** Clean, intuitive desktop app with visual controls and status indicators.
* **Visual Settings Manager:** Easy-to-use form-based configuration - no JSON editing required.
* **Customizable Mapping:** Define destination subfolders for specific file extensions through a simple interface.
* **Auto-save Settings:** Changes are saved automatically when closing the settings window.
* **Safe File Movement:** Prevents overwriting existing files and handles naming conflicts gracefully.

## 🛠️ Tech Stack

* **Language:** Python 3
* **GUI Framework:** Tkinter (built-in)
* **Libraries:** `watchdog`, `json`, `shutil`

## 📦 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/HugoLennartsson/file-sorter.git
   cd file-sorter
   ```

2. **Install dependencies:**
   ```bash
   pip install watchdog
   ```

## 💻 Usage

Run the main application file to launch the control panel:

```bash
python main.py
```

### Configuration

1. Click **Settings** to open the configuration panel
2. **Folder to Monitor:** Browse and select the folder you want to organize
3. **File Mappings:** Add extension-to-folder mappings:
   - Click **+ Add Extension**
   - Enter the file extension (e.g., `.jpg`, `.pdf`, `.exe`)
   - Enter the destination subfolder name (e.g., `Images`, `Documents`, `Installers`)
4. Settings auto-save when you close the window

### Default Mappings

| Extension | Folder |
|-----------|--------|
| `.pdf`, `.docx`, `.txt` | Documents |
| `.jpg`, `.png` | Images |
| `.mp4` | Videos |
| `.zip` | Archives |
| `.exe` | Installers |

### Sorting Files

- Click **Start Sorter** to:
  1. Sort all existing files in the monitored folder
  2. Begin watching for new files (auto-sorts as they appear)
- Click **Stop Sorter** to pause monitoring

## 📁 Config File

Settings are stored in `config.json` in the application directory:

```json
{
    "track_path": "C:/Users/YourName/Downloads",
    "mappings": {
        ".pdf": "Documents",
        ".jpg": "Images",
        ".exe": "Installers"
    }
}
```
