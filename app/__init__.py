from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = "my-key"
    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://rakib:1234@localhost:3306/smarttask_db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    from app.routes.auth import auth_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.add_tasks import add_bp
    from app.routes.edit_tasks import edit_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(add_bp)
    app.register_blueprint(edit_bp)
    

    @app.route("/")
    def home():
        return redirect(url_for("auth.login"))

    return app