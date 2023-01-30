from flask import Flask
from flask import request
from flask import render_template
from flask import abort, redirect, url_for




app = Flask(__name__)

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
    return redirect(url_for("index"))

@app.route("/reg",methods = ["POST"])
def reg():
    return redirect(url_for("index"))