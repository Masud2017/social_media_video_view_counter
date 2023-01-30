from flask import Flask
from flask import request
from flask import render_template
from flask import abort, redirect, url_for
from src.AuthHandler import AuthHandler
from src.models.Models import db
from flask_migrate import Migrate


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///video_viewer.db"
db.init_app(app)
migrate = Migrate(app, db)

with app.app_context():
    db.create_all()

secret = "ds;fjasdklfjwefids;kfjsdklj234js;dklfjsd;sdfkjs;dfk"

auth_handler  = AuthHandler(secret)

@app.route("/",methods = ["GET"])
def index():
    return render_template("index.html")

@app.route("/login",methods = ["GET"])
def login():
    return render_template("login.html")

@app.route("/signup",methods = ["GET"])
def signup():
    return render_template("signup.html")

@app.route("/auth",methods = ["POST"])
def auth():
    print(request.form["username"])
    return redirect(url_for("index"))

@app.route("/reg",methods = ["POST"])
def reg():
    return redirect(url_for("index"))