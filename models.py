from sqlalchemy import Column, Integer, String, DateTime
from database import Base
from datetime import datetime

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    user = Column(String(50))
    name = Column(String(128))
    mail = Column(String(128))
    password = Column(String(128))
    rank = Column(String(50))
    date = Column(DateTime, default=datetime.utcnow)
    stat = Column(String(120))

    def __init__(self, user=None, name=None, mail=None, password=None, rank=None, date=None, stat=None):
        self.user = user
        self.name = name
        self.mail = mail
        self.password = password
        self.rank = rank
        self.date = date
        self.stat = stat

    def __repr__(self):
        return '<user %r>' % (self.user)

class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    isbn = Column(String(50))
    title = Column(String(120))
    author = Column(String(50))
    year = Column(String(50))
    date = Column(DateTime, default=datetime.utcnow)
    stat = Column(String(120), default="ready")

    def __init__(self, isbn=None, title=None, author=None, year=None, date=None, stat=None):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.year = year
        self.date = date
        self.stat = stat

    def __repr__(self):
        return '<book %r>' % (self.book)

class Review(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True)
    bok_id = Column(Integer)
    b_isbn = Column(String(50))
    usr_id = Column(Integer)
    name = Column(String(50))
    review = Column(String(256))
    rating = Column(Integer)
    date = Column(DateTime, default=datetime.utcnow)
    stat = Column(String(120), default="ready")

    def __init__(self, bok_id=None, b_isbn=None, usr_id=None, name=None, review=None, rating = None, date=None, stat=None):
        self.bok_id = bok_id
        self.b_isbn = b_isbn
        self.usr_id = usr_id
        self.name = name
        self.review = review
        self.rating = rating
        self.date = date
        self.stat = stat

    def __repr__(self):
        return '<review %r>' % (self.review)