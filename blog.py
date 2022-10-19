from datetime import datetime
from pickle import NONE
from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os 

app = Flask(__name__)
db = SQLAlchemy()
basedir = os.path.abspath(os.path.dirname('1800 Final Project Blog Post'))
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(basedir, 'blog.sqlite')

db.init_app(app)
#Create your Flask application object, load any config, and then initialize the SQLAlchemy extension class with the application by calling db.init_app. This example connects to a SQLite database, which is stored in the app’s instance folder.
#https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/quickstart/#installation

class User(db.Model):
    #Creating user table schema
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    username = db.Column(db.String, unique=True, nullable=False)
    address = db.Column(db.String, unique=True, nullable=True)
    email = db.Column(db.String, unique=True, nullable=False)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)

#Define Models 
#https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/quickstart/#define-models


#Creating tables   
#https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/quickstart/#create-the-tables     
with app.app_context():
    db.create_all()


@app.route('/homepage')
def home():
    user_blogs = Post.query.order_by(Post.id.desc()).all()
    return render_template("index.html",blogs=user_blogs)


#Users Endpoints

@app.route('/registration', methods=['POST', 'GET'])
def register():
    firstname = request.form.get('firstname')
    lastname = request.form.get('lastname')
    username = request.form.get('username')
    email = request.form.get('email')
    if request.method == 'POST':
        user = User(first_name = firstname, last_name = lastname, username = username, email = email)
        db.session.add(user) 
        db.session.commit()
        #https://flask-sqlalchemy.palletsprojects.com/en/2.x/queries/#inserting-records
    return render_template("register.html")

@app.route('/login', methods=['POST', 'GET'])
def login():
    username = request.form.get('username')
    if request.method == 'POST':
        user = User.query.filter_by(username=username).first()

        if user:
            return redirect(url_for('home'))
    return render_template('login.html')


@app.route('/profile/<id>', methods=['GET'])
def user_profile(id):
    user = User.query.filter_by(id=id).first()
    if user is None:
        return redirect(url_for('home'))
    return render_template("profile.html", user_details=user)


@app.route('/update_user/<id>', methods=['POST', 'GET'])
def update_user(id):
    firstname = request.form.get('firstname')
    lastname = request.form.get('lastname')
    email = request.form.get('email')
    address = request.form.get('address')
    user = User.query.filter_by(id=id).first()
    if user is None:
        return redirect(url_for('home'))
    #https://flask-sqlalchemy.palletsprojects.com/en/2.x/queries/
    if request.method == 'POST': 
        if firstname is not None:
            user.first_name = firstname
        if lastname is not None:
            user.last_name = lastname
        if address is not None:
            user.address = address
        if email is not None:
            user.email = email
        db.session.commit()
        return redirect (url_for('user_profile' , id=user.id))
    return render_template("user_update.html", user_details=user)
    


@app.route('/delete_user/<id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.filter_by(id=id).first()
    if user:
        db.session.delete(user)
        db.session.commit()
        return "User deleted"
    else:
        return "User not found"

#Posts Endpoints

@app.route('/create_post', methods=['POST', 'GET'])
def user_post():
    title = request.form.get('title')
    content = request.form.get('content')
    user_id = request.form.get('user_id')
    user = User.query.filter_by(id=user_id).first()
    if request.method == 'POST' and user is not None:
        post = Post(title=title, content=content, user_id=user_id)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('create_post.html')


@app.route('/post/<title>')
def get_post(title):
    post = Post.query.filter(Post.title.like(f'%{title}%')).order_by(Post.id.desc()).all()
    if post is None:
        return "no post is found"
    return render_template('get_post.html', post_details=post)
    
#https://docs.sqlalchemy.org/en/14/orm/quickstart.html
#https://devsheet.com/code-snippet/like-query-sqlalchemy/

@app.route('/delete_post/<id>', methods=['DELETE'])
def delete_post(id):
    post = Post.query.filter_by(id=id).first()
    if post:
        db.session.delete(post)
        db.session.commit()
        return "Post deleted"
    else:
        return "Post not found"
   


@app.route('/update_post/<id>', methods=['PUT'])
def update_post(id):
    title = request.form.get('title')
    content = request.form.get('content')
    date_posted = request.form.get('date_posted')
    user_id = request.form.get('user_id')
    post = Post.query.filter_by(id=id).first()
    if title is not None:
        post.title = title
    if content is not None:
        post.content = content

    db.session.commit()
    return "Post Update"



#python -m venv venv
#venv\Scripts\activate
#pip install Flask

#set FLASK_APP=blog.py
#set FLASK_DEBUG=True
#flask run

#Ability to post / Ability to edit

#Ability to like a post

#logout

#ability to comment

#Pagination

#Local Storage

