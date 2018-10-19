# -*- coding: utf-8 -*-
"""
    MiniTwit
    ~~~~~~~~

    A microblogging application written with Flask and sqlite3.

    :copyright: © 2010 by the Pallets team.
    :license: BSD, see LICENSE for more details.
"""

import time
from sqlite3 import dbapi2 as sqlite3
from hashlib import md5
from datetime import datetime
from flask import Flask, request, session, url_for, redirect, \
     render_template, abort, g, flash, _app_ctx_stack
from werkzeug import check_password_hash, generate_password_hash
import requests


# configuration
DATABASE = '/tmp/minitwit.db'
PER_PAGE = 30
DEBUG = True
SECRET_KEY = b'_5#y2L"F4Q8z\n\xec]/'

# create our little application :)
app = Flask('minitwit')
app.config.from_object(__name__)
app.config.from_envvar('MINITWIT_SETTINGS', silent=True)



def format_datetime(timestamp):
    """Format a timestamp for display."""
    return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d @ %H:%M')


def gravatar_url(email, size=80):
    """Return the gravatar image for the given email address."""
    return 'https://www.gravatar.com/avatar/%s?d=identicon&s=%d' % \
        (md5(email.strip().lower().encode('utf-8')).hexdigest(), size)

@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        url = "http://localhost:8080/api/userInfo/" + session['username']
        resp = requests.get(url = url)
        g.user = resp.json()


@app.route('/')
def timeline():
    """Shows a users timeline or if no user is logged in it will
    redirect to the public timeline.  This timeline shows the user's
    messages as well as all the messages of followed users.
    """
    if not g.user:
        return redirect(url_for('public_timeline'))
    r = requests.get("http://localhost:8080/api/HomeTimeline", auth=(session['username'],session['password']))
    return render_template('timeline.html', messages=r.json())


@app.route('/public')
def public_timeline():
    """Displays the latest messages of all users."""
    r = requests.get("http://localhost:8080/api/publicTimeline")
    return render_template('timeline.html', messages=r.json())


@app.route('/<username>')
def user_timeline(username):
    """Display's a users tweets."""
    url = "http://localhost:8080/api/userInfo/" + username
    response = requests.get(url = url)
    profile_user = response.json()
    url_time = "http://localhost:8080/api/" + username + "/timeline"
    if profile_user is None:
        abort(404)
    followed = False
    if g.user:
        url = "http://localhost:8080/api/followed" + "/"+  session['username'] + "/" + profile_user['username']
        response = requests.get(url = url)
        followed = response.json()
    r = requests.get(url = url_time)
    return render_template('timeline.html', messages=r.json(),followed=followed,profile_user=profile_user)


@app.route('/<username>/follow')
def follow_user(username):
    """Adds the current user as follower of the given user."""
    if not g.user:
        abort(401)
    url = "http://localhost:8080/api/userInfo/" + username
    r = requests.get(url = url)
    user = r.json()
    whom_id = user['user_id']
    if whom_id is None:
        abort(404)
    url = "http://localhost:8080/api/" + username + "/following"
    r = requests.get(url, auth=(session['username'],session['password']))
    flash('You are now following "%s"' % username)
    return redirect(url_for('user_timeline', username=username))


@app.route('/<username>/unfollow')
def unfollow_user(username):
    """Removes the current user as follower of the given user."""
    if not g.user:
        abort(401)
    url = "http://localhost:8080/api/userInfo/" + username
    r = requests.get(url = url)
    user = r.json()
    whom_id = user['user_id']
    if whom_id is None:
        abort(404)
    url = "http://localhost:8080/api/" + username + "/following"
    r = requests.delete(url, auth=(session['username'],session['password']))
    flash('You are no longer following "%s"' % username)
    return redirect(url_for('user_timeline', username=username))


@app.route('/add_message', methods=['POST'])
def add_message():
    """Registers a new message for the user."""
    if 'user_id' not in session:
        abort(401)
    if request.form['text']:
        url = "http://localhost:8080/api/HomeTimeline"
        r = requests.post(url,auth=(session['username'],session['password']), json={'text':request.form['text']})
        if(r.status_code == 200):
            flash('Your message was recorded')
    return redirect(url_for('timeline'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Logs the user in."""
    if g.user:
        return redirect(url_for('timeline'))
    error = None
    if request.method == 'POST':
       url = "http://localhost:8080/api/userInfo/" + request.form['username']
       resp = requests.get(url = url)
       user = resp.json()
       if user is None:
           error = 'Invalid username'
       elif not check_password_hash(user['pw_hash'],
                                    request.form['password']):
           error = 'Invalid password'
       r = requests.post("http://localhost:8080/api/login", json={'username':request.form['username'],'password':request.form['password']})
       if(r.status_code == 200):
           flash('You were logged in')
           session['user_id'] = user['user_id']
           session['username'] = request.form['username']
           session['password'] = request.form['password']
           return redirect(url_for('timeline'))
    return render_template('login.html', error=error)


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Registers the user."""
    if g.user:
        return redirect(url_for('timeline'))
    error = None
    if request.method == 'POST':
        url = "http://localhost:8080/api/userInfo/" + request.form['username']
        resp = requests.get(url = url)
        user = resp.json()
        if not request.form['username']:
            error = 'You have to enter a username'
        elif not request.form['email'] or \
                '@' not in request.form['email']:
            error = 'You have to enter a valid email address'
        elif not request.form['password']:
            error = 'You have to enter a password'
        elif request.form['password'] != request.form['password2']:
            error = 'The two passwords do not match'
        elif resp.status_code == 200:
            error = 'The username is already taken'
        else:
            r = requests.post("http://localhost:8080/api/register", json={'username':request.form['username'],'password':request.form['password'],'email':request.form['email']})
            flash('You were successfully registered and can login now')
            return redirect(url_for('login'))
    return render_template('register.html', error=error)


@app.route('/logout')
def logout():
    """Logs the user out."""
    r = requests.get("http://localhost:8080/api/logout")
    if(r.status_code == 200):
        flash('You were logged out')
        session.pop('user_id', None)
        return redirect(url_for('public_timeline'))


# add some filters to jinja
app.jinja_env.filters['datetimeformat'] = format_datetime
app.jinja_env.filters['gravatar'] = gravatar_url
