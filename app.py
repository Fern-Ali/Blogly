"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

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
    """Return homepage, list all users."""
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

@app.route('/users/<int:id>', methods=["GET"])
def list_specific_users(id):
    """Return user details page, based on user ID."""
    users = User.query.all()
    specified_user = User.query.filter_by(id=id).all()
    first_name = specified_user[0].first_name
    last_name = specified_user[0].last_name
    image_url = specified_user[0].image_url
    
    
    
    return render_template('user_page.html', users=users, first_name=first_name, specified_user=specified_user, last_name = last_name, image_url=image_url, id=id)


@app.route('/delete-all', methods=["GET"])
def delete_all_users():
    """Return user details page, based on user ID."""
    usersquery = User.query.delete()
    db.session.commit()
    
    
    return render_template('userlist.html',)



@app.route('/delete/<int:id>', methods=["GET"])
def delete_specified_user(id):
    """Return user details page, based on user ID."""
    specified_user = User.query.filter_by(id=id).all()
    first_name = specified_user[0].first_name
    last_name = specified_user[0].last_name
    image_url = specified_user[0].image_url
    
    specified_user_delete = User.query.filter_by(id=id).delete()


    db.session.commit()
    flash(f"You deleted {first_name} {last_name}!", "error")
    return redirect('/users')
    
    
@app.route('/edit/<int:id>', methods=["GET", "POST"])
def edit_specified_user(id):


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
    return render_template('user_edit.html', id=id)