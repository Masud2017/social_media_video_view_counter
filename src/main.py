from flask import Flask,jsonify,flash
from flask import request
from flask import render_template
from flask import abort, redirect, url_for
from .models.Models import db
from flask_migrate import Migrate
from flask_login import login_manager,login_required
from .models.Models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager
from flask_login import login_user,logout_user
from flask_login import current_user

from .UrlProcessor  import UrlProcessor
from .UrlHandlerFactory import UrlHandlerFactory
from .models.Models import Url
import re
import os

from flask_socketio import SocketIO, emit, disconnect

from .VideoViewsStat import VideoViewsStat

from instagram_private_api import Client, ClientCompatPatch
from flask import g,copy_current_request_context

import atexit

from flask_apscheduler import APScheduler

import time
from sqlalchemy import exc,text



# global_insta_api_obj = Client("jibon123420", "@amiakjajabor0433")
# global_insta_api_obj = Client("khannaalankar2023", "alankarM@")




#?
app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret-key-goes-here'
# app. config["SQLALCHEMY_DATABASE_URI"] =  "sqlite:///video_viewer.db"

db_url = os.environ.get("CLEARDB_DATABASE_URL")
app.config["SQLALCHEMY_DATABASE_URI"] = db_url.split("?")[0]

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_POOL_RECYCLE'] = 299
app.config['SQLALCHEMY_POOL_TIMEOUT'] = 20

db.init_app(app)
migrate = Migrate(app, db,render_as_batch=True)

with app.app_context():
    db.create_all()

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

async_mode = None
# socket_ = SocketIO(app, async_mode=async_mode)

# task schedular 
def update_url_list():
    with app.app_context():
        url_list = Url.query.all()
        time.sleep(3)
        url_list = Url.query.all()


        for url_item in url_list:
            handler = UrlHandlerFactory.get_instance(url_item.url)
            try:
                updated_view_count = handler.scrap_data().get_video_view_count()
                print(url_item.url,updated_view_count)
                url_item.view_count = updated_view_count
                try:
                    db.session.commit()
                except exc.OperationalError:
                    db.session.commit()
            except KeyError:
                print("This url is causing the exception: ",url_item.url)
        
schedular = APScheduler()
schedular.init_app(app)
schedular.add_job(func=update_url_list,trigger='interval',minutes=25,id='update_url_list')
schedular.start()
atexit.register(lambda: schedular.shutdown())



# view routing area
@app.route("/",methods = ["GET"])
def index():
    if current_user.is_authenticated:
        return redirect(url_for("viewer")) 
    # return render_template("index.html")
    return redirect(url_for("login"))

@app.route("/login",methods = ["GET"])
def login():

    return render_template("login.html")

@app.route("/signup",methods = ["GET"])
def signup():
    return render_template("signup.html")

@app.route("/viewer",methods = ["GET"])
@login_required
def viewer():
    video_views_stat = VideoViewsStat()

    if (current_user.is_admin):
        return render_template("views_viewer.html",total_count_by_url_type=video_views_stat.get_total_views_count_by_url_type(), total_count = video_views_stat.get_total_views_value(), total_count_for_each_user = video_views_stat.get_total_views_by_user())

    return render_template("views_viewer.html")

@app.route("/setting",methods = ["GET"])
@login_required
def setting():
    return render_template("setting.html")


@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))

# controller routing area
@app.route("/auth",methods = ["POST"])
def auth():
    email = request.form.get('username')
    password = request.form.get('password')


    user = User.query.filter_by(email=email).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    # print(user.name)
    if not user or not check_password_hash(user.password, password):
        flash("Your password is wrong!")
        return redirect(url_for('login')) # if the user doesn't exist or password is wrong, reload the page

    login_user(user, remember=False)

    
    return redirect(url_for("index"))

@app.route("/reg",methods = ["POST"])
def reg():
    name = request.form["name"]
    email1 = request.form["username"]
    password = request.form["pass"]
    hashed_pass = generate_password_hash(password,method = 'sha256')

    user = User.query.filter_by(email=email1).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        return redirect(url_for('signup'))

    new_user = User(name = name, email = email1, password = hashed_pass)
    db.session.add(new_user)
    db.session.commit()


    return redirect(url_for("index"))



@app.route("/logout",methods = ["GET"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

@app.route("/add_url",methods = ["POST"])
# @login_required
def addUrl():
    url = request.form["url"]
    
    processor = UrlProcessor(url)
    processed_url = processor.get_processed_data()
    print(type(url))
    
    url_handler = UrlHandlerFactory.get_instance(url)
    user = User.query.filter_by(email=current_user.email).first()
    view_count = url_handler.scrap_data().get_video_view_count()

    url_ = Url.query.filter_by(url=url).first()
    if url_ : 
        print("url found so quiting")
        return {"code":"201"}
    print("url is not found so saving")

    new_url = Url(url = url,platform = processed_url[0], view_count = view_count)

    user.urls.append(new_url)

    db.session.add(new_url)
    db.session.commit()

    return {"code":"200"}

@app.route("/fetch_url_data",methods = ["get"])
def fetch_url_data():
    url = Url.query.filter_by(user_id=current_user.id).all()
    print("printing data")
    

    url_json = []
    
    if not url:
        return jsonify(url_json)

    for url_item in url:
        di = {"id":url_item.id,"url": url_item.url,"platform" : url_item.platform,"view_count": url_item.view_count}
        url_json.append(di)

    url_json.reverse()
    return jsonify(url_json)

@app.route("/refresh_list",methods = ["GET"])
def refresh_list():
    url_list = current_user.urls
    
    for url_item in url_list:
        handler = UrlHandlerFactory.get_instance(url_item.url)
        updated_view_count = handler.scrap_data().get_video_view_count()
        print(url_item.url,updated_view_count)
        url_item.view_count = updated_view_count
        db.session.commit()
    return jsonify({"code":"200"})

@app.route("/delete_url",methods = ["POST"])
def delete_url():
    id = request.form["id"]
    id = id.replace("/","")
    print("id printing " , id)
    uri_obj = Url.query.filter_by(id = id).first()
    print(uri_obj.url)
    db.session.delete(uri_obj)
    db.session.commit()

    return redirect(url_for('index'))

@app.route("/change_pass",methods = ["POST"])
def change_pass():
    old_pass = request.form["old_pass"]
    new_pass = request.form["new_pass"]

    user = User.query.filter_by(email=current_user.email).first()
    if not user or not check_password_hash(user.password, old_pass):
        flash("Old password is not matched with your account credential please try again!")
        return redirect(url_for('setting')) # if the user doesn't exist or password is wrong, reload the page
    user.password = generate_password_hash(new_pass,method = 'sha256')
    db.session.commit()

    return redirect(url_for("index"))



def try_reconnect():
    while True:
        try:
            db.session.rollback()

            db.session.execute(text("SELECT 1"))

            break
        except (exc.OperationalError, exc.ProgrammingError):
            time.sleep(1)


@app.before_request
def before_request():
    try:
        db.session.execute(text("SELECT 1"))

    except (exc.OperationalError, exc.ProgrammingError):
        try_reconnect()
# @app.before_first_request
# def admin_user_seeder():
#     # admin_user = User.query.filter_by(is_admin = True).first()

#     if (not admin_user.is_admin):
#         print("Registering admin user...")
#         admin_user = User(name = "Admin user", email = "khannaalankar2023@gmail.com",password=generate_password_hash("alankarM@",method = "sha256"),is_admin=True)
#         db.session.add(admin_user)
#         db.session.commit()
#     else:
#         print("Admin credential is already available in the database")



# web socket portion started

# @socket_.on('my_event', namespace='/sock')
# def test_message(message):
#     # session['receive_count'] = session.get('receive_count', 0) + 1
#     print(message["data"])
#     emit('my_response',
#          {'data': message['data'], 'count': 2})
# @socket_.on("refresh",namespace='/sock')
# def refresh(message):
#     url_list = current_user.urls
    
#     for url_item in url_list:
#         handler = UrlHandlerFactory.get_instance(url_item.url)
#         updated_view_count = handler.scrap_data().get_video_view_count()
#         print(url_item.url,updated_view_count)
#         url_item.view_count = updated_view_count
#         db.session.commit()
#     emit("refresh_ans",{'data':'data'})


# @socket_.on('my_broadcast_event', namespace='/sock')
# def test_broadcast_message(message):
#     # session['receive_count'] = session.get('receive_count', 0) + 1
#     emit('my_response',
#          {'data': message['data'], 'count': 2},
#          broadcast=True)


# @socket_.on('disconnect_request', namespace='/sock')
# def disconnect_request():
#     @copy_current_request_context
#     def can_disconnect():
#         disconnect()

#     # session['receive_count'] = session.get('receive_count', 0) + 1
#     emit('my_response',
#          {'data': 'Disconnected!', 'count': 2},
#          callback=can_disconnect)
