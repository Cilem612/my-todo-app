from flask import Flask, render_template, request, redirect
import json
import os

app = Flask(__name__)
TASKS_FILE = 'tasks.json'

def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, 'r') as file:
        return json.load(file)

def save_tasks(tasks):
    with open(TASKS_FILE, 'w') as file:
        json.dump(tasks, file)

@app.route("/", methods=["GET", "POST"])
def index():
    tasks = load_tasks()
    if request.method == "POST":
        task_name = request.form.get("task")
        if task_name:
            tasks.append({"name": task_name, "done": False})
            save_tasks(tasks)
        return redirect("/")
    return render_template("index.html", tasks=tasks)

@app.route("/toggle", methods=["POST"])
def toggle_task():
    task_name = request.form.get("task")
    tasks = load_tasks()
    for task in tasks:
        if task["name"] == task_name:
            task["done"] = not task["done"]
            break
    save_tasks(tasks)
    return redirect("/")

@app.route("/delete", methods=["POST"])
def delete_task():
    task_name = request.form.get("task")
    tasks = load_tasks()
    tasks = [task for task in tasks if task["name"] != task_name]
    save_tasks(tasks)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)