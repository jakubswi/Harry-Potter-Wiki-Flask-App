import requests
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.fields.choices import SelectField
from wtforms.fields.simple import SubmitField
from wtforms.validators import DataRequired

WTF_CSRF_SECRET_KEY = 'a random string'

choices = {
    'books': 'books.html',
    'characters': 'characters.html',
    'movies': 'movies.html',
    'spells': 'spells.html',
    'potions': 'potions.html',
}


class QueryForm(FlaskForm):
    query = StringField('What do you want to look up', validators=[DataRequired()])
    choice = SelectField('Choose Resources',
                         choices=[('books', 'Books'), ('characters', 'Characters'), ('movies', 'Movies'),
                                  ('spells', 'Spells'), ('potions', 'Potions')])
    submit = SubmitField('Submit')


app = Flask(__name__)
app.config['SECRET_KEY'] = WTF_CSRF_SECRET_KEY
Bootstrap5(app)


@app.route('/', methods=['GET', 'POST'])
def main_page():
    form = QueryForm()
    if request.method == 'POST' and form.validate():
        query = request.form['query']
        choice = request.form['choice']
        return redirect(url_for('query', choice=choice, query=query))
    return render_template("index.html", form=form)


@app.route('/<choice>/<query>')
def query(choice, query):
    query = query.replace(' ', '-').lower()
    try:
        response = requests.get(f'https://api.potterdb.com/v1/{choice}/{query}').json()['data']['attributes']
        return render_template(choices[choice], data=response)
    except Exception:
        flash("Name not found")
        return redirect(url_for('main_page'))


if __name__ == "__main__":
    app.run(debug=False)
