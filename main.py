# Python Backend Module
# Used to connect with the mySQL database and handle web endpoint calls

from flask import Flask, render_template, request, redirect
from mysql.connector import connect, Error
import logging

# Create a logger instance
logger = logging.getLogger(__name__)

# Set logging level to ERROR
logger.setLevel(logging.ERROR)

# Create a file handler to log errors to a file
file_handler = logging.FileHandler('errors.log')
file_handler.setLevel(logging.ERROR)

# Create a formatter for log messages
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Add the file handler to the logger
logger.addHandler(file_handler)

app = Flask(__name__)

def getLastRow():
    # Try to get last row from tasks, if unsuccessful log the error
    try:
        cursor = db.cursor()
        # SQL query to get last inserted id
        cursor.execute("SELECT id FROM tasks WHERE date = (SELECT MAX(date) FROM tasks);")
        return cursor.fetchone()[0]
    except Error as e:
        logger.error(f'Error getting last row from database: {e}')
        return 'An error occurred while retrieving last row'

# Primary Author: Peyton Smith
# Current Semester: Spring 2023
# Connects to the mySQL server running 
# on Peyton's computer with the following credentials

# Try to connect to database, if unsuccessful log the error
try:
    db = connect(
    host="26.209.55.71",
    user="remote_user",
    password="remote_user",
    database="testdb"
    )
    print("Database connected!")
except Error as e:
    print(e)

# Primary Author: Peyton Smith
# Current Semester: Spring 2023
# Web endpoint handler, used to display all the tasks
@app.route("/")
def tasks():
    # Try to retrieve tasks, if unsuccessful log the error
    try:
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
    except Error as e:
        logger.error(f'Error retrieving tasks from database: {e}')
        return 'Error occurred retrieving tasks'

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
    # Try to submit task, if unsuccessful log the error
    try:
        cursor = db.cursor()
        # Get the following parameters from the front-end form
        title = request.form["title"]
        description = request.form["description"]
        # Insert task into database
        cursor.execute("INSERT INTO tasks (title, description) VALUES (%s, %s)", (title, description))
        db.commit()
        # Redirects automatically to the start
        return redirect("/")
    except Error as e:
        logger.error(f'Error adding task to database: {e}')
        return 'An error occurred adding task'

# Primary Author: Peyton Smith
# Current Semester: Spring 2023
# Web endpoint handler used when a user checks off a task as completed
@app.route("/complete_task/<int:id>", methods=["POST"])
def complete_task(id):
    # Try to complete task, if unsuccessful log the error
    try:
        cursor = db.cursor()
        # Change is_completed parameter to 1 for that task
        cursor.execute("UPDATE tasks SET is_completed=1 WHERE id=%s", (id,))
        # Set the date_completed parameter to the current date/time
        cursor.execute("UPDATE tasks SET date_completed=NOW() WHERE id=%s", (id,))
        db.commit()
        # Redirects automatically to the start
        return redirect("/")
    except Error as e:
        logger.error(f'Error completing task in database: {e}')
        return 'An error occurred while completing task'

# Primary Author: Peyton Smith
# Current Semester: Spring 2023
# Web endpoint handler used to delete a specific task 
@app.route('/delete_task/<int:id>', methods=['POST'])
def delete_task(id):
    # Try to delete task, if unsuccessful log the error
    try:
        cursor = db.cursor()
        # Delete the task from the tasks table given the id
        cursor.execute("DELETE FROM tasks WHERE id = %s;", (id,))
        db.commit()
        # Redirects automatically to the start
        return redirect("/")
    except Error as e:
        logger.error(f'Error deleting task from database: {e}')
        return 'An error occurred while deleting task'

if __name__ == '__main__':
    app.run(debug=True)
