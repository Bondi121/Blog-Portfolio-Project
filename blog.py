from datetime import datetime
from flask import Flask, request, render_template, redirect, url_for, jsonify
# importing SQLAlchemy for communicating with postgreSQL
from flask_sqlalchemy import SQLAlchemy
import os
from flask_moment import Moment  # For displaying date and time on the frontend
# for allowing our backend to communicate effectively with backend without blocking it.
from flask_cors import CORS

app = Flask(__name__)  # creating a Flask instance
# register the http://127.0.0.1:5000 so that our backend will not block the request from fetch
CORS(app,  origins=["http://127.0.0.1:5000"])

db = SQLAlchemy()  # create an nstance of sqlalchemy

# getting the base directory of the project
basedir = os.path.abspath(os.path.dirname('1800 Final Project Blog Post'))
# configuring the SQLAlchemy to communicate with the database
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + \
    os.path.join(basedir, 'blog.sqlite')

moment = Moment(app)  # Registering the blueprint with Flask
db.init_app(app)  # Registering the bleuprint with Flask

# Create your Flask application object, load any config, and then initialize the SQLAlchemy extension class with the application by calling db.init_app. This example connects to a SQLite database, which is stored in the app’s instance folder.
# https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/quickstart/#installation


def get_file():
    # class used for form submission
    html_file = open("user_no_address.txt")
    content = html_file.read()
    html_file.close()
    return content


def write_note(text):
    # function for write to file
    file = open("user_no_address.txt", "a")
    file.write("----\n")
    file.write(f"<p> {text}</p>" + "\n")
    file.close()


class User(db.Model):
    """The below class User is model for creating a table on the database blog.sqlite"""
    # Creating user table schema
    # id column on the table in the database
    id = db.Column(db.Integer, primary_key=True)
    # first_name column in the table in the database
    first_name = db.Column(db.String, nullable=False)
    # last_name column in the table in the database
    last_name = db.Column(db.String, nullable=False)
    # username column in the table in the database
    username = db.Column(db.String, nullable=False, unique=True)
    # address column in the table in the database
    address = db.Column(db.String, nullable=True)
    # email column in the table in the database
    email = db.Column(db.String, nullable=False, unique=True)

    def user_details(self):
        """This collect the user information and store in a dictionary and save to user_information variable, and later return from the method"""
        user_information = {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "username": self.username,
            "address": self.address,
            "email": self.email,
        }
        return user_information

    def is_address(self):
        """This check if the address is given or not, if give return false, and if not, return true """
        if self.address:
            return False
        else:
            return True


class Post(db.Model):
    """The below class User is model for creating a table on the database blog.sqlite"""
    id = db.Column(
        db.Integer, primary_key=True)  # id column in the table in the database
    # title column in the table in the database
    title = db.Column(db.String, nullable=False)
    # content column in the table in the database
    content = db.Column(db.String, nullable=False)
    # datetime  column in the table in the database
    date_posted = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)

# Define Models
# https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/quickstart/#define-models


# Creating tables
# https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/quickstart/#create-the-tables
with app.app_context():  # This is a context manager that manage the opening and closing of the application context
    # This part will actually create all tables i.e both user and post inside the blog.sqlite in the project if it is not created, otherwise, it will ignore it.
    db.create_all()


@app.route('/homepage')  # homepage route
@app.route('/')
def home():
    # This will query all the post in the database blog.sqlite and save the result in the user_blog as a list
    user_blogs = Post.query.order_by(Post.id.desc()).all()
    # render_template take two arguments, the index.html file, and the user_blogs save to blogs  and pass to the template for rendering
    return render_template("index.html", blogs=user_blogs)


# Users Endpoints

# Registration route for creating a user
@app.route('/registration', methods=['POST', 'GET'])
def register():
    # on GET request, it will be None, and on POST request, it will get the firstname data
    firstname = request.form.get('firstname')
    # on GET request, it will be None, and on POST request, it will get the lastname data
    lastname = request.form.get('lastname')
    # on GET request, it will be None, and on POST request, it will get the username data
    username = request.form.get('username')
    # on GET request, it will be None, and on POST request, it will get the email data
    email = request.form.get('email')
    # on GET request, it will be None, and on POST request, it will get the address data
    address = request.form.get('address')
    if request.method == 'POST':  # this will only run if the requet.method is a POST request

        # check if the any user in the database is using either the email or username
        is_user_available = User.query.filter_by(
            username=username).first() or User.query.filter_by(email=email).first()

        # if is_user_available is found in the database, return the user_status page on the browser.
        if is_user_available:
            status = f'User already exists'
            return render_template("user_status.html", user_status=status)

        # if the condition above is false i.e the if conditionin line 109 is false, register the user into the database
        user = User(first_name=firstname, last_name=lastname,
                    username=username, email=email, address=address)

        # add user to sqlalchey session, at this point, the user is not yet save to database
        db.session.add(user)
        db.session.commit()  # the part that actually save the user to the database

        # if user register without address, save the user to a file
        if user.is_address():
            write_note(user.username)

        return redirect(url_for('login'))
        # https://flask-sqlalchemy.palletsprojects.com/en/2.x/queries/#inserting-records
    # displaying the registration page
    return render_template("register.html"), 201


@app.route('/login', methods=['POST', 'GET'])  # The login route
def login():
    # on GET request, it will be None, and on POST request, it will get the firstname data
    username = request.form.get('username')
    if request.method == 'POST':  # this will only run if the requet.method is a POST request
        # check if the user is in the database, if found, return the result to user, otherwise, return None
        user = User.query.filter_by(username=username).first()
        if user:  # if there is a user, it will redrect the user to homepage
            # the "home" is the function in line 88
            return redirect(url_for('home'))

        if user is None:  # if user is None, that is , not found in the database, show the user User not found
            status = f'User not found.'
            # This part render the user_status.html and pass the status to the render_template
            return render_template("user_status.html", user_status=status)
    return render_template('login.html')  # display the login page


app.route('/not_found')  # route for telling a user if the user is not register


def user_not_found():
    status = f'User not found.'
    # displaying the status of the user
    return render_template("user_status.html", user_status=status)


# the profile route with dynamic part called username accepting only GET request method
@app.route('/profile/<username>', methods=['GET'])
def user_profile(username):  # pass the dynamic part to the function
    # search if the user is present in the database using the dynamic part which is the username, if found, return the user and save to the user variable, else return None and save to the user variable.
    user = User.query.filter_by(username=username).first()
    if user:  # This will only run if the user is found.
        # get all the post of that same user, using the user.id to serach for his post on the post table.
        posts = Post.query.filter_by(user_id=user.id).all()
    if user is None:  # If the user in line 150 is None, then render the user_status.html with a status of User not found.
        status = f'User not found.'
        return render_template("user_status.html", user_status=status)

    # This part display the user profile and the user data with the post. The user_details=user.user_details() means pass the user details to the template, and blogs=posts is the post of a particular user being sent to the template.
    return render_template("profile.html", user_details=user.user_details(), blogs=posts)


# This route is used to check if a user is in our database or not using the dynamic part which is the username
@app.route('/check_user/<username>', methods=['GET'])
def check_user(username):
    # pass the username to the sqlalchemy code to get the user. if found, return the user, otherwise return None
    user = User.query.filter_by(username=username).first()
    # if user:
    #  posts = Post.query.filter_by(user_id=user.id).all()
    # if user is None, return {"status": "No user found"}, 404
    if user is None:
        return {"status": "No user found"}, 404
    # if user is found, return this line of code
    return {"status": "User found"}, 200


# route for updating existing user, and it accept GET and POST method.
@app.route('/update_user/<username>', methods=['POST', 'GET'])
def update_user(username):
    # on GET request, it will be None, and on POST request, it will get the firstname data
    firstname = request.form.get('firstname')
    # on GET request, it will be None, and on POST request, it will get the lastname data
    lastname = request.form.get('lastname')
    # on GET request, it will be None, and on POST request, it will get the email data
    email = request.form.get('email')
    # on GET request, it will be None, and on POST request, it will get the address data
    address = request.form.get('address')

    # search if the user is present in the database using the dynamic part which is the username, if found, return the user and save to the user variable, else return None and save to the user variable.
    user = User.query.filter_by(username=username).first()

    # if user is not found, return the user_status.html page showing user the information error
    if user is None:
        status = f'User not found.'
        return render_template("user_status.html", user_status=status)

    # https://flask-sqlalchemy.palletsprojects.com/en/2.x/queries/
    if request.method == 'POST':
        if firstname is not None:  # if firstname in line 172 in not None, update user.first_name of the user
            user.first_name = firstname  # updating first_name
        if lastname is not None:  # if lastname in line 173 in not None, update user.last_name of the user
            user.last_name = lastname
        if address is not None:  # if address in line 175 in not None, update user.address of the user
            user.address = address
        if email is not None:  # if email in line 172 in not None, update user.email of the user
            user.email = email

        db.session.commit()  # Whenever changes is made to the user, always save to database

        # after update the user, redirect to profile page
        return redirect(url_for('user_profile', username=user.username))

    # display the user_update.html
    return render_template("user_update.html", user_details=user),


# route for deleting a register user
@app.route('/delete_user/<username>', methods=['GET'])
def delete_user(username):
    # search if the user is present in the database using the dynamic part which is the username, if found, return the user and save to the user variable, else return None and save to the user variable.
    user = User.query.filter_by(username=username).first()
    if user:  # if user is present, the code in the if condition is run
        # delete all the post of the user to be deleted.
        posts = Post.query.filter(Post.user_id == user.id).delete()
        db.session.delete(user)  # add user to be deleted to session
        db.session.commit()  # finally delete the user
        # send a message to the user informing them the account is deleted
        status = f'User {user.username} deleted'
        # render the user_status.html with the status message
        return render_template("user_status.html", user_status=status)
    else:  # if the user is None , render the below code
        status = "User not found"
        return render_template('user_status.html', user_status=status)


# Posts Endpoints

# route for creating post, and it accept GET and POST method.
@app.route('/create_post', methods=['POST', 'GET'])
def user_post():
    # on GET request, it will be None, and on POST request, it will get the title data
    title = request.form.get('title')
    # on GET request, it will be None, and on POST request, it will get the content data
    content = request.form.get('content')
    # on GET request, it will be None, and on POST request, it will get the username data
    username = request.form.get('username')

    # check if the user is in our database by passing the username in line 222 which is sent from the backend to the sqlalchey part to search for the user, if found, it will return the user, otherwise, return None
    user = User.query.filter_by(username=username).first()
    # print(user)

    # if request.method is POST and the user in line 224 if found, run the block of code in the if statement
    if request.method == 'POST' and user is not None:

        if not user:
            status = "User not found"
            return render_template('user_status.html', user_status=status)

        # create the post with the id of the user that created the post
        post = Post(title=title, content=content, user_id=user.id)
        db.session.add(post)  # add the created post to session
        db.session.commit()  # finally save the post to the database inside the post table
        # return us back to the homepage after saving the post to database. The home in redirect(url_for('home')) is the function name in line 88
        return redirect(url_for('home'))
    # display the create_post.html when the browser first load the page on GET request
    return render_template('create_post.html')


# route for getting a particular post with the title
@app.route('/post/<title>')
def get_post(title):
    # this line of code will get all the post that has a specific word title in the title, if found, it will return the result as a list and save to post, otherwise, it will return None
    post = Post.query.filter(Post.title.like(
        f'%{title}%')).order_by(Post.id.desc()).all()
    print(post)
    if post is None:  # if the post variable in line 242 is None, run the if block code
        status = f'Post not found'
        # return the post status and pass the status to the template
        return render_template("post_status.html", user_status=status)
    # if the post in line 242 is found, render the get_post.html template
    return render_template('get_post.html', post_details=post)

# https://docs.sqlalchemy.org/en/14/orm/quickstart.html
# https://devsheet.com/code-snippet/like-query-sqlalchemy/


# route for searching a particular post with the form
@app.route('/search_post', methods=['POST', 'GET'])
def search_post():
    # it will get the title from the form submit for searching a post
    title = request.form.get('title')
    # this line of code will get all the post that has a specific word title in the title, if found, it will return the result as a list and save to post, otherwise, it will return None
    post = Post.query.filter(Post.title.like(
        f'%{title}%')).order_by(Post.id.desc()).all()
    if not post:  # if the post variable in line 242 is None, run the if block code
        status = f'Post not found'
        # return the post status and pass the status to the template
        return render_template("post_status.html", user_status=status)
    # if the post in line 242 is found, render the get_post.html template
    return render_template('get_post.html', post_details=post)


# this route uses two dynamic variables, id and user_id
@app.route('/delete_post/<id>/<user_id>', methods=['GET'])
def delete_post(id, user_id):
    # search if the post is present in the database using the dynamic part which is the id, if found, return the post and save to the post variable, else return None and save to the post variable.
    post = Post.query.filter_by(id=id).first()
    # search if the user is present in the database using the dynamic part which is the username, if found, return the user and save to the user variable, else return None and save to the user variable.
    user = User.query.filter_by(id=user_id).first()
    # check if the post is available, and also if post.user_id == user.id, if those conditions are true, run the code tin the if condition.
    if post and post.user_id == user.id:
        db.session.delete(post)  # add the created post to session
        db.session.commit()  # finally save the post to the database inside the post table
        # after deleting the post, redirect the user to the homepage
        return redirect(url_for('home'))
    else:  # if the condition is false, run the below code
        status = f'Post not found'
        return render_template("post_status.html", user_status=status)


# route for updating a post
@app.route('/update_post/<id>', methods=['POST', 'GET'])
def update_post(id):
    # on GET request, it will be None, and on POST request, it will get the title data
    title = request.form.get('title')
    # on GET request, it will be None, and on POST request, it will get the content data
    content = request.form.get('content')
    # search if the post is present in the database using the dynamic part which is the id, if found, return the post and save to the post variable, else return None and save to the post variable.
    post = Post.query.filter_by(id=id).first()
    if post is None:  # if the post is None, redirect the user to home
        return redirect(url_for('home'))
    if request.method == 'POST':  # if the request.method is a POST, update the post and save it to database
        if title is not None:
            post.title = title
        if content is not None:
            post.content = content
        db.session.commit()
        # after updating the post, redirect to the get_post route with the title
        return redirect(url_for('get_post', title=post.title))
    # display the create_post.html when the browser first load the page on GET request
    return render_template("post_update.html", post_details=post)


# python -m venv venv
# venv\Scripts\activate
# pip install Flask

# set FLASK_APP=blog.py
# set FLASK_DEBUG=True
# flask run
