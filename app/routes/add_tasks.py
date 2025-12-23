from flask import Blueprint, request, render_template, url_for, session, redirect,flash
from app.models import Tasks,User
from app import db

add_bp = Blueprint("add",__name__,url_prefix="/add")

@add_bp.route("/add_tasks", methods=["GET", "POST"])
def add_tasks():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        content = request.form.get("content")
        scheduled_time = request.form.get("scheduled_time")

        if content and scheduled_time:
            new_tasks = Tasks(
                user_id = session["user_id"],
                content=content,
                scheduled_time=scheduled_time,
                status="pending"
            )
            db.session.add(new_tasks)
            db.session.commit()
            flash("Task was saved!", "success")

        return redirect(url_for("dashboard.view_tasks"))

    return render_template("add_tasks.html")