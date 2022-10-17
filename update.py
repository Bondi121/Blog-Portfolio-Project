
@app.route('/update_user/<id>', methods=['PUT'])
def update_user(id):
    user_data = request.json
    firstname = user_data.get('firstname')
    lastname = user_data.get('lastname')
    email = user_data.get('email')
    user = User.query.filter_by(id=id).first()
    #https://flask-sqlalchemy.palletsprojects.com/en/2.x/queries/
    if firstname is not None:
        user.first_name = firstname
    if lastname is not None:
        user.last_name = lastname
    if email is not None:
        user.email = email
    
    db.session.commit()
    return "User update"



@app.route('/update_post/<id>', methods=['PUT'])
def update_post(id):
    post_data = request.json
    title = post_data.get('title')
    content = post_data.get('content')
    date_posted = post_data.get('date_posted')
    user_id = post_data.get('user_id')
    post = Post.query.filter_by(id=id).first()
    if title is not None:
        post.title = title
    if content is not None:
        post.content = content

    db.session.commit()
    return "Post update"