from flask import Flask

app = Flask(__name__)

@app.route('/homepage')
def home():
    return "Hello World"

#Users Endpoints

@app.route('/registration', methods=['POST'])
def register():
    return "Registration"


@app.route('/profile')
def user_profile():
    return "User Profile"


@app.route('/update_user', methods=['PUT'])
def update():
    return "User update"


@app.route('/delete_user', methods=['DELETE'])
def delete_user():
    return "Delete user"

#Posts Endpoints

@app.route('/create_post', methods=['POST'])
def user_post():
    return "User Post"


@app.route('/post/<id>')
def get_post():
    return "Post id"


@app.route('/delete_post', methods=['DELETE'])
def delete_post():
    return "Delete Post"


@app.route('/update_post', methods=['PUT'])
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
