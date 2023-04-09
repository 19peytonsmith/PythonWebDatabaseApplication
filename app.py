# Python Backend Module
# Used to connect with the mySQL database and handle web endpoint calls

from flask import Flask, render_template, request, redirect
import mysql.connector

# Primary Author: Peyton Smith
# Current Semester: Spring 2023
# Connects to the mySQL server running 
# on Peyton's computer with the following credentials
app = Flask(__name__)
db = mysql.connector.connect(
  host="26.209.55.71",
  user="remote_user",
  password="remote_user",
  database="testdb"
)

# Primary Author: Peyton Smith
# Current Semester: Spring 2023
# Web endpoint handler, used to display all the tasks
@app.route("/")
def tasks():
    cursor = db.cursor()
    # Fetch all rows form the tasks table
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    non_completed = []
    completed = []
    empty_non_completed = True
    empty_completed = True
    # Iterate through the tasks
    for task in tasks:
        # If is_completed is true append to completed array
        if task[4]:
            completed.append(task)
            empty_completed = False
        # If is_completed is false append to non_completed array
        else:
            non_completed.append(task)
            empty_non_completed = False
    # Render out the tasks.html and send over the following parameters
    return render_template("tasks.html", non_completed=non_completed, completed=completed, empty_non_completed=empty_non_completed, empty_completed=empty_completed)

# Primary Author: Peyton Smith
# Current Semester: Spring 2023
# Web endpoint handler that renders the tasks.html file
@app.route("/add_task")
def add_task():
    return render_template("add_task.html")

# Primary Author: Peyton Smith
# Current Semester: Spring 2023
# Web endpoint handler used when a user adds a new task
@app.route("/submit_task", methods=["POST"])
def submit_task():
    cursor = db.cursor()
    # Get the following parameters from the front-end form
    title = request.form["title"]
    description = request.form["description"]
    # Insert task into database
    cursor.execute("INSERT INTO tasks (title, description) VALUES (%s, %s)", (title, description))
    db.commit()
    # Redirects automatically to the start
    return redirect("/")

# Primary Author: Peyton Smith
# Current Semester: Spring 2023
# Web endpoint handler used when a user checks off a task as completed
@app.route("/complete_task/<int:id>", methods=["POST"])
def complete_task(id):
    cursor = db.cursor()
    # Change is_completed parameter to 1 for that task
    cursor.execute("UPDATE tasks SET is_completed=1 WHERE id=%s", (id,))
    # Set the date_completed parameter to the current date/time
    cursor.execute("UPDATE tasks SET date_completed=NOW() WHERE id=%s", (id,))
    db.commit()
    # Redirects automatically to the start
    return redirect("/")

# Primary Author: Peyton Smith
# Current Semester: Spring 2023
# Web endpoint handler used to delete a specific task 
@app.route('/delete_task/<int:id>', methods=['POST'])
def delete_task(id):
    cursor = db.cursor()
    # Delete the task from the tasks table given the id
    cursor.execute("DELETE FROM tasks WHERE id = %s;", (id,))
    db.commit()
    # Redirects automatically to the start
    return redirect("/")


if __name__ == '__main__':
    app.run(debug=True)
