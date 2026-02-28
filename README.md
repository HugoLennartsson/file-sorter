# file-sorter

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🚀 Features

* **Automated Monitoring:** Uses the `watchdog` library to detect new files instantly.
* **Customizable Rules:** Define destination folders for different file extensions in a simple `config.json` file.
* **Error Handling:** Prevents crashes if a file is already in use or a naming conflict occurs.
* **Detailed Logging:** Maintains a log of all moved files for auditing.

## 🛠️ Tech Stack

* **Language:** Python 3
* **Libraries:** `os`, `shutil`, `watchdog`, `json`

## 📦 Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/HugoLennartsson/file-sorter.git
    cd file-sorter
    ```

2.  **Install dependencies:**
    ```bash
    pip install watchdog
    ```
## 💻 Usage

To start the automated sorting, run the following command in your terminal:

```bash
python main.py