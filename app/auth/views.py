from flask import render_template, redirect, url_for, flash, request, session
from flask_login import login_required, current_user, login_user
from . import auth
from .email import send_email
from .forms import *
from .security import Security, User
from ..db.database_queries import query_select, query_change
from datetime import datetime
from .. import login_manager


# Adapted from Flask Web Development: Developing Web Applications with Python 2nd Edition,  978-1491991732
@auth.route('/login', methods=["GET", "POST"])
def login():
    """Login user if they are registered"""
    login_form = LoginForm()

    if login_form.validate_on_submit():
        email = login_form.email.data.lower()
        password = login_form.password.data

        # Retrieve user object to verify if email and password are correct
        registered_user = query_select(
            query="SELECT * FROM user WHERE email = (?)",
            key=email
        )

        if registered_user:
            user = load_user(registered_user[0][0])
            if user.email == email and Security().verify_password(user.password_hash, password):
                login_user(user)
                session['user_id'] = user.get_id()
                return redirect(url_for('profile.profile_main'))
            else:
                flash('Invalid password')
        else:
            flash('Invalid email')

    return render_template('login.html', form=login_form)


@auth.route('/register', methods=["GET", "POST"])
def register():
    registration_form = RegistrationForm()

    if registration_form.validate_on_submit():
        email = registration_form.email.data.lower()

        # Check for duplicate email
        duplicate_email = query_select(
            query="SELECT * FROM user WHERE email = (?)",
            key=email
        )

        if duplicate_email:
            flash("Email already registered")
        else:
            # Generate password hash
            password_hash = Security().generate_password_hash(registration_form.password.data)

            # Insert new user into the user table
            query_change(
                query="INSERT INTO user (email, password) VALUES (?, ?)",
                key=[email, password_hash]
            )

            # Select user_id of the new user
            user_id = query_select(
                query="SELECT user_id FROM user WHERE email = (?)",
                key=email
            )[0][0]

            # Process date of birth and allergies
            dob = datetime.strptime(request.form['dob'], '%Y-%m-%d').date()
            dob = datetime.strftime(dob, "%m-%d-%Y")

            # Insert new patient into the patient_table
            query_change(
                query="INSERT INTO patient (fname, lname, mname, dob, weight, user_id) VALUES (?, ?, ?, ?, ?, ?)",
                key=[request.form['fname'],
                     request.form['lname'],
                     request.form['minitial'],
                     dob,
                     request.form['weight'],
                     user_id]
            )

            # Select patient_id of the new user
            patient_id = query_select(
                query="SELECT patient_id FROM patient WHERE user_id = (?)",
                key=user_id)[0][0]

            # Add allergy to patient_allergy table
            allergies = request.form['allergies']
            if allergies != "":
                allergies = allergies.split(",")
                for allergy in allergies:
                    query_change(
                        query="INSERT OR IGNORE INTO  patient_allergy (patient_id, allergy) VALUES (?, ?)",
                        key=[patient_id, allergy]
                    )

            # Add user and patient ids to the session
            session['user_id'] = user_id
            session['patient_id'] = patient_id

            # Generate token, used to verify email address
            token = Security().generate_configuration_token(user_id)
            send_email(email,
                       "Confirm Your Account",
                       "confirm_registration.html",
                       token=token)
            flash("A confirmation email has been sent")
        return redirect(url_for("auth.register"))

    return render_template("register.html", form=registration_form)


@auth.route('/confirm_registration/<token>')
@login_required
def confirm_registration(token):
    """Confirm token in confirmation email"""
    if current_user.confirmed:
        return redirect(url_for('profile.profile_main'))

    if Security().confirm(current_user.id, token):
        query_change(
            query="UPDATE user SET confirmed = (?) WHERE user_id = (?)",
            key=[1, session["user_id"]]
        )
        flash('You have confirmed your account.')
    else:
        flash('The confirmation link is invalid or has expired.')

    return redirect(url_for('main.index'))


@login_manager.user_loader
def load_user(user_id):
    """Reload the user object from the user ID stored in the session"""

    result = query_select(
        query="SELECT * FROM user WHERE user_id = (?)",
        key=user_id
    )

    if result is None:
        return False
    else:
        return User(int(result[0][0]), result[0][1], result[0][2], result[0][3])