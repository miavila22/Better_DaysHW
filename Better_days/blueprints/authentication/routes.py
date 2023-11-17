#External Imports
import site
from flask import Blueprint, render_template, request, redirect, flash
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user

#Internal Imports
from Better_days.models import User, db
from Better_days.forms import RegisterForm, LoginForm

authentication = Blueprint('authentication', __name__, template_folder='authentication_templates')

@authentication.route('/signup', methods=['GET', 'POST'])
def signup():
    registerform = RegisterForm()

    if request.method == 'POST' and registerform.validate_on_submit():
        #now we need to grab the data that was submitted
        first_name = registerform.first_name.data
        last_name = registerform.last_name.data
        username = registerform.username.data
        email = registerform.email.data
        password = registerform.password.data

        print(email, password, username)


        if User.query.filter(User.username == username).first():
            flash(f"That Username already exist! Please Try Again", category='warning')
            return redirect('/signup')
        if User.query.filter(User.email == email).first():
            flash("That email already exist! Please Try Again", category='warning')
            return redirect('/signup')
        
        user = User(username, email, password, first_name, last_name)
        print(user)
        #adding objects to our database
        db.session.add(user) # almost like "git add ."
        db.session.commit() # almost like "git commit"

        flash(f'{username} has been registered!', category='success')
        return redirect('/signin')
    
    return render_template('sign_up.html', form=registerform)

@authentication.route('/signin', methods=['GET', 'POST'])
def signin():
    loginform = LoginForm()

    if request.method == 'POST' and loginform.validate_on_submit():
        email = loginform.email.data
        password = loginform.password.data
        print("login info", email, password)

        user = User.query.filter(User.email == email).first()

        if user and check_password_hash(user.password, password):
            login_user(user) #this is saved as current_user everywhere in our application
            flash(f'{email} successfully logged in!', category='success')
            return redirect('/')
           
        else:
            flash(f'Invalid Email or Password! Please Try Again', category='warning')
            return redirect('/signin')
        
    return render_template('sign_in.html', form=loginform)

#logout

@authentication.route('/logout')
def logout():
    logout_user()
    return redirect('/')

