from flask import render_template, redirect, url_for, flash, request, session
from flask_login import login_required, current_user
from . import auth
from .email import send_email
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

            allergies = request.form['allergies']
            if allergies != "":
                allergies = allergies.split(" ")
                for allergy in allergies:
                    # Add allergy to allergy table
                    query_change(
                        query="INSERT INTO allergy (allergy_name) VALUES (?)",
                        key=(allergy,)
                    )
                    # Select allergy id that was just inserted
                    allergy_id = query_select(
                        query="SELECT allergy_id FROM allergy ORDER BY allergy_id DESC LIMIT (?)",
                        key=1
                    )[0][0]
                    # Add both patient and allergy id to linking table
                    query_change(
                        query="INSERT INTO patient_allergy (patient_id, allergy_id) VALUES (?, ?)",
                        key=[patient_id, allergy_id]
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
            flash("A confirmation email has been sent.")
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