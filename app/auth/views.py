from flask import render_template, redirect, url_for, flash, request, session
from . import auth
from .forms import *
from .security import Security
from ..db.database_queries import query_select, query_change
from datetime import datetime


# Adapted from Flask Web Development: Developing Web Applications with Python 2nd Edition,  978-1491991732
@auth.route('/register', methods=["GET", "POST"])
def register():
    registration_form = RegistrationForm()

    if registration_form.validate_on_submit():
        email = registration_form.email.data.lower()
        duplicate_email = query_select(
            query="SELECT * FROM user WHERE email = (?)",
            key=email
        )
        print(duplicate_email)
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
            )

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
                key=user_id
            )

            # Add user and patient ids to the session
            session['user_id'] = user_id
            session['patient_id'] = patient_id






    """    
    Take user input
    Check if there is a duplicate email
        If duplicate - flash error  message
        Else - insert new user into db, 
                select user after being inserted, 
                generate token for verification
                send confirmation email
    """

    return render_template("register.html", form=registration_form)