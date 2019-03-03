import os
import sys
import requests
from datetime import datetime
from flask import Flask, session, render_template, url_for, request, redirect
from flask_session import Session
from sqlalchemy import create_engine 
from sqlalchemy.sql import func
from sqlalchemy.orm import scoped_session, sessionmaker

from control_center import Data_control
from database import db_session
from models import User, Book

app = Flask(__name__)
title = "Project 1 (One)"

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

@app.route('/index')
@app.route("/")
def index():
    html_file='home'
    part={}
    page_data = Data_control()
    page_data.add('page_active', html_file)
    page_data.add('page_title', 'PJ1 | '+(html_file.title()))
    # Content data code
    page_data.add('title', title)

    # End content data
    log_st='logged_in' if session.get('logged_in') == True else 'logged_out'
    HTML = render_template(html_file+'.html', title = title,  part=part, data = page_data.all())
    return f"Project 1: TODO state='{log_st}' methot:'{request.method}'<br> {HTML} <br>"

@app.route("/about")
def about():
    html_file='about'
    part={}
    page_data = Data_control()
    page_data.add('page_active', html_file)
    page_data.add('page_title', 'PJ1 | '+(html_file.title()))
    # Content data code
    page_data.add('title', title)

    # End content data
    log_st='logged_in' if session.get('logged_in') == True else 'logged_out'
    HTML = render_template(html_file+'.html', title = title,  part=part, data = page_data.all())
    return f"Project 1: TODO state='{log_st}' methot:'{request.method}'<br> {HTML} <br>"

@app.route("/contact")
def contact():
    html_file='contact'
    part={}
    page_data = Data_control()
    page_data.add('page_active', html_file)
    page_data.add('page_title', 'PJ1 | '+(html_file.title()))
    # Content data code
    page_data.add('title', title)

    # End content data
    log_st='logged_in' if session.get('logged_in') == True else 'logged_out'
    HTML = render_template(html_file+'.html', title = title,  part=part, data = page_data.all())
    return f"Project 1: TODO state='{log_st}' methot:'{request.method}'<br> {HTML} <br>"

@app.route("/books", methods=["POST", "GET"])
def books():
    html_file='books'
    part={}
    page_data = Data_control()
    page_data.add('page_active', html_file)
    page_data.add('page_title', 'PJ1 | '+(html_file.title()))
    # Content data code
    page_data.add('title', title)

    part["search_bar"] = True
    part["book_card"] = True
    part["book_list"] = False

    res = requests.get("https://www.goodreads.com/search/index.xml", params={"key": "dqUu9oCrKhE1x47m3oAUQ", "q": "Ender%27s+Game"});
    if res.status_code != 200:
        raise Exception("ERROR: API request unsuccessful.");    
    book = res.text;

    key = request.url
    key = request.args.get('search')
    print(key)
    data_book = Book.query.filter(Book.author.like(f"%{key}%")).all()
    #data_book = Book.query.all()
    #data_book = Book.queryorder_by(func.random()).limit(5).all()
    page_data.add('search_key', key)
    page_data.add('data_book', data_book if not (key == None or key == "") else Book.query.order_by(func.random()).limit(8))
    # End content data
    log_st='logged_in' if session.get('logged_in') == True else 'logged_out'
    HTML = render_template(html_file+'.html', title = title,  part=part, data = page_data.all())
    return f"Project 1: TODO state='{log_st}' methot:'{request.method}'<br> {HTML} <br>"

@app.route("/cekbook")
def cekbook():
    html_file='book'
    part={}
    page_data = Data_control()
    page_data.add('page_active', html_file)
    page_data.add('page_title', 'PJ1 | '+(html_file.title()))
    # Content data code
    page_data.add('title', title)
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "dqUu9oCrKhE1x47m3oAUQ", "isbns": "9781632168146"});
    if res.status_code != 200:
        raise Exception("ERROR: API request unsuccessful.");    
    BOOK = res.json();
    # End content data
    log_st='logged_in' if session.get('logged_in') == True else 'logged_out'
    HTML = render_template(html_file+'.html', title = title, part=part, data = page_data.all())
    return f"Project 1: TODO state='{log_st}' methot:'{request.method}'<br> {HTML} <br>"

@app.route('/user')
def user():
    html_file='user'
    part={}
    page_data = Data_control()
    page_data.add('page_active', html_file)
    page_data.add('page_title', 'PJ1 | '+(html_file.title()))
    # Content data code
    page_data.add('title', title)

    data_user = User.query.all()
    part["register"]    = False;
    part["user_list"]   = True;
    page_data.add('data_user', data_user)
    page_data.add('user_active', user)

    # End content data
    log_st='logged_in' if session.get('logged_in') == True else 'logged_out'
    HTML = render_template(html_file+'.html', title = title,  part=part, data = page_data.all())
    return f"Project 1: TODO state='{log_st}' methot:'{request.method}'<br> {HTML} <br>"

@app.route('/register', methods=["POST", "GET"])
def register():
    html_file='register'
    part={}
    page_data = Data_control()
    page_data.add('page_active', html_file)
    page_data.add('page_title', 'PJ1 | '+(html_file.title()))
    # Content data code
    page_data.add('title', title)
    if request.method == 'POST':
        user = request.form['username']
        name = request.form['name']
        mail = request.form['email']
        pswd = request.form['password']

        #date = datetime.strptime(request.form['depature'], '%d-%m-%Y %H:%M %p')
        date = datetime.now()
        status = "valid"

        data_user = User.query.filter_by(user=user).first()
        if data_user==None:
            new_User = User(user, name, mail, pswd, rank, date, status)
            db_session.add(new_User)
            db_session.commit()
            print("user registering...")
            part["register"]    = True;
            part["user_list"]   = False;
        else:
            data_user = User.query.filter_by(user=user)
            part["register"]    = False;
            part["user_list"]   = True;
            page_data.add('data_user', data_user)
            page_data.add('user_active', user)
    else:
        part["register"]    = True;
        part["user_list"]   = False;
    # End content data
    log_st='logged_in' if session.get('logged_in') == True else 'logged_out'
    HTML = render_template(html_file+'.html', title = title,  part=part, data = page_data.all())
    return f"Project 1: TODO state='{log_st}' methot:'{request.method}'<br> {HTML} <br>"

@app.route('/login', methods=["POST", "GET"])
def login():
    page_data = Data_control()
    if request.method == 'POST':
        usrn = request.form['username']
        pswd = request.form['password']

        if True:
            session['logged_in'] = True
            session['username'] = request.form['username']
            print('login1:'+session['username'])
            sys.stdout.flush()
            return redirect(url_for('index'))
        else:
            #return Response(stream_template('fail.html', code=pswd, username=usrn))
            return redirect(url_for('login'))
    else:
        html_file='login'
        page_data.add('page_active', html_file)
        page_data.add('page_title', 'PJ1 | '+(html_file.title()))
        page_data.add('title', title)
        
        log_st='logged_in' if session.get('logged_in') == True else 'logged_out'
        HTML = render_template(html_file+'.html', title = title, data = page_data.all())
        return f"Project 1: TODO state='{log_st}' methot:'{request.method}'<br> {HTML} <br>"

@app.route('/logout', methods=["POST", "GET"])
def logout():
    # remove the username from the session if it's there
    session.pop('logged_in', None)
    session.pop('username', None)
    session.clear()
    return redirect(url_for('index'))

@app.route('/backend', methods=["POST", "GET"])
def backend():
    page_data = Data_control()
    if request.method == "POST":
        user = "admin"
        mail = "admin@flask.com"
        rank = "admin"
        #date = datetime.strptime(request.form['depature'], '%d-%m-%Y %H:%M %p')
        date = datetime.strptime('23-07-2018 07:23 AM', '%d-%m-%Y %H:%M %p')
        status = "valid"
        new_User = User(user, mail, rank, date, status)
        db_session.add(new_User)
        db_session.commit()
        return redirect("/", code=302)
    else:
        user = "admin"
        mail = "admin@flask.com"
        rank = "admin"
        #date = datetime.strptime(request.form['depature'], '%d-%m-%Y %H:%M %p')
        date = datetime.strptime('23-07-2018 07:23 AM', '%d-%m-%Y %H:%M %p')
        status = "valid"

        new_User = User(user, mail, rank, date, status)
        db_session.add(new_User)
        db_session.commit()

        user = User.query.all()
        page_data.add('page_active', 'login')
        page_data.add('page_title', 'PJ1 | Login')
        page_data.add('title', title)
        HTML = render_template('list.html', title = title, data = page_data.all(), user=user)
        return f"Project 1: TODO <br> {HTML} <br>"

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    # app.run(debug=True,host='0.0.0.0', port=4000)
