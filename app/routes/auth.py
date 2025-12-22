from flask import Blueprint, request, redirect, url_for, flash, render_template, session
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models import User

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")




@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        if not username or not email or not password:
            flash("Fill all fields", "danger")
            return redirect(url_for("auth.register"))

        if User.query.filter_by(email=email).first():
            flash("Email already exists", "warning")
            return redirect(url_for("auth.register"))

        hashed_password = generate_password_hash(password)

        user = User(
            username=username,
            email=email,
            password_hash=hashed_password
        )

        db.session.add(user)
        db.session.commit()

        flash("Registration successful", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html")






@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password_hash, password):
            session["user_id"] = user.id          
            session["username"] = user.username  
            flash("Login successful", "success")
            return redirect(url_for("dashboard.view_tasks"))

        flash("Invalid email or password", "danger")
        return redirect(url_for("auth.login"))

    return render_template("login.html")





@auth_bp.route("/logout")
def logout():
    session.pop("user_id", None)
    session.pop("username", None)
    flash("Logged out successfully", "success")
    return redirect(url_for("auth.login"))