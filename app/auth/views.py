from flask import render_template, redirect, url_for, flash
from . import auth
from .forms import *


@auth.route('/register', methods=["GET", "POST"])
def register():
    registration_form = RegistrationForm()

    return render_template("register.html", form=registration_form)