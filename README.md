# file-sorter

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🚀 Features

* **Real-time Monitoring:** Instantly detects new files using the `watchdog` library.
* **Graphical User Interface (GUI):** Easy-to-use desktop app to start/stop the sorter and manage settings.
* **Customizable Mapping:** Define destination subfolders for specific file extensions via a visual interface.
* **Error Handling:** Safe file movement prevents data loss or crashes during naming conflicts.



## 🛠️ Tech Stack

* **Language:** Python 3
* **GUI Framework:** Tkinter (Built-in)
* **Libraries:** `watchdog`, `json`, `shutil`

## 📦 Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/HugoLennartsson/file-sorter.git](https://github.com/HugoLennartsson/file-sorter.git)
    cd file-sorter
    ```

2.  **Install dependencies:**
    ```bash
    pip install watchdog
    ```

## 💻 Usage

Run the main application file to launch the control panel:

```bash
python main.py