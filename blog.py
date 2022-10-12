from flask import Flask

app = Flask(__name__)

@app.route('/homepage')
def home():
    return "Hello World"


@app.route('/registration')
def register():
    return "Registration"


@app.route('/profile')
def user_profile():
    return "User Profile"


@app.route('/post')
def user_post():
    return "User Post"


@app.route('/post/<id>')
def get_post():
    return "Post id"


@app.route('/delete_post')
def delete_post():
    return "Delete Post"


@app.route('/update_post')
def update_post():
    return "Update Post"




#set FLASK_APP=blog.py
#set FLASK_DEBUG=True
#flask run

#Ability to post / Ability to edit

#Ability to like a post

#logout

#ability to comment

#Pagination

#Local Storage
