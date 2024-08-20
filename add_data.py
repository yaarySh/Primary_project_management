import sqlite3


def insert_test_data():
    conn = sqlite3.connect("project_management.db")
    cursor = conn.cursor()

    # Insert into projects
    cursor.execute(
        """
    INSERT INTO projects (name, description, start_date, end_date) VALUES (?, ?, ?, ?)
    """,
        ("Project Alpha", "Description for Project Alpha", "2024-08-01", "2024-12-31"),
    )

    # Insert into tasks
    cursor.execute(
        """
    INSERT INTO tasks (project_id, task_name, due_date) VALUES (?, ?, ?)
    """,
        (1, "Task 1 for Project Alpha", "2024-08-15"),
    )

    # Insert into team_members
    cursor.execute(
        """
    INSERT INTO team_members (name, role) VALUES (?, ?)
    """,
        ("John Doe", "Developer"),
    )

    # Insert into project_team
    cursor.execute(
        """
    INSERT INTO project_team (project_id, team_member_id) VALUES (?, ?)
    """,
        (1, 1),
    )  # Linking Project Alpha (id=1) with John Doe (id=1)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    insert_test_data()
