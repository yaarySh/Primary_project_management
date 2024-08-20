import sqlite3
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from datetime import datetime, timedelta

app = Flask(__name__, static_folder="static")
CORS(app)  # Enable CORS for all routes


def get_db_connection():
    conn = sqlite3.connect("project_management.db")
    conn.row_factory = sqlite3.Row
    return conn


# Initialize the database and create the necessary tables
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        start_date DATE NOT NULL,
        end_date DATE
    )
    """
    )

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_id INTEGER,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        due_date DATE,
        is_urgent INTEGER NOT NULL,
        team_member_id INTEGER,
        FOREIGN KEY (project_id) REFERENCES projects(id),
        FOREIGN KEY (team_member_id) REFERENCES team_members(id)
    )
    """
    )

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS team_members (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        role TEXT
    )
    """
    )

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS project_team (
        project_id INTEGER,
        team_member_id INTEGER,
        FOREIGN KEY (project_id) REFERENCES projects(id),
        FOREIGN KEY (team_member_id) REFERENCES team_members(id),
        PRIMARY KEY (project_id, team_member_id)
    )
    """
    )

    conn.commit()
    conn.close()


@app.route("/home")
def home():
    return send_from_directory("front", "base.html")


@app.route("/create_project")
def create_project_f():
    return send_from_directory("front", "create_project_form.html")


@app.route("/create_task")
def create_task():
    return send_from_directory("front", "create_task_form.html")


@app.route("/view_projects")
def view_projects():
    return send_from_directory("front", "view_projects.html")


@app.route("/add_team_member")
def add_team_member_form():
    return send_from_directory("front", "add_team_member_form.html")


@app.route("/urgent_tasks_list")
def urgent_tasks_page():
    return send_from_directory("front", "urgent_tasks.html")


@app.route("/projects", methods=["GET"])
def get_projects():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM projects")
    projects = cursor.fetchall()
    conn.close()

    projects_list = []
    for project in projects:
        projects_list.append(
            {
                "id": project["id"],
                "name": project["name"],
                "description": project["description"],
                "start_date": project["start_date"],
                "end_date": project["end_date"],
            }
        )

    return jsonify(projects_list)


@app.route("/projects", methods=["POST"])
def create_project():
    try:
        request_data = request.json
        name = request_data["name"]
        description = request_data["description"]
        start_date = request_data["start_date"]
        end_date = request_data["end_date"]

        if not name or not description or not start_date:
            raise ValueError("Missing required fields")

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
        INSERT INTO projects (name, description, start_date, end_date) VALUES (?, ?, ?, ?)
        """,
            (name, description, start_date, end_date),
        )
        conn.commit()
        conn.close()

        return jsonify(
            {"status": "success", "message": "Project created successfully!"}
        )
    except KeyError as e:
        print(f"error in post project, error is: {str(e)}")
        return jsonify({"status": "error", "message": f"Missing field: {str(e)}"}), 400


@app.route("/tasks", methods=["POST"])
def create_task_endpoint():
    try:
        request_data = request.json
        project_id = request_data["project_id"]
        title = request_data["title"]
        description = request_data["description"]
        due_date = request_data["due_date"]
        team_member_id = request_data["team_member_id"]  # Optional

        # Check if task is urgent (due within 24 hours)
        is_urgent = (
            1
            if datetime.strptime(due_date, "%Y-%m-%d")
            <= datetime.now() + timedelta(days=1)
            else 0
        )

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO tasks (project_id, title, description, due_date, is_urgent, team_member_id) VALUES (?, ?, ?, ?, ?, ?)",
            (project_id, title, description, due_date, is_urgent, team_member_id),
        )
        conn.commit()
        conn.close()

        return jsonify({"message": "Task created successfully!"}), 201

    except KeyError as e:
        return jsonify({"error": f"Missing field: {str(e)}"}), 400


@app.route("/team_members", methods=["POST"])
def add_team_member():
    try:
        request_data = request.json
        name = request_data["name"]
        role = request_data["role"]

        conn = get_db_connection()
        cursor = conn.cursor()

        # Insert team member into the database
        cursor.execute(
            "INSERT INTO team_members (name, role) VALUES (?, ?)",
            (name, role),
        )
        conn.commit()
        conn.close()

        return jsonify(
            {"status": "success", "message": "Team member added successfully!"}
        )

    except KeyError as e:
        return jsonify({"status": "error", "message": f"Missing field: {str(e)}"}), 400


@app.route("/team_members", methods=["GET"])
def get_team_members():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM team_members")
    team_members = cursor.fetchall()
    conn.close()

    # Convert rows to a list of dictionaries
    team_members_list = [
        {"id": member["id"], "name": member["name"]} for member in team_members
    ]

    return jsonify(team_members_list)


@app.route("/urgent_tasks", methods=["GET"])
def get_urgent_tasks():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Tasks WHERE is_urgent = 1")
    tasks = cursor.fetchall()
    conn.close()

    # Convert rows to a list of dictionaries
    tasks_list = [
        {
            "id": task["id"],
            "project_id": task["project_id"],
            "title": task["title"],
            "description": task["description"],
            "due_date": task["due_date"],
        }
        for task in tasks
    ]

    return jsonify(tasks_list)


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
