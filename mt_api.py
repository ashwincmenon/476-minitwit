import time
from sqlite3 import dbapi2 as sqlite3
from hashlib import md5
from datetime import datetime
from flask import Flask, request, abort, flash, g, _app_ctx_stack,jsonify,make_response
from werkzeug.security import check_password_hash, generate_password_hash
import jwt
import datetime
from functools import wraps
import uuid

# configuration
DATABASE1 = '/tmp/minitwit1.db'
DATABASE2 = '/tmp/minitwit2.db'
DATABASE3 = '/tmp/minitwit3.db'
PER_PAGE = 30
DEBUG = True
SECRET_KEY = b'_5#y2L"F4Q8z\n\xec]/'


# create our little application :)
app = Flask('minitwit')
app.config.from_object(__name__)
app.config.from_envvar('MINITWIT_SETTINGS', silent=True)
app.config['SECRET_KEY']='keepitsecret'

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    sqlite_db = sqlite3.connect(app.config['DATABASE1'])
    sqlite_db.row_factory = sqlite3.Row
    sqlite_db2 = sqlite3.connect(app.config['DATABASE2'])
    sqlite_db2.row_factory = sqlite3.Row
    sqlite_db3 = sqlite3.connect(app.config['DATABASE3'])
    sqlite_db3.row_factory = sqlite3.Row
    return (sqlite_db,sqlite_db2,sqlite_db3)

@app.teardown_appcontext
def close_database(exception):
    """Closes the database again at the end of the request."""
    top = _app_ctx_stack.top
    if hasattr(top, 'sqlite_db'):
        top.sqlite_db.close()
        top.sqlite_db2.close()
        top.sqlite_db3.close()


def init_db():
    """Initializes the database."""
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db[0].cursor().executescript(f.read())
    db[0].commit()
    with app.open_resource('schema.sql', mode='r') as f2:
        db[1].cursor().executescript(f2.read())
    db[1].commit()
    with app.open_resource('schema.sql', mode='r') as f3:
        db[2].cursor().executescript(f3.read())
    db[2].commit()

def query_db(query, args=(), one=False):
    """Queries the database and returns a list of dictionaries."""
    cur = get_db()
    ab = cur[0].execute(query, args)
    rv = ab.fetchall()
    if rv:
        database = "one"
        return (rv[0] if rv else None) if one else rv
    else:
        cd = cur[1].execute(query, args)
        rv = cd.fetchall()
        if rv:
            database = "two"
            return (rv[0] if rv else None) if one else rv
        else:
            ef = cur[2].execute(query, args)
            rv = ef.fetchall()
            if rv:
                database = "three"
            return (rv[0] if rv else None) if one else rv

def query_db_public(query, args=(), one=False):
    """Queries the database and returns a list of dictionaries."""
    cur = get_db()
    ab = cur[0].execute(query, args)
    first = ab.fetchall()
    cd = cur[1].execute(query, args)
    second = cd.fetchall()
    ef = cur[2].execute(query, args)
    third = ef.fetchall()
    rv = first + second + third
    return (rv[0] if rv else None) if one else rv

def get_user_id(username):
    """Convenience method to look up the id for a username."""
    rv = query_db('select user_id from user where username = ?',
                  [username], one=True)
    return rv[0] if rv else None


#Inserts values to the database
def populate_db():
    db = get_db()
    with app.open_resource('populatedb1.sql', mode='r') as f:
        db[0].cursor().executescript(f.read())
    db[0].commit()
    with app.open_resource('populatedb2.sql', mode='r') as f:
        db[1].cursor().executescript(f.read())
    db[1].commit()
    with app.open_resource('populatedb3.sql', mode='r') as f:
        db[2].cursor().executescript(f.read())
    db[2].commit()

#Creates the database tables
@app.cli.command('initdb')
def initdb_command():
    init_db()
    print('Initialized the database.')

#Inserts values to the database tables
@app.cli.command('populatedb')
def populatedb_command():
    populate_db()
    print('Inserted values to the database.')

#Wrap function to decode the token
def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization

        if auth is None:
            return jsonify({'message':'Login credentials required to authenticate'})
        user = query_db('''select * from user where
            username = ?''', [auth.username], one=True)

        if user is None:
            error = 'Invalid username'
            return jsonify({'message': error, 'Status Code': '500 Internal Server Error'}),500
        elif not check_password_hash(user['pw_hash'],
                                         auth.password):
            error = 'Invalid password'
            return jsonify({'message': error, 'Status Code': '500 Internal Server Error'}),500
        return f(*args, **kwargs)
    return decorated

def retrieve_userInfo():
    auth = request.authorization
    userID = get_user_id(auth.username)
    return userID

def retrieve_username():
    auth = request.authorization
    username = auth.username
    return username

def get_databaseNumber(username):
    cur = get_db()
    query = "select * from user where username = ?"
    ab = cur[0].execute(query, [username])
    rv = ab.fetchall()
    if rv:
        database = "one"
        return database
    else:
        cd = cur[1].execute(query, [username])
        rv = cd.fetchall()
        if rv:
            database = "two"
            return database
        else:
            ef = cur[2].execute(query, [username])
            rv = ef.fetchall()
            if rv:
                database = "three"
                return database

#"""--------------------API--------------------------------"""
#--------------------PUBLIC TIMLINE---------------------
@app.route('/api/publicTimeline')
def public_timeline():
    messages=(query_db_public('''
            select message.*, user.* from message, user
            where message.author_id = user.user_id
            order by message.pub_date desc'''))
    print(messages)
    return (jsonify([dict(r) for r in messages]),200)


#--------------------HOME TIMLINE---------------------
@app.route('/api/HomeTimeline', methods=['GET','POST'])
@require_auth
def home_timeline():
    userID = retrieve_userInfo()
    if request.method=='GET':
        messages=(query_db_public('''
                select message.*,user.* from message,user
                where message.author_id = user.user_id and (
                user.user_id = ? or
                user.user_id in (select whom_id from follower
                                    where who_id = ?))''',[userID, userID]))
        return jsonify([dict(r) for r in messages]),200
    if request.method=='POST':
        if request.json['text']:
            db = get_db()
            database = get_databaseNumber(request.authorization.username)
            if database == "one":
                db[0].execute('''insert into message (author_id, text, pub_date)
                  values (?, ?, ?)''', (userID, request.json['text'],
                                        int(time.time())))
                db[0].commit()
            elif database == "two":
                db[1].execute('''insert into message (author_id, text, pub_date)
                  values (?, ?, ?)''', (userID, request.json['text'],
                                        int(time.time())))
                db[1].commit()
            else:
                db[2].execute('''insert into message (author_id, text, pub_date)
                  values (?, ?, ?)''', (userID, request.json['text'],
                                        int(time.time())))
                db[2].commit()
        return jsonify({'message':'Your message has been recorded','Status Code': '200 OK'}),200


#--------------------REGISTER USER---------------------
@app.route('/api/register', methods=['POST'])
def register():
    """Registers the user."""
    db = get_db()
    id = uuid.uuid1()
    user_id = id.int
    reg =  user_id % 3
    exist = get_user_id(request.json['username'])
    if exist:
        return jsonify({'message':'Username already exists'})
    else:
        if reg == 0:
            db[0].execute('''insert into user (
                      user_id,username, email, pw_hash) values (?, ?, ?, ?)''',
                      [str(id),request.json['username'], request.json['email'],
                       generate_password_hash(request.json['password'])])
            db[0].commit()
        elif reg == 1:
                db[1].execute('''insert into user (
                          user_id, username, email, pw_hash) values (?, ?, ?, ?)''',
                          [str(id),request.json['username'], request.json['email'],
                           generate_password_hash(request.json['password'])])
                db[1].commit()
        else:
            db[2].execute('''insert into user (
                      user_id,username, email, pw_hash) values (?, ?, ?, ?)''',
                      [str(id),request.json['username'], request.json['email'],
                       generate_password_hash(request.json['password'])])
            db[2].commit()
        return jsonify({'message':'You were successfully registered and can login now'})


#--------------------LOGIN------------------------------
@app.route('/api/login', methods=['POST'])
def login():
    user = query_db('''select * from user where
        username = ?''',[request.json['username']], one=True)
    if user is None:
        error = 'Invalid username'
        return jsonify({'message': error, 'Status Code': '500 Internal Server Error'}),500
    elif not check_password_hash(user['pw_hash'],
                                     request.json['password']):
        error = 'Invalid password'
        return jsonify({'message': error, 'Status Code': '500 Internal Server Error'}),500
    else:
        return jsonify({'message':'User %s has logged in'% request.json['username']})


#--------------------USER TIMLINE---------------------
@app.route('/api/<username>/timeline',methods=['GET'])
def username_timeline(username):
    if request.method == 'GET':
        messages=(query_db('''
            select message.*,user.* from message, user
                where message.author_id = ? and user.username = ?''',[get_user_id(username),username]))
        return (jsonify([dict(r) for r in messages]),200)



#--------------------FOLLOW/UNFOLLOW USER-----------------------------
@app.route('/api/<username>/following', methods=['GET','DELETE'])
@require_auth
def follow_user(username):
    """Function to follow and unfollow another user."""
    userID = retrieve_userInfo()
    whom_id = get_user_id(username)
    if whom_id == userID:
        return jsonify({'message':'You cannot follow/unfollow yourself'})
    if request.method == 'GET':
        exist = query_db('select * from follower where who_id=? and whom_id=?',[userID,whom_id])
        db = get_db()
        if not exist:
            database = get_databaseNumber(username)
            if database == "one":
                db[0].execute('''insert into follower (who_id, whom_id) values (?, ?)''',
                  [userID, whom_id])
                db[0].commit()
            elif database == "two":
                  db[1].execute('insert into follower (who_id, whom_id) values (?, ?)',
                    [userID, whom_id])
                  db[1].commit()
            else:
                  db[2].execute('insert into follower (who_id, whom_id) values (?, ?)',
                    [userID, whom_id])
                  db[2].commit()
            return jsonify({'message':'You are now following %s' % username, 'Status Code': '200 OK'}),200
    if request.method == 'DELETE':
        db = get_db()
        database = get_databaseNumber(username)
        if database == "one":
            exist = db[0].execute('select * from follower where who_id=? and whom_id=?',[userID,whom_id])
            if exist:
                db[0].execute('delete from follower where who_id=? and whom_id=?',
                          [userID, whom_id])
                db[0].commit()
        elif database == "two":
            exist = db[1].execute('select * from follower where who_id=? and whom_id=?',[userID,whom_id])
            if exist:
                  db[1].execute('delete from follower where who_id=? and whom_id=?',
                            [userID, whom_id])
                  db[1].commit()
        else:
              db[2].execute('delete from follower where who_id=? and whom_id=?',
                        [userID, whom_id])
              db[2].commit()
        return jsonify({'message':'You are now unfollowing %s' % username, 'Status Code': '200 OK'}),200


#--------------------LOGOUT---------------------------------
@app.route('/api/logout')
@require_auth
def logout():
    return jsonify({'message':'You are logged out'})


#-----------------GET USER DETAIL---------------------------
@app.route('/api/userInfo/<user>')
def before_req(user):
        gUser = query_db('select * from user where username = ?',
                          [user], one=True)
        if gUser is not None:
            return (jsonify(dict(gUser)),200)
        else:
            return (jsonify(gUser),201)


@app.route('/api/followed/<username>/<profile>')
def follow_info(username,profile):
    userId = get_user_id(username)
    prof_id = get_user_id(profile)
    followed =  query_db('''select 1 from follower where
        follower.who_id = ? and follower.whom_id = ?''',
        [userId, prof_id],
        one=True) is not None
    return jsonify(followed)
