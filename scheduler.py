import json
import os
from datetime import datetime, timedelta
import pytz
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor
from croniter import croniter
from file_watch import check_file

# Initialize the scheduler with a ThreadPoolExecutor to handle multiple jobs
scheduler = BackgroundScheduler(
    jobstores={'default': MemoryJobStore()},
    executors={'default': ThreadPoolExecutor(10)},
    job_defaults={'coalesce': False, 'max_instances': 1},
    timezone=pytz.utc
)


def read_tasks_from_json():
    if os.path.exists('tasks.json'):
        with open('tasks.json', 'r') as file:
            try:
                tasks = json.load(file)
            except json.JSONDecodeError:
                tasks = []
    else:
        tasks = []
    return tasks


def execute_task(task, retries=0):
    print(f"Executing task {task['task_id']}, attempt {retries + 1}")

    # Calculate the start time to check for timeout
    start_time = datetime.now(pytz.utc)

    # Check if the task has a timeout and if it has been exceeded
    if task.get('timeout'):
        timeout = int(task['timeout'])
        elapsed_time = (start_time - task.get('start_time', start_time)).total_seconds()
        if elapsed_time >= timeout:
            print(f"Task {task['task_id']} timed out after {elapsed_time} seconds.")
            return

    # Execute the check_file function
    success = check_file(task)

    # If check_file is successful, return and don't reschedule
    if success:
        print(f"Task {task['task_id']} completed successfully.")
        return

    # If check_file fails and there are retries left
    if retries < task['retries']:
        retries += 1
        print(f"Task {task['task_id']} failed, will retry in {task['retry_delay']} seconds.")
        task['start_time'] = task.get('start_time', start_time)  # Track the start time

        # Reschedule the task after the retry delay
        scheduler.add_job(
            execute_task,
            'date',
            run_date=start_time + timedelta(seconds=task['retry_delay']),
            args=[task, retries]
        )
    else:
        print(f"Task {task['task_id']} failed after {retries} retries.")


def schedule_check():
    print("Scheduler running...")
    tasks = read_tasks_from_json()

    # Get current time and time 1 minute later
    current_time = datetime.now(pytz.utc)
    next_minute_time = current_time + timedelta(minutes=1)

    for task in tasks:
        cron = croniter(task['schedule'], current_time)
        next_run_time = cron.get_next(datetime)

        # If the cron job is due to run within the next minute
        if current_time <= next_run_time < next_minute_time:
            execute_task(task)
