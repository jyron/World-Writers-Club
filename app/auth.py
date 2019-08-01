from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, Writing
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from random import choice as rand
from .prompts import promptlist



auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html', title = "Login")

@auth.route('/login', methods=['POST'])
def login_post():
    #login code here
    email = request.form.get('email').lower()
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False
    
    user = User.query.filter_by(email=email).first()

    if not user: 
        flash('We dont have that email, Try again.', 'danger')
        return redirect(url_for('auth.login'))
    
    elif not check_password_hash(user.password, password):
        flash('Wrong password, Try again', 'danger')
        return redirect(url_for('auth.login'))
    
    login_user(user, remember=remember)
    flash('{} successfully logged in!'.format(user.email))
    return redirect(url_for('main.profile'))


    

@auth.route('/signup')
def signup():
    return render_template('signup.html', title = "Sign Up")

@auth.route('/signup', methods=['POST'])
def signup_post():

    email = request.form.get('email').lower()
    name = request.form.get('name').capitalize()
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again  
        flash("Email address already exists")
        return redirect(url_for('auth.signup'))

    # create new user with the form data. Hash the password so plaintext version isn't saved.
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

    db.session.add(new_user)
    db.session.commit()


    flash("Account created for {}!".format(email), 'success')
    return redirect(url_for('auth.login'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))




@auth.route('/prompt', methods=['GET'])
@login_required
def prompt_page():
    randomprompt = rand(promptlist)
    return render_template('prompt.html', prompt=randomprompt)
    

@auth.route('/prompt', methods=['POST'])
@login_required
def prompt_post():
    randomprompt = rand(promptlist)
    text = request.form.get('text')
    title = request.form.get('title')    
    author = current_user.id
    new_writing = Writing(text=text, title=title, prompt=randomprompt, author=author)
    db.session.add(new_writing)
    db.session.commit()
    flash('Thanks for submitting!')
    return redirect(url_for('main.profile'))
    



    


