from flask import flash
from flask import url_for
from flask import redirect
from flask import render_template

from Example.forms import LoginForm
from Example.forms import RegisterationForm

from Example import app

from Example.models import User, Post


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

    form = RegisterationForm()

    if form.validate_on_submit():

        flash(f'Account Created For { form.username.data }!', 'success')
        return redirect( url_for('home') )

    return render_template('register.html', title='Register', form=form)



# ______________________________________

@app.route("/login", methods=['GET', 'POST'])

def login():

    form = LoginForm()

    if form.validate_on_submit():
        
        if form.email.data == 'Snorlaxy.0211@gmail.com' and form.password.data =='password':

            flash('You have been logged in!', 'success')
            return redirect( url_for('home') )
        else:
            flash('Login Unsuccessful. Please Check Username and Password', 'danger')
    return render_template('login.html', title='Login', form=form)

