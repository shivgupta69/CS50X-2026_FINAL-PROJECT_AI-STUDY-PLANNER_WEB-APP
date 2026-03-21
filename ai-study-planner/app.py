from flask import Flask, render_template, request, redirect, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
app.secret_key = "secretkey"


def get_db():
    return sqlite3.connect("study.db")


def generate_schedule(tasks):
    schedule = []
    current_time = 9

    tasks = sorted(tasks, key=lambda x: x[4], reverse=True)

    for task in tasks:
        schedule.append({
            "task": task[2],
            "start": current_time,
            "end": current_time + task[4]
        })
        current_time += task[4]

    return schedule


@app.route("/")
def index():
    if "user_id" not in session:
        return redirect("/login")

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM tasks WHERE user_id=?",
        (session["user_id"],)
    )
    tasks = cursor.fetchall()

    cursor.execute(
        "SELECT category, SUM(duration) FROM tasks WHERE user_id=? GROUP BY category",
        (session["user_id"],)
    )
    stats = cursor.fetchall()
    conn.close()

    labels = [row[0] for row in stats]
    data = [row[1] for row in stats]

    return render_template(
        "dashboard.html",
        tasks=tasks,
        labels=labels,
        data=data
    )


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if not username or not password:
            flash("Username and password cannot be empty.", "error")
            return redirect("/register")

        hashed_password = generate_password_hash(password)

        conn = get_db()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, hashed_password)
            )
            conn.commit()

        except sqlite3.IntegrityError:
            conn.close()
            flash("Username already exists. Please choose another.", "error")
            return redirect("/register")

        conn.close()
        flash("Registration successful! Please login.")
        return redirect("/login")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if not username or not password:
            flash("Username and password cannot be empty.", "error")
            return render_template("login.html")

        conn = get_db()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE username=?",
            (username,)
        )
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user[2], password):
            session["user_id"] = user[0]
            return redirect("/")

        flash("Invalid username or password.", "error")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


@app.route("/add", methods=["POST"])
def add_task():
    if "user_id" not in session:
        return redirect("/login")

    task = request.form.get("task", "").strip()
    category = request.form.get("category", "").strip()

    if not task or not category:
        flash("Task name and category cannot be empty.", "error")
        return redirect("/")

    try:
        duration = int(request.form.get("duration"))
        if duration < 1:
            raise ValueError
    except (ValueError, TypeError):
        flash("Duration must be a whole number of at least 1.", "error")
        return redirect("/")

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO tasks (user_id, task_name, category, duration) VALUES (?, ?, ?, ?)",
        (session["user_id"], task, category, duration)
    )

    conn.commit()
    conn.close()

    flash("Task added successfully!")
    return redirect("/")


@app.route("/delete/<int:id>")
def delete_task(id):
    if "user_id" not in session:
        return redirect("/login")

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM tasks WHERE id=? AND user_id=?",
        (id, session["user_id"])
    )

    conn.commit()
    conn.close()

    return redirect("/")


@app.route("/schedule")
def schedule():
    if "user_id" not in session:
        return redirect("/login")

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM tasks WHERE user_id=?",
        (session["user_id"],)
    )
    tasks = cursor.fetchall()
    conn.close()

    schedule = generate_schedule(tasks)

    return render_template("schedule.html", schedule=schedule)


if __name__ == "__main__":
    app.run(debug=True)
