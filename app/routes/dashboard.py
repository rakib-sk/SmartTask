from flask import Blueprint, request, render_template, url_for, session, redirect
from app.models import Tasks,User

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")

@dashboard_bp.route("")
def view_tasks():
    if "user_id" not in session:   
        return redirect(url_for("auth.login"))
        
    tasks = Tasks.query.filter_by(user_id=session["user_id"]).order_by(Tasks.scheduled_time).all()
    return render_template("dashboard.html", tasks=tasks)
