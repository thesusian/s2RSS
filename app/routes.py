from flask import render_template, flash, redirect, url_for, request, Response, jsonify
from flask_login import current_user, login_user, logout_user, login_required
import requests
from app.searcher import get_foramtted_list
from app import app, db
from app.models import User, Feed
from app.forms import LoginForm, RegistrationForm, LoadSourceForm, SearchPatternForm
from werkzeug.urls import url_parse

@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', title='Home', feeds=Feed.query.filter_by(owner=current_user))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        # check password
        user = User.query.filter_by(username=form.username.data.lower()).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user)
        # redirect user to the page they were on, but first check if the redirect
        # is to a url, if not it can proceed
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Log In', form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('index')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # lower-case username, for consistency
        user = User(username=form.username.data.lower())
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/create-feed', methods=['GET', 'POST'])
@login_required
def create_feed():
    feed = Feed()
    return render_template('create-feed.html', title='Create Feed')

@app.route('/fetch-source', methods=['POST'])
@login_required
def fetch_source():
    address = request.json['address']
    try:
        response = requests.get(address)
        source_code = response.text
    except Exception as e:
        source_code = f"Error: {str(e)}"
        # FIX , users shouldn't be seeing error messages        
    return jsonify({'source_code': source_code})

@app.route('/fetch-pattern-result', methods=['POST'])
@login_required
def search_pattern_form():
    pattern = request.json['pattern']
    source_code = request.json['source_code']
    pattern_result = get_foramtted_list(source_code, pattern)
    return jsonify({'pattern_result': pattern_result})

@app.route('/feed/<id>.xml')
def get_feed(id):
    feed = Feed.query.filter_by(id=id).first_or_404()
    return Response(feed.gen_xml(), mimetype='text/xml')
