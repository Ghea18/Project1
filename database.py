import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Set up database
# Check for environment variable
if not os.getenv("DATABASE_URL"):
    #raise RuntimeError("DATABASE_URL is not set") 
else:
    engine = create_engine(os.getenv("DATABASE_URL"))
db_session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

def import_book(filename='books.csv', r=False):
    from models import Book
    from time import time
    from datetime import datetime
    import csv
    t = time()
    try:
        skiphead = 1
        csvfile = open(filename, 'r', newline='')
        # process subsequent lines of the file
        infile = csv.reader(csvfile, delimiter=',', quotechar='"')
        for data in infile:
            if skiphead == 1: skiphead = 0; continue
            if data == "": continue
            # turn the line into a student record \t \n \s
            # new_row = Books(**{ 'date'  : datetime.now(), 'stat'  : 'valid'})

            db_session.execute("INSERT INTO books (isbn, title, author, year, date, stat) VALUES (:isbn, :title, :author,:year, :date, :stat)",
            {   'isbn'  : data[0],
                'title' : data[1],
                'author': data[2],
                'year'  : data[3],
                'date'  : datetime.now(), 
                'stat'  : 'valid'})
            db_session.commit()
            print(f"{data[1]} has been success add in to database")
        csvfile.close()
    except:
        print("Error, roolback...") if r else 1+1
        db_session.rollback()
    finally:
        print("Close Session") if r else 1+1
        db_session.close()
    print(f"Time Elapsed: {str(time()-t)}s") if r else 1+1

def import_user(filename='users.csv', r=False):
    from models import User
    from time import time
    from datetime import datetime
    import csv
    t = time()
    try:
        skiphead = 1
        csvfile = open(filename, 'r', newline='')
        # process subsequent lines of the file
        infile = csv.reader(csvfile, delimiter=',', quotechar='"')
        for data in infile:
            if skiphead == 1: skiphead = 0; continue
            if data == "": continue
            # turn the line into a student record \t \n \s
            new_row = User(**{
                'user'  : data[1],
                'name'  : data[2],
                'mail'  : data[3],
                'pswd'  : data[4],
                'rank'  : data[5],
                'date'  : datetime.now(), 
                'stat'  : 'valid'})
            db_session.add(new_row)
            print(f"add:{data}") if r else 1+1
        print("finalize...") if r else 1+1
        db_session.commit()
        csvfile.close()
    except:
        print("Error, roolback...") if r else 1+1
        db_session.rollback()
    finally:
        print("Close Session") if r else 1+1
        db_session.close()
    print(f"Time Elapsed: {str(time()-t)}s") if r else 1+1

def init_db():
    import models
    from time import time
    msg, t = "", time()
    try:
        msg += "Creating Database: "
        Base.metadata.create_all(bind=engine)
        msg += "OK!\n"
    except Exception as e:
        msg += "FAIL!\n"
    finally:
        msg += f"Time Elapsed: {str(time()-t)}s\n"
    try:
        msg += "Importing Book data: "
        r = import_book('books.csv', False)
        msg += f"OK!\n"
    except Exception as e:
        msg += "FAIL!\n"
    finally:
        msg += f"Time Elapsed: {str(time()-t)}s\n"
    try:
        msg += "Importing Book data: "
        r = import_user('users.csv', False)
        msg += f"OK!\n"
    except Exception as e:
        msg += "FAIL!\n"
    finally:
        msg += f"Time Elapsed: {str(time()-t)}s\n"
    print(msg)
