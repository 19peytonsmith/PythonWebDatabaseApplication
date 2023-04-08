from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)
db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root",
  database="testdb"
)

@app.route("/")
def tasks():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    non_completed = []
    completed = []
    empty_non_completed = True
    empty_completed = True
    for task in tasks:
        if task[4]:
            completed.append(task)
            empty_completed = False
        else:
            non_completed.append(task)
            empty_non_completed = False
    return render_template("tasks.html", non_completed=non_completed, completed=completed, empty_non_completed=empty_non_completed, empty_completed=empty_completed)

@app.route("/add_task")
def add_task():
    return render_template("add_task.html")

@app.route("/submit_task", methods=["POST"])
def submit_task():
    cursor = db.cursor()
    title = request.form["title"]
    description = request.form["description"]
    cursor.execute("INSERT INTO tasks (title, description) VALUES (%s, %s)", (title, description))
    db.commit()
    return redirect("/")

@app.route("/complete_task/<int:id>", methods=["POST"])
def complete_task(id):
    cursor = db.cursor()
    cursor.execute("UPDATE tasks SET is_completed=1 WHERE id=%s", (id,))
    cursor.execute("UPDATE tasks SET date_completed=NOW() WHERE id=%s", (id,))
    db.commit()
    return redirect("/")

@app.route('/delete_task/<int:id>', methods=['POST'])
def delete_task(id):
    cursor = db.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = %s;", (id,))
    db.commit()
    return redirect("/")


if __name__ == '__main__':
    app.run(debug=True)
