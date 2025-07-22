from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import db
from app.models import Task

tasks_bp = Blueprint('tasks', __name__)  # Blueprint name = 'tasks'

@tasks_bp.route('/tasks', methods=['GET', 'POST'])  # ✅ added POST
def view_tasks():
    if 'user' not in session:
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        title = request.form.get('title')
        if title:
            new_task = Task(title=title, status='Pending')
            db.session.add(new_task)
            db.session.commit()
            flash('Task successfully created.', 'success')

    tasks = Task.query.all()
    return render_template('tasks.html', tasks=tasks)

@tasks_bp.route('/toggle/<int:task_id>', methods=['POST'])
def toggle_status(task_id):  # ✅ Corrected spelling
    task = Task.query.get(task_id)
    if task:
        if task.status == 'Pending':
            task.status = 'Working'
        elif task.status == 'Working':
            task.status = 'Done'
        else:
            task.status = 'Pending'
        db.session.commit()
    return redirect(url_for('tasks.view_tasks'))

@tasks_bp.route('/clear', methods=['POST'])
def clear_tasks():
    Task.query.delete()
    db.session.commit()
    flash('All tasks cleared!', 'info')
    return redirect(url_for('tasks.view_tasks'))  # ✅ correct blueprint name
