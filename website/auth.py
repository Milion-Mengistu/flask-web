from flask import Blueprint, flash, redirect , render_template , request, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from website.models import User 
auth = Blueprint('auth', __name__)
from website import db
from flask_login import login_user,logout_user,current_user,login_required 


@auth.route('/login', methods=['GET', 'POST'])
def login():
  
  
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Find user by email
        user = User.query.filter_by(email=email).first()
    
        print (user)
        # Validation checks
       
        if user:
            # Check if password matches the hashed password
            if check_password_hash(user.password_hash, password):
                # Log in the user
                flash('Login successful!', 'success')
                login_user(user,remember=True)  # Log in the user
                return redirect(url_for('views.home'))  # Redirect to some dashboard page
            else:
                flash('Incorrect password!', 'danger')
         # Redirect to some dashboard page
    
    return render_template('login.html',user=current_user)



@auth.route('/logout')
@login_required
def logout():
    
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/signup',methods=['GET' , 'POST'])
def signup():
    if request.method == 'POST':
        # Get form data
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        # Validation checks
        user = User.query.filter_by(email=email).first()
       
        if user:
            flash('Email already registered!', 'danger')
        if not name or not email or not password or not confirm_password:
            flash('All fields are required!', 'danger')
        # elif email_exists(email):
            # flash('Email already registered!', 'danger')
        elif password != confirm_password:
            flash('Passwords do not match!', 'danger')
        elif len(password) < 6:
            flash('Password must be at least 6 characters long!', 'danger')
        else:
            # Hash the password before storing it
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256:600000')
            
            # Add user to the "database"
            new_user = User( username = name,email = email, password_hash = hashed_password)
            db.session.add(new_user)
            db.session.commit()

            flash('Account created successfully! ', 'success')
            # Assuming you have a login page
            return redirect(url_for('views.home'))

    return render_template('sign-up.html',user = current_user)

