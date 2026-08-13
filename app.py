import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'student-task-manager-key-9999'

# SQLite database setup at database.db
db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(300), nullable=True)
    due_date = db.Column(db.String(10), nullable=True)  # Format: YYYY-MM-DD
    completed = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Task {self.title}>'

# Create tables and populate some sample data if database is new
with app.app_context():
    db.create_all()
    if Task.query.count() == 0:
        sample_tasks = [
            Task(
                title="Complete Backend Fundamentals Project",
                description="Implement CRUD operations with Flask and Bootstrap.",
                due_date=datetime.now().strftime("%Y-%m-%d"),
                completed=False
            ),
            Task(
                title="Study Database Indexing",
                description="Read about B-Trees and query optimization in PostgreSQL.",
                due_date="2026-08-20",
                completed=True
            ),
            Task(
                title="Prepare for Midterm Exam",
                description="Revise algorithms and time complexity analyses.",
                due_date="2026-08-25",
                completed=False
            )
        ]
        db.session.bulk_save_objects(sample_tasks)
        db.session.commit()

# Context Processor to make datetime available in templates
@app.context_processor
def inject_now():
    return {'datetime': datetime}

# --- ROUTES ---

@app.route('/')
def index():
    # Retrieve optional filter parameter
    status_filter = request.args.get('filter', 'all')
    
    query = Task.query
    if status_filter == 'completed':
        query = query.filter_by(completed=True)
    elif status_filter == 'active':
        query = query.filter_by(completed=False)
        
    tasks = query.order_by(Task.due_date.asc(), Task.created_at.desc()).all()
    
    # Overview metrics
    total_count = Task.query.count()
    completed_count = Task.query.filter_by(completed=True).count()
    pending_count = total_count - completed_count
    
    return render_template(
        'index.html',
        tasks=tasks,
        current_filter=status_filter,
        total_count=total_count,
        completed_count=completed_count,
        pending_count=pending_count
    )

@app.route('/add', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        due_date = request.form.get('due_date', '').strip()

        # Basic server-side validation
        if not title:
            flash('Task title is required.', 'danger')
            return render_template('form.html', action_url=url_for('add_task'), is_edit=False, task_data=request.form)

        try:
            new_task = Task(
                title=title,
                description=description,
                due_date=due_date if due_date else None,
                completed=False
            )
            db.session.add(new_task)
            db.session.commit()
            flash('Task added successfully!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding task: {str(e)}', 'danger')
            return render_template('form.html', action_url=url_for('add_task'), is_edit=False, task_data=request.form)

    # GET request: render form for adding
    return render_template('form.html', action_url=url_for('add_task'), is_edit=False, task_data={})

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_task(id):
    task = Task.query.get_or_404(id)

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        due_date = request.form.get('due_date', '').strip()
        completed = 'completed' in request.form  # Checkbox value handling

        if not title:
            flash('Task title is required.', 'danger')
            return render_template('form.html', action_url=url_for('edit_task', id=id), is_edit=True, task_data=request.form, task=task)

        try:
            task.title = title
            task.description = description
            task.due_date = due_date if due_date else None
            task.completed = completed
            db.session.commit()
            flash('Task updated successfully!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating task: {str(e)}', 'danger')
            return render_template('form.html', action_url=url_for('edit_task', id=id), is_edit=True, task_data=request.form, task=task)

    # GET request: pre-populate form with existing task database values
    task_data = {
        'title': task.title,
        'description': task.description,
        'due_date': task.due_date,
        'completed': task.completed
    }
    return render_template('form.html', action_url=url_for('edit_task', id=id), is_edit=True, task_data=task_data, task=task)

@app.route('/delete/<int:id>', methods=['POST'])
def delete_task(id):
    task = Task.query.get_or_404(id)
    try:
        db.session.delete(task)
        db.session.commit()
        flash('Task deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting task: {str(e)}', 'danger')
        
    return redirect(url_for('index'))

@app.route('/complete/<int:id>', methods=['POST'])
def complete_task(id):
    task = Task.query.get_or_404(id)
    try:
        task.completed = not task.completed  # Toggle status
        db.session.commit()
        status_text = "completed" if task.completed else "marked active"
        flash(f'Task "{task.title}" {status_text}!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error toggling task completion: {str(e)}', 'danger')
        
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
