from . import profile
from flask import render_template, request, redirect, url_for, flash
from .forms import PatientProfileForm


@profile.route('/profile', methods=["GET", "POST"])
def profile():
    """Display profile page"""

    profile_form = PatientProfileForm()
    # retrieve patient information
    # set form objects to patient information

    return render_template("profile.html", form=profile_form)