from flask import current_app, render_template
from flask_mail import Message
from .. import mail


# Adapted from Flask Web Development: Developing Web Applications with Python 2nd Edition,  978-1491991732
def send_email(to, subject, template, **kwargs):
    """Will send an email to the indicated recipient"""

    app = current_app
    message = Message(app.config['LOGIN_MAIL_SUBJECT_PREFIX'] + subject,
                      sender=app.config['LOGIN_MAIL_SENDER'],
                      recipients=[to])

    message.html = render_template(template, **kwargs)
    mail.send(message)
