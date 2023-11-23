from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy()
db.init_app(app)

class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(500), nullable=False)

with app.app_context():
    db.create_all()

new_test = Test(
    title="Test",
    year=2002,
    description="Test.",

)

with app.app_context():
    db.session.add(new_test)
    db.session.commit()

@app.route("/")
def home():
    result = db.session.execute(db.select(Test).order_by(Test.id))
    all_tests = result.scalars()
    return render_template("login.html", test=all_tests)


if __name__ == '__main__':
    app.run(debug=True)