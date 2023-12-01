from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests
import header
from header import app, db, DB, render_template
import korruptionspruefung

@app.route("/")
def home():
    Beruf = db.session.execute(db.select(DB.cis_classes.Beruf).order_by(DB.cis_classes.Beruf.ID)).scalars()
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