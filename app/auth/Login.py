from flask import Flask
app = Flask(_name_)

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators = [DataRequired()])
    submit = SbumitField ('Submit')

@app.route('/', methods=['GET','POST'])
def index():
    name = None
    form = NameForm()
