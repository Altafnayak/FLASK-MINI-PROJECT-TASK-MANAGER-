# Student Task Manager

A simple, responsive web application built with Python Flask and Bootstrap 5 to demonstrate backend engineering fundamentals.

## Features
- **Add Task:** Create task with title, description, and due date.
- **View Tasks:** View dashboard list of tasks with filters (All, Active, Completed) and status banners.
- **Edit Task:** Edit title, description, due date, and completion status.
- **Mark Completed:** Toggle completion status directly from the home dashboard list.
- **Delete Task:** Remove task record from the SQLite database.

## Technologies Used
- Python 3
- Flask (Backend HTTP server and Jinja2 views templating)
- SQLite (Self-contained transactional relational database engine)
- Flask-SQLAlchemy (ORM layers mapping models to SQL queries)
- Bootstrap 5 (CSS component toolkit)

## Project Structure
```text
flask mini project/
├── app.py                  # Main Flask server and SQL database schema
├── database.db             # SQLite Database (generated on first execution)
├── requirements.txt        # Package dependencies list
├── README.md               # User guide documentation
├── static/
│   └── style.css           # Custom dark theme overriding Bootstrap styles
└── templates/
    ├── base.html           # Layout shell structure
    ├── index.html          # Tasks dashboard feed
    └── form.html           # Reusable add/edit task form
```

## How to Run Locally

1. Create a Python virtual environment:
   ```bash
   python -m venv venv
   ```
2. Activate virtual environment:
   - On Windows: `.\venv\Scripts\Activate.ps1`
   - On MacOS/Linux: `source venv/bin/activate`
3. Install packages:
   ```bash
   pip install -r requirements.txt
   ```
4. Start the local server:
   ```bash
   python app.py
   ```
5. View in browser at: `http://127.0.0.1:5000`
