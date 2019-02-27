import os
import sys
from flask import Flask, session, render_template, url_for, request, redirect
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import requests
import control_data as page_data

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
    page_data.add('page_active', 'home')
    page_data.add('page_title', 'PJ1 | Home')
    page_data.add('title', title)
    HTML = render_template('index.html', title = title, data = page_data.all())
    return f"Project 1: TODO <br> {HTML} <br>"

@app.route("/about")
def about():
    page_data.add('page_active', 'about')
    page_data.add('page_title', 'PJ1 | About')
    page_data.add('title', title)
    HTML = render_template('about.html', title = title, data = page_data.all())
    return f"Project 1: TODO <br> {HTML} <br>"

@app.route("/contact")
def contact():
    page_data.add('page_active', 'contact')
    page_data.add('page_title', 'PJ1 | Contact')
    page_data.add('title', title)
    HTML = render_template('contact.html', title = title, data = page_data.all())
    return f"Project 1: TODO <br> {HTML} <br>"

@app.route("/partisipan")
def partisipan():
    page_data.add('page_active', 'partisipan')
    page_data.add('page_title', 'PJ1 | Partisipan')
    page_data.add('title', title)
    HTML = render_template('partisipan.html', title = title, data = page_data.all())
    return f"Project 1: TODO <br> {HTML} <br>"

@app.route("/books")
def book():
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "dqUu9oCrKhE1x47m3oAUQ", "isbns": "9781632168146"});
    if res.status_code != 200:
        raise Exception("ERROR: API request unsuccessful.");    
    BOOK = res.json();

    page_data.add('page_active', 'book')
    page_data.add('page_title', 'PJ1 | Book')
    page_data.add('title', title)
    HTML = render_template('book.html', title = title, data = page_data.all())
    return f"Project 1: TODO <br> {HTML} <br>"

@app.route('/login', methods=['GET', 'POST'])
def login():
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
            return Response(stream_template('fail.html', code=pswd, username=usrn))
    else:
        page_data.add('page_active', 'login')
        page_data.add('page_title', 'PJ1 | Login')
        page_data.add('title', title)
        HTML = render_template('login.html', title = title, data = page_data.all())
        return f"Project 1: TODO <br> {HTML} <br>"

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    # app.run(debug=True,host='0.0.0.0', port=4000)
