# 🔐 Password Manager

A simple, secure password manager built with Python that works on Windows, Mac, and Linux.

-----

## 🚀 Quick Setup

### Step 1: Install Python

Ensure you have Python 3 and Pip installed on your system.

  * **Windows**: Download from [python.org](https://www.python.org/downloads/).
  * **Mac**: `brew install python` or download from [python.org](https://www.python.org/downloads/).
  * **Linux (Debian/Ubuntu)**: `sudo apt update && sudo apt install python3 python3-pip python3-venv`

### Step 2: Download the Code

Download the project files and place them in a folder named `Password_Manager`.

### Step 3: Navigate to the Project Folder

Open your terminal or command prompt and navigate into the project directory.

```bash
cd path/to/Password_Manager
```

### Step 4: Create and Activate a Virtual Environment

Creating a virtual environment keeps your project's dependencies separate from your global Python installation.

1.  **Create the environment:**

    ```bash
    python3 -m venv venv
    ```

2.  **Activate the environment:**

      * **Windows (Command Prompt):**
        ```cmd
        .\venv\Scripts\activate
        ```
      * **Windows (PowerShell):**
        ```powershell
        .\venv\Scripts\Activate.ps1
        ```
      * **Mac & Linux:**
        ```bash
        source venv/bin/activate
        ```

    > ✨ **Pro-tip**: You'll know the virtual environment is active when you see `(venv)` at the beginning of your terminal prompt.

### Step 5: Install Dependencies and Run

With your virtual environment active, install the required packages and launch the application.

1.  **Install packages:**

    ```bash
    pip install flask cryptography
    ```

2.  **Set up the database:**

    ```bash
    python setup_database.py
    ```

3.  **Run the application:**

    ```bash
    python run.py
    ```

### Step 6: Open in Your Browser

Once the server is running, open your web browser and go to the following address:

[http://127.0.0.1:5000](https://www.google.com/search?q=http://127.0.0.1:5000)
