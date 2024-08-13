import json
import os
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, request, render_template, redirect, url_for
from task_model import Task, save_task_to_json
from scheduler import schedule_check
app = Flask(__name__)

tasks_file_name = 'tasks/tasks.json'


@app.route('/')
def index():
    return render_template('create_task.html')


@app.route('/add_task', methods=['POST'])
def add_task():
    task = Task(
        task_id=request.form['task_id'],
        schedule=request.form['schedule'],
        filename=request.form['filename'],
        filepath=request.form['filepath'],
        server_key=request.form['server_key'],
        retries=int(request.form.get('retries', 3)),
        retry_delay=int(request.form.get('retry_delay', 60)),
        timeout=request.form.get('timeout', None),
        dependency_server_key=request.form.get('dependency_server_key', None),
        command=request.form.get('command', None)
    )

    if task.timeout:
        task.timeout = int(task.timeout)

    save_task_to_json(task, tasks_file_name)

    return redirect(url_for('index'))


@app.route('/tasks')
def view_tasks():
    # Load tasks from the JSON file
    if os.path.exists(tasks_file_name):
        with open(tasks_file_name, 'r') as file:
            try:
                tasks = json.load(file)
            except json.JSONDecodeError:
                tasks = []
    else:
        tasks = []

    return render_template('view_tasks.html', tasks=tasks)


if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.add_job(schedule_check, 'interval', minutes=1)
    scheduler.start()
    try:
        app.run(debug=True, use_reloader=False)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
