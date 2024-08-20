import sqlite3


def create_tables():
    conn = sqlite3.connect("project_management.db")
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
        task_name TEXT NOT NULL,
        due_date DATE,
        FOREIGN KEY (project_id) REFERENCES projects(id)
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


if __name__ == "__main__":
    create_tables()


# project_management
