# task_model.py
from dataclasses import dataclass, asdict
from typing import Optional
import json
import os


@dataclass
class Task:
    task_id: str
    schedule: str
    filename: str
    filepath: str
    server_key: str
    retries: int = 3
    retry_delay: int = 60
    timeout: Optional[int] = None
    dependency_server_key: Optional[str] = None
    command: Optional[str] = None


def save_task_to_json(task: Task, json_file: str):
    if os.path.exists(json_file):
        with open(json_file, 'r') as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = []  # Initialize as empty list if file is empty or corrupted
    else:
        data = []

    # Convert the Task dataclass instance to a dictionary
    task_dict = asdict(task)

    # Append the new task to the existing data
    data.append(task_dict)

    # Write the updated data back to the file
    with open(json_file, 'w') as file:
        json.dump(data, file, indent=4)
