from flask import Flask, request, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import Required, Email

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.debug = True

@app.route('/')
def home():
    return "Hello, world!"

class ItunesForm(FlaskForm):
    artist_name = StringField('What is the artist name?', validators=[Required()])
    number_results = IntegerField('How many results do you want from the API?', validators=[Required()])
    email = StringField('What is your email?', validators=[Required(),Email()])
    submit = SubmitField('Submit')

@app.route('/itunes-form')
def itunes_form():
    itunesform =ItunesForm()
    return render_template('itunes-form.html', form=itunesform)

@app.route('/itunes-result', methods = ['GET', 'POST'])
def itunes_result():
    form = ItunesForm(request.form)
    params_diction = {}
    base_url = "https://itunes.apple.com/search"
    if request.method == "POST" and form.validate_on_submit():
        params_diction["term"] = form.artist_name.data
        params_diction["limit"] = form.number_results.data
        resp = requests.get(base_url,params=params_diction)
        text = resp.text
        python_obj = json.loads(text)
        result_py = python_obj['results']
        return render_template('itunes-result.html',result_html = result_py)
    flash('All fields are required!')
    return redirect(url_for('itunes_form')) #this redirects you to itunes_form if there are errors

if __name__ == '__main__':
    app.run()
