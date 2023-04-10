"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flask-blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "itsasecret!!!333#!!!333!!!!"

debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)
db.create_all()


@app.route('/', methods=["GET"])
def redirect_list_users():
    flash("Redirected to Users List!", "success")
    return redirect('/users')

@app.route('/users', methods=["GET"])
def list_users():
    """Return homepage, list all users."""
    users = User.query.all()
    first_name=""
    if request.args:
        first_name=request.args['first_name']
    return render_template('home.html', users=users, first_name=first_name )


@app.route('/users/new', methods=["POST", "GET"])
def get_new_user():
    """Create new user."""
    users = User.query.all()
    first_name=""
    last_name=""
    image_url=""
    new_user=""
    our_request = request.form
    if request.args:
        first_name=request.args['first_name']
    if request.method == 'POST':
        #if request.args:
        #    first_name=request.args['first_name']
        #    last_name=request.args['last_name']
        #    user_image=request.args['user_image']
        #    new_user = User(first_name=first_name, last_name=last_name, user_image=user_image)

        our_request = request.form
        first_name=our_request['first_name']
        last_name=our_request['last_name']
        if our_request['image_url']:
            image_url=our_request['image_url']
            new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
        else:
            new_user = User(first_name=first_name, last_name=last_name)
        db.session.add(new_user)
        db.session.commit()
        flash(f"You created {first_name}!", "success")
        return redirect('/users')
    return render_template('userlist.html', users=users, first_name=first_name, new_user=new_user, our_request=our_request, image_url=image_url)

@app.route('/users/<int:id>', methods=["GET", "POST"])
def list_specific_users(id):
    """Return user details page, based on user ID."""
    users = User.query.all()
    posts = Post.query.all()
    #import pdb; pdb.set_trace()
    specified_user = User.query.filter_by(id=id).all()
    first_name = specified_user[0].first_name
    last_name = specified_user[0].last_name
    image_url = specified_user[0].image_url

    title=""
    content=""
    thumbnail=""

    if request.method == 'POST':
        post = request.form
        title = post['title']
        content = post['content']
        thumbnail = post['image_url']
    
    
    
    return render_template('user_page.html', users=users, first_name=first_name, specified_user=specified_user, last_name = last_name, image_url=image_url, id=id, title=title, content=content, thumbnail=thumbnail, posts=posts)


@app.route('/delete-all', methods=["GET"])
def delete_all_users():
    """DELETE ALL USERS.."""
    usersquery = User.query.delete()
    db.session.commit()
    
    
    return render_template('userlist.html',)



@app.route('/delete/<int:id>', methods=["GET"])
def delete_specified_user(id):
    """Delete user, based on user ID."""
    specified_user = User.query.filter_by(id=id).all()
    first_name = specified_user[0].first_name
    last_name = specified_user[0].last_name
    image_url = specified_user[0].image_url
    
    specified_user_delete = User.query.filter_by(id=id).delete()


    db.session.commit()
    flash(f"You deleted {first_name} {last_name}!", "error")
    return redirect('/users')


@app.route('/delete/post/<int:id>', methods=["GET"])
def delete_specified_post(id):
    """Delete user, based on user ID."""
    specified_post = Post.query.filter_by(id=id).all()
    #first_name = specified_user[0].first_name
    #last_name = specified_user[0].last_name
    #image_url = specified_user[0].image_url
    
    specified_post_delete = Post.query.filter_by(id=id).delete()


    db.session.commit()
    flash(f"You deleted this post!", "error")
    return redirect('/users')
    
    
@app.route('/edit/<int:id>', methods=["GET", "POST"])
def edit_specified_user(id):
    """Edit user details, based on user ID."""
    specified_user = User.query.filter_by(id=id).all()
    
    if request.method == 'POST':
        
        specified_user = User.query.filter_by(id=id).all()
        our_request = request.form
        first_name=our_request['first_name']
        last_name=our_request['last_name']
        specified_user[0].first_name = first_name
        specified_user[0].last_name = last_name
        if our_request['image_url']:
            image_url=our_request['image_url']
            
        
        
        updated_user = specified_user[0]
        db.session.add(updated_user)
        db.session.commit()
        flash(f"You updated {first_name}!", "success")
        return redirect('/users')
    return render_template('user_edit.html', id=id, specified_user=specified_user)

@app.route('/posts/<int:id>/edit', methods=["GET", "POST"])
def edit_specified_post(id):
    """Edit POST details, based on POST ID."""
    specified_post = Post.query.filter_by(id=id).all()
    user_id = specified_post[0].user_id
    specified_user = User.query.filter_by(id=user_id).all()
    
    if request.method == 'POST':
        
        specified_post = Post.query.filter_by(id=id).all()
        our_request = request.form
        title=our_request['title']
        content=our_request['content']
        specified_post[0].title = title
        specified_post[0].content = content
        if our_request['image_url']:
            image_url=our_request['image_url']
            specified_post[0].image_url = image_url
        else:
            image_url = "https://99designs-blog.imgix.net/blog/wp-content/uploads/2018/11/attachment_78456430-e1541654366936.jpeg?auto=format&q=60&fit=max&w=930"
            specified_post[0].image_url = image_url
        
        
        updated_post = specified_post[0]
        db.session.add(updated_post)
        db.session.commit()
        flash(f"You updated your post!", "success")
        return redirect(f'/post/{updated_post.id}')
    return render_template('post_edit.html', id=id, specified_post=specified_post, specified_user=specified_user)




#Add Post Routes
#GET /users/[user-id]/posts/new
#Show form to add a post for that user.
#POST /users/[user-id]/posts/new
#Handle add form; add post and redirect to the user detail page.
#GET /posts/[post-id]
#Show a post.

#Show buttons to edit and delete the post.

#GET /posts/[post-id]/edit
#Show form to edit a post, and to cancel (back to user page).
#POST /posts/[post-id]/edit
#Handle editing of a post. Redirect back to the post view.
#POST /posts/[post-id]/delete
#Delete the post.
#Change the User Page
#Change the user page to show the posts for that user.

#Testing
#Update any broken tests and add more testing

#Celebrate!
#Yay! Congratulations on the first big two parts.




@app.route('/users/<int:id>/posts/new', methods=["GET", "POST"] )
def add_user_post(id):
    """NEED TO ACTUALLY ADD POST DATA TO POST MODEL AND COMMIT, THEN MAKE NEW PAGE WHERE POSTS ARE HOSTED. FORM DATA IS BEING CAPTURED."""
    specified_user = User.query.filter_by(id=id).all()
    title=""
    content=''
    thumbnail=''
    user_id=id
    if request.method == 'POST':
        post = request.form
        title = post['title']
        content = post['content']
        user_id = user_id
        
        if post['image_url']:
            thumbnail = post['image_url']
            new_post = Post(title=title, content=content, image_url=thumbnail, user_id=user_id)
        else:
            new_post = Post(title=title, content=content, user_id=user_id)
        
        db.session.add(new_post)
        db.session.commit()
        flash(f"New post created!", "success")
        return redirect('/users')
    return render_template('new_post.html', id=id, specified_user=specified_user, title=title, content=content, thumbnail=thumbnail)





@app.route('/post/<int:id>', methods=["GET"])
def show_post(id):
    """Return post details page, based on post ID."""
    #users = User.query.all()
    

    specified_post = Post.query.filter_by(id=id).all()
    title = specified_post[0].title
    content = specified_post[0].content
    created_at = specified_post[0].created_at
    image_url = specified_post[0].image_url
    user_id = specified_post[0].user_id
    
    specified_user = User.query.filter_by(id=user_id).all()
    
    #specified_user_delete = User.query.filter_by(id=id).delete()


    
    
    return render_template('post_page.html', title=title, content=content, created_at=created_at, image_url=image_url, specified_user=specified_user, user_id=user_id, specified_post=specified_post)
        