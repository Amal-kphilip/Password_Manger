# 🔐 P-Vault: Your Personal Password Manager

Welcome to P-Vault, a simple and secure password manager built with Python. It works seamlessly across **Windows**, **macOS**, and **Linux**, keeping your digital life safe and organized.

-----

## ✨ Features

  * **Cross-Platform:** Works on Windows, macOS, and Linux.
  * **Secure:** Uses strong encryption to protect your passwords.
  * **Local Storage:** Your data stays on your machine, giving you full control.
  * **Web Interface:** Easy-to-use interface accessible from your browser.
  * **Lightweight:** Minimal dependencies and easy setup.

-----

## 🚀 Getting Started

Follow these simple steps to get P-Vault up and running in minutes.

### 1\. Prerequisites

First, make sure you have **Python 3** installed on your system.

  * **Windows:** Download from [python.org](https://www.python.org/downloads/).
  * **macOS:** Install with Homebrew (`brew install python`) or download from [python.org](https://www.python.org/downloads/).
  * **Linux (Ubuntu/Debian):**
    ```bash
    sudo apt update
    sudo apt install python3 python3-pip
    ```

### 2\. Installation

1.  **Download the Code**
    Download the project files and place them in a folder named `P-Vault`.

2.  **Open Your Terminal**

      * **Windows:** Press `Win + R`, type `cmd`, and press Enter.
      * **macOS:** Press `Cmd + Space`, type `Terminal`, and press Enter.
      * **Linux:** Press `Ctrl + Alt + T`.

3.  **Navigate to the Project Folder**
    Replace `path/to/P-Vault` with the actual path to your folder.

    ```bash
    cd path/to/P-Vault
    ```

4.  **Install Dependencies & Setup Database**
    This single command installs the required Python packages and sets up the database for you.

    ```bash
    pip install flask cryptography && python setup_database.py
    ```

### 3\. Usage

1.  **Run the Application**
    Start the local server with this command:

    ```bash
    python run.py
    ```

2.  **Open Your Browser**
    Navigate to the following address to start using your password manager:
    [**http://localhost:5000**](https://www.google.com/search?q=http://localhost:5000)
