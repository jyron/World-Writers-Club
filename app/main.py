#routes not related to signup process

from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required, current_user
from . import db
from .models import User, Writing
main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('home.html', title = "Home")

@main.route('/profile')
@login_required
def profile():
    personals = Writing.query.filter_by(author=current_user.id)
    return render_template('profile.html', current=current_user,personals = personals, title = "Profile")


    


###Finally writing the page that accepts posts 
###Functionality needs to include:
###  Join a Prompt?
###  "Yes"
###  ...Prompt Loading...
###  Show Prompt
###  Get ready, timer starts in 3...2....1...
###  After 15 minutes input screen is locked, forms are either submitted or emptied. DONT FORCE THEM TO SUBMIT!!
###  Sending Post to User2
###  Receiving Post from User2
###  User1 submits writing, User2 submits writing
# From Users I will be able to search All Prompts
# From Posts I will search


