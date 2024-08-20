# Project Management System
# Tables
# Projects

# id (Primary Key)
# name (String)
# description (String)
# start_date (Date)
# end_date (Date)
# Tasks

# id (Primary Key)
# project_id (Foreign Key referencing Projects.id)
# name (String)
# description (String)
# assigned_to (Foreign Key referencing TeamMembers.id)
# status (String: e.g., "Not Started", "In Progress", "Completed")
# due_date (Date)
# TeamMembers

# id (Primary Key)
# name (String)
# role (String: e.g., "Developer", "Manager", "Tester")
# email (String)
# CRUD Operations
# Projects

# Create: Add a new project with details like name, description, start date, and end date.
# Read: View details of a specific project or list all projects.
# Update: Modify project details.
# Delete: Remove a project from the system.
# Tasks

# Create: Add a new task to a project, including assigning it to a team member.
# Read: View details of a specific task or list all tasks within a project.
# Update: Modify task details, such as changing the status or reassigning it.
# Delete: Remove a task from a project.
# TeamMembers

# Create: Add a new team member with details like name, role, and email.
# Read: View details of a specific team member or list all team members.
# Update: Modify team member details.
# Delete: Remove a team member from the system.
# Database Relationships
# A Project can have multiple Tasks.
# A Task is assigned to a single TeamMember.
# A TeamMember can be assigned to multiple Tasks across different Projects.
# Example API Endpoints
# Projects

# POST /projects - Create a new project
# GET /projects - List all projects
# GET /projects/<id> - Get details of a specific project
# PUT /projects/<id> - Update a project
# DELETE /projects/<id> - Delete a project
# Tasks

# POST /projects/<project_id>/tasks - Create a new task within a project
# GET /projects/<project_id>/tasks - List all tasks within a project
# GET /tasks/<id> - Get details of a specific task
# PUT /tasks/<id> - Update a task
# DELETE /tasks/<id> - Delete a task
# TeamMembers

# POST /team_members - Create a new team member
# GET /team_members - List all team members
# GET /team_members/<id> - Get details of a specific team member
# PUT /team_members/<id> - Update a team member
# DELETE /team_members/<id> - Delete a team member
