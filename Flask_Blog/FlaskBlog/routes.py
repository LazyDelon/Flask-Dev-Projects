import os
import secrets

from PIL import Image

from flask import flash
from flask import url_for
from flask import request
from flask import redirect
from flask import render_template

from FlaskBlog.forms import LoginForm
from FlaskBlog.forms import RegisterationForm
from FlaskBlog.forms import UpdateAccountForm

from FlaskBlog import db
from FlaskBlog import app
from FlaskBlog import bcrypt

from flask_login import login_user
from flask_login import logout_user
from flask_login import current_user
from flask_login import login_required

from FlaskBlog.models import User, Post


posts = [
    {
        'author'       :  'LazyDelon'            ,
        'title'        :  'Blog Post 1'          ,
        'content'      :  'First Post Content'   ,
        'date_posted'  :  'February 11, 2001'
    }
    ,
    {
        'author'       :  'Jane Doe'             ,
        'title'        :  'Blog Post 2'          ,
        'content'      :  'Second Post Content'  ,
        'date_posted'  :  'April 21, 2023'
    }
]






@app.route("/")

def home():

    return render_template('home.html', posts=posts)



# ______________________________________

@app.route("/about")

def about():

    return render_template('about.html', title='About')


# ______________________________________

@app.route("/register", methods=['GET', 'POST'])

def register():

    if current_user.is_authenticated:
        return redirect( url_for('home') )

    form = RegisterationForm()

    if form.validate_on_submit():

        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        
        db.session.add(user)
        db.session.commit()

        flash('Your account has been created! You are now able to log in', 'success')
        return redirect( url_for('login') )

    return render_template('register.html', title='Register', form=form)



# ______________________________________

@app.route("/login", methods=['GET', 'POST'])

def login():

    if current_user.is_authenticated:
        return redirect( url_for('home') )  

    form = LoginForm()

    if form.validate_on_submit():
        
        user = User.query.filter_by(email=form.email.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect( url_for('home') )
        else:
            flash('Login Unsuccessful. Please Check Email and Password', 'danger')
    return render_template('login.html', title='Login', form=form)


# ______________________________________

@app.route("/logout")

def logout():

    logout_user()

    return redirect( url_for('home') )




# ______________________________________

def save_picture(form_picture):

    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)

    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    picture_image = Image.open(form_picture)
    picture_image.thumbnail(output_size)

    picture_image.save(picture_path)

    return picture_fn


# ______________________________________

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():

    form = UpdateAccountForm()

    if form.validate_on_submit():

        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        
        current_user.username = form.username.data
        current_user.email = form.email.data

        db.session.commit()

        flash('Your account has been updated!', 'success')
        return redirect( url_for('account') )
    
    elif request.method == 'GET':

        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)