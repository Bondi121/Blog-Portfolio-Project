from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import os 

app = Flask(__name__)
db = SQLAlchemy()
basedir = os.path.abspath(os.path.dirname('1800 Final Project Blog Post'))
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(basedir, 'blog.sqlite')
print(basedir)

db.init_app(app)

class User(db.Model):
    #Creating user table schema
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    username = db.Column(db.String, unique=True, nullable=False)
    address = db.Column(db.String, unique=True, nullable=True)
    email = db.Column(db.String, unique=True, nullable=False)


#Creating tables        
with app.app_context():
    db.create_all()


@app.route('/homepage')
def home():
    return "Hello World"

#Users Endpoints

@app.route('/registration', methods=['POST'])
def register():
    user_data = request.json
    firstname = user_data.get('firstname')
    lastname = user_data.get('lastname')
    username = user_data.get('username')
    email = user_data.get('email')
    if request.method == 'POST':
        user = User(first_name = firstname, last_name = lastname, username = username, email = email)
        db.session.add(user) 
        db.session.commit()
    return "Registration"


@app.route('/profile/<id>', methods=['GET'])
def user_profile(id):
    user = User.query.filter_by(id=id).first()
    if user is None:
        return "no user found"
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

