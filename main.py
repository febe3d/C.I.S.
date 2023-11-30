from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests
import DB.cis_classes

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cisdb.db'
# db = SQLAlchemy()
# db.init_app(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cisdb.db'
app.config['SQLALCHEMY_BINDS'] = {'extern' : 'sqlite:///dbext.db',}
db = SQLAlchemy()
db.init_app(app)

@app.route("/")
def home():
    result = db.session.execute(db.select(DB.cis_classes.Beruf).order_by(DB.cis_classes.Beruf.ID))
    Beruf = result.scalars()
    result1 = db.session.execute(db.select(DB.cis_classes.Beruf.Berufname)).scalar()
    print(result1)
    return render_template("resultatseite.html", Beruf=Beruf)

@app.route("/startseite")
def startseite():
    return render_template("startseite.html", active_page='startseite')

@app.route("/optionen")
def optionen():
    return render_template("options.html", active_page='optionen')

@app.route("/resultatseite")
def resultatseite():
    return render_template("resultatseite.html", active_page='resultatseite')

@app.route("/suche")
def suche():
    return render_template("searchMenu.html", active_page='suche')

if __name__ == '__main__':

    app.run(debug=True)