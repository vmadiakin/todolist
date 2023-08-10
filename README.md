#Todolist

Todolist is a simple task planner that helps you manage your tasks and to-dos.

## Description

Todolist provides a user-friendly interface for creating, editing, and tracking tasks. You can create tasks, set due dates for them, add descriptions, and mark them as completed as they are completed. It will help you organize your work, manage projects and improve your productivity.

## Stack

-Python 3.11
- Django
- postgres

## How to start

Follow these steps to get the project up and running:

1. Install Poetry if you haven't already installed it by running the following command:
`pip poetry install`

2. Install the dependencies by running the following command:
`poetry install`
This command will read the `pyproject.toml` file and install all dependencies into your project's virtual environment.
3. Create a `.env` file in the root directory of the project and specify the necessary values for environment variables, such as database settings, secret key, and others.

4. Apply the database migrations by running the following command:
`python manage.py migrate`

5. Run the project using the following command:
`python manage.py runserver`

6. Open a browser and navigate to `http://localhost:8000` to access Todolist.

Make sure you have Python 3.11 installed and Postgres up and running correctly before running the project.
