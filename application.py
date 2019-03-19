import os
import sys
import requests
from pprint import pprint
from datetime import datetime
from flask import Flask, session, render_template, url_for, make_response, request, redirect, jsonify, flash, abort
from flask_scss import Scss
from flask_session import Session
from sqlalchemy import create_engine 
from sqlalchemy.sql import func
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_hashing import Hashing as Hashing
from flask_login import LoginManager, current_user, login_user, logout_user, login_required, UserMixin
from datetime import datetime

from control_center import Data_control
from database import db_session
from models import User as db_User

# Declare FLASK app
app = Flask(__name__)
title = "Project 1 (One)"

# Configure app to use in filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["HASHING_METHOD"] = "sha256"
app.config['SECRET_KEY'] = "lkkajdghdadkglajkgah" # a secret key for login

# Init some fungtion needed in app
Session(app)
hash = Hashing(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'index' # the login view of your application
login_manager.login_message = 'Silahkan login utuk dapat mengakses halaman.'
login_manager.login_message_category = "warning"
Scss(app, static_dir='static', asset_dir='static')

class User(UserMixin):
  def __init__(self,id):
    self.id = id

# Route Main Front Page
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
    HTML = render_template(html_file+'.html', title = title,  part=part, data = page_data.all())
    return HTML

# Route About Author
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
    return f"{HTML}"

# Route Contact
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
    return f"{HTML}"

# Route Book search
@app.route("/books", methods=["POST", "GET"])
@login_required
def books():
    # Page initial data
    html_file='books'
    part={}
    page_data = Data_control()
    page_data.add('page_active', html_file)
    page_data.add('page_title', 'PJ1 | '+(html_file.title()))
    page_data.add('title', title)
    part["search_bar"] = True
    part["book_card"] = True
    part["book_list"] = False

    # Content data code
    req = request.url
    req = request.args.get('search')
    if req != None:
        key = "%"+ req.title() + "%"
        data_book = db_session.execute("SELECT * FROM books WHERE isbn LIKE :key OR\
            title LIKE :key OR\
            author LIKE :key LIMIT 15", {"key": key} )
        data_book = data_book.fetchall()
        db_session.commit()
    else:
        data_book = db_session.execute("SELECT * FROM books ORDER BY random() LIMIT 10")
        data_book = data_book.fetchall()
        db_session.commit()

    # Get Book info
    colection=[]
    print(data_book)
    for book in data_book:
        colection.append({
            'title'        : book.title,
            'year'        : book.year,
            'isbn'        : book.isbn,
            'author'    : book.author,
            'id'        : book.id,
            'img_url'    : f"http://covers.openlibrary.org/b/isbn/{book.isbn}-M.jpg"})
    data_book = colection

    # End get info buku

    page_data.add('search_key', req)
    page_data.add('data_book', data_book)
    # End content data
    log_st='logged_in' if session.get('logged_in') == True else 'logged_out'
    HTML = render_template(html_file+'.html', title = title,  part=part, data = page_data.all())
    return f"{HTML}"

# Route Book detail
@app.route("/book/<isbn>")
@app.route("/book")
@login_required
def book(isbn=None):
    # Cek if theare isbn if not redirect to search book page
    if isbn == None: redirect(url_for('books'))

     # Page initial data
    html_file='book'
    part={}
    page_data = Data_control()
    page_data.add('page_active', html_file)
    page_data.add('page_title', 'PJ1 | '+(html_file.title()))
    page_data.add('title', title)
    part["book_leflet"] = True

    # Content data code
    # Get book info from database
    data_book = db_session.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn": isbn} )
    data_book = data_book.fetchall()
    book = data_book[0]

    # Get Book rating from Goodsreads
    try:    
        # Request data from goodreads
        goodreads = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "dqUu9oCrKhE1x47m3oAUQ", "isbns": book.isbn})

        # Raise error if response failed
        if goodreads.status_code != 200:
            raise Exception("ERROR: API request unsuccessful.")

        # Prosses data from Goodsread
        goodreads = goodreads.json()
        goodreads = goodreads['books'][0]
    
        img_url = f"http://covers.openlibrary.org/b/isbn/{book.isbn}-M.jpg"
    except:
        # Aditional dummy info =>
        rating  = 'We are offline'
        img_url = '../static/dummy_cover.jpg'
        print(f"Offline using dummy \nrating: {rating} \nimage: {img_url}")
    finally:print('')

    # Build data structur to pass on tempelate
    data_book = {
        'title'             : book.title,
        'year'              : book.year,
        'isbn'              : book.isbn,
        'author'            : book.author,
        'id'                : book.id,
        'rating'            : goodreads['average_rating'], 
        'work_rating_count' : goodreads['work_ratings_count'],
        'img_url'           : img_url
         }
    page_data.add('data_book', data_book)

    # End content data
    log_st='logged_in' if session.get('logged_in') == True else 'logged_out'
    HTML = render_template(html_file+'.html', title = title,  part=part, data = page_data.all())
    return f"{HTML}"

# Route to user list
@app.route('/user')
@login_required
def user():
    # Page initial data
    html_file='user'
    part={}
    page_data = Data_control()
    page_data.add('page_active', html_file)
    page_data.add('page_title', 'PJ1 | '+(html_file.title()))
    # Content data code
    page_data.add('title', title)

    data_user = db_User.query.all()
    part["register"]    = False
    part["user_list"]   = True
    page_data.add('data_user', data_user)
    page_data.add('user_active', user)

    # End content data
    log_st='logged_in' if session.get('logged_in') == True else 'logged_out'
    HTML = render_template(html_file+'.html', title = title,  part=part, data = page_data.all())
    return f"{HTML}"

# Route for register page and post
@app.route('/register', methods=["POST", "GET"])
def register():    
    # Page initial data
    html_file='register'
    part={}
    page_data = Data_control()
    page_data.add('page_active', html_file)
    page_data.add('page_title', 'PJ1 | '+(html_file.title()))
    page_data.add('title', title)
    
    # clear user data in session
    session.clear()

    # Cek if user request via POST
    if request.method == 'POST':
        # Get input user
        user = request.form['username']
        name = request.form['name']
        mail = request.form['email']
        password = request.form['password']
        rank = "costumer"
        date = datetime.now()
        status = "valid"

        # Cek if user exist
        cek_user = db_session.execute('SELECT * FROM users WHERE "user" = :user',
        {'user': user}).fetchall()

        # Generade hash 
        hash_password = hash.hash_value(password, salt='AIk0bQ1dxHAWG1yq2iGPK6GrM9oe5h3V')

        # If user not found create user else show messege
        if cek_user==[]:
            # Insert user data into database
            db_session.execute('INSERT INTO users ("user", "name", "mail", "password", "rank", "date", "stat") VALUES (:user, :name, :mail, :password, :rank, :date, :status)',
                {"user":user, "name":name, "mail":mail, "password":hash_password, "rank":rank, "date":date, "status":status})
            
            # Closing trasaction
            db_session.commit()

            # Notif user that register is sucsessful
            print(f"{user} registering...")
            flash('Register sucsessful, Welcome '+name, 'success')
            redirect(url_for('index'))
        else:
            # Notif user that username already taken
            flash('Sorry! your username already taken!', 'danger')
            data_user = cek_user
            part["register"]    = False
            part["user_list"]   = True
            page_data.add('data_user', data_user)
            page_data.add('user_active', user)
    else:
        part["register"]    = True
        part["user_list"]   = False
    # End content data
    HTML = render_template(html_file+'.html', title = title,  part=part, data = page_data.all())
    return HTML

# Route for login API
@app.route('/login', methods=["POST"])
def login():
    # Cek if user request via POST
    if request.method == 'POST':
        # clear user data in session
        session.clear()

        # Cek if user request via POST
        user = request.form['username']
        password = request.form['password']
               
        # Cek user in database
        user_hash = db_session.execute('SELECT password, name FROM users WHERE \
            "user" = :user', 
            {'user': user}).fetchone()

        # If user found and password macth change stat to login
        if login != None and hash.check_value(user_hash[0], password, salt='AIk0bQ1dxHAWG1yq2iGPK6GrM9oe5h3V'):
            # Save login data into sessions
            session['logged_in'] = True
            session['user_id'] = 1
            session['user_name'] = request.form['username']
            session['name'] = user_hash[1]
            login_user(User(1))
            # Welcome user and redirected to book page
            print('login:'+ session['user_name'])
            flash('Welcome '+session['name'], 'success')
            sys.stdout.flush()
            return redirect(url_for('books'))
        else:
            # Notif user and redirected to index
            flash('Sorry! username or password you enter is wrong!', 'danger')
            return redirect(url_for('index'))

# ROute for logout API
@app.route('/logout', methods=["POST", "GET"])
@login_required
def logout():
    # remove the username from the session if it's there
    logout_user()
    session.pop('logged_in', None)
    session.pop('username', None)
    session.clear()
    return redirect(url_for('index'))

# Route for API
@app.route("/API/<key>/<isbn>", methods=["GET","POST"])
@app.route("/API/<key>", methods=["GET","POST"])
@app.route("/API")
def API(key=None, isbn=None):
    if key == None: abort(404)
    print(f"API key: \n{key}")
    if request.method == 'POST' and key == 'get_review' and isbn != None:
        # Cek if user login if not terminat it
        if not session['logged_in']: abort(404)

        # Get book review data from database
        #data_book = Review.query.filter_by(b_isbn=isbn)
        data_review = db_session.execute('SELECT * FROM reviews WHERE b_isbn = :b_isbn',{"b_isbn":isbn}).fetchall()
        db_session.commit()

        # Build data structur to send to browser
        colection={}
        num = 0
        for review in data_review:
            colection[num]=({
                'id'      : review.id,
                'book_id' : review.bok_id,
                'user_id' : review.usr_id,
                'name'    : review.name,
                'rating'  : int(review.rating),
                'review'  : review.review,
                'date'    : review.date
                })
            num = num+1
        data_review = colection
        
        # Convert data to json nad send it to browser
        return jsonify(data_review)

    elif request.method == 'POST' and key == 'add_review' and isbn != None:
        # Cek if user login if not terminat it
        if not session['logged_in']: abort(404)

        # Get request data
        rating = request.form.get('rating')
        review = request.form.get('review')

        # Get user data
        curent_user = session['user_id']
        curent_name = session['user_name']

        # Cek id book
        base_data = db_session.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn":isbn}).fetchone()
        bookID = base_data[0]

        # Cek for user submision 
        base_data = db_session.execute("SELECT * FROM reviews WHERE \
            usr_id = :usr_id AND\
            bok_id = :bok_id",{"usr_id":curent_user, "bok_id":bookID })
        if base_data.rowcount == 1:
            return "Maaf anda hanya dapat mengirimkan review sekali saja"

        # Convert rating into integer
        rating = int(rating)
        
        # Input review into database
        if base_data.rowcount == 0:
            db_session.execute("INSERT INTO reviews (bok_id, b_isbn, usr_id, name, review, rating, date, stat) VALUES \
            (:bok_id, :b_isbn, :usr_id, :name, :review, :rating, :date, :stat)",
            {"bok_id":bookID,
            "b_isbn":isbn, 
            "usr_id":curent_user, 
            "name":curent_name, 
            "review":review,
            "rating":rating,
            "date":datetime.now(),
            "stat":"vaid"})

        #data_book = Review.query.filter_by(b_isbn=isbn)
        data_review = db_session.execute('SELECT * FROM reviews WHERE b_isbn = :b_isbn',{"b_isbn":isbn}).fetchall()
        
        # Ending data transmision and close database connection
        db_session.commit()

        # Build data structur to send to browser
        colection={}
        num = 0
        for review in data_review:
            colection[num]=({
                'id'      : review.id,
                'book_id' : review.bok_id,
                'user_id' : review.usr_id,
                'name'    : review.name,
                'rating'  : int(review.rating),
                'review'  : review.review,
                'date'    : review.date
                })
            num = num+1
        
        # Convert data to json nad send it to browser
        return jsonify(colection)
    
    elif request.method == 'GET' and key != None:
        # Get request data
        isbn = key
        
        # Request data from goodreads      
        goodreads = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "dqUu9oCrKhE1x47m3oAUQ", "isbns": isbn})

        # Raise error if response failed
        if goodreads.status_code != 200:
            raise Exception("ERROR: API request unsuccessful.")

        # Prosses data from Goodsread
        goodreads = goodreads.json()
        goodreads = goodreads['books'][0]

        # Get book book and review data from database
        data_book = db_session.execute('SELECT * FROM books WHERE isbn = :b_isbn',{"b_isbn":isbn}).fetchone()
        data_review = db_session.execute('SELECT COUNT(review), AVG(rating) FROM reviews WHERE b_isbn = :b_isbn',{"b_isbn":isbn}).fetchall()[0]
        db_session.commit()

        print(data_book)
        # Build data structur to send to browser
        a = {
            "title" : data_book.title,
            "author" : data_book.author,
            "year" : data_book.year,
            "isbn" : data_book.isbn,
            "review_count" : data_review.count,
            "average_score" : round(float(data_review.avg)),
            "rating" : goodreads['average_rating'], 
            "work_rating_count" : goodreads['work_ratings_count'],
        }

        # Convert data to json nad send it to browser
        return jsonify(a)
    
    else: abort(404)

# Route to manage user
@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@login_manager.unauthorized_handler
def unauthorized():
    # Redirect to home
    response = make_response(redirect(url_for('index'), code=302))
    response.headers['url'] = 'parachutes are cool'
    return response

# Route to manage user
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    # app.run(debug=True,host='0.0.0.0', port=4000)
