# Task Scheduler with SFTP File Checker

This project is a Python-based Flask application designed to run scheduled tasks using cron-like syntax. The application reads a list of tasks from a JSON file, checks if any tasks are due to run, and if so, performs an SFTP file check on a remote server. The project also includes retry logic and timeout handling for each task.

## Features

- **Task Scheduling**: Schedules tasks based on cron-like syntax and executes them at the correct time.
- **SFTP File Checking**: Connects to remote servers via SFTP and checks for the presence of files, with support for regex patterns.
- **Retry and Timeout Logic**: Retries failed tasks based on configurable delay and retry limits, with support for timeout.
- **Web Interface**: A basic Flask web UI to add tasks and display them in a tabular format.

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/starinfinity/FWOS2.git
   cd FWOS2
   ```
2. **Install the required Python packages**:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the Flask application:
   ```bash
   python app.py
   ```
