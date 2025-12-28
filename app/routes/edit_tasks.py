from flask import Blueprint, request, render_template, url_for, session, redirect,flash
from app.models import Tasks,User
from app import db

edit_bp = Blueprint("edit",__name__,url_prefix="/edit")

@edit_bp.route("/edit_tasks/<int:task_id>", methods=["GET", "POST"])
def edit_tasks(task_id):
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    task = Tasks.query.filter_by(
        id=task_id,
        user_id=session["user_id"]
    ).first()

    if task is None:
        flash("Task not found", "danger")
        return redirect(url_for("dashboard.view_tasks"))

    if request.method == "POST":
        task.content = request.form.get("content")
        task.scheduled_time = request.form.get("scheduled_time")

        db.session.commit()
        flash("Task updated!", "success")
        return redirect(url_for("dashboard.view_tasks"))

    return render_template("edit_tasks.html", task=task)
    
    
@edit_bp.route("/delete_task/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    task = Tasks.query.filter_by(
        id=task_id,
        user_id=session["user_id"]
    ).first()

    if task is None:
        flash("Task not found", "danger")
        return redirect(url_for("dashboard.view_tasks"))

    db.session.delete(task)
    db.session.commit()
    flash("Task deleted!", "success")
    return redirect(url_for("dashboard.view_tasks"))    