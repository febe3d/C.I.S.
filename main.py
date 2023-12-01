from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests
import header
from header import app, db, DB, render_template
import korruptionspruefung


class CreateForm(FlaskForm):
    Nachname = StringField("Nachname", validators=[DataRequired()])
    Vorname = StringField("Vorname", validators=[DataRequired()])
    Projektname = StringField("Projektname", validators=[DataRequired()])
    Versicherungsnummer = StringField("Versicherungsnummer", validators=[DataRequired()])
    Mitarbeiter_ID = StringField("Mitarbeiter_ID", validators=[DataRequired()])
    IBAN = StringField("IBAN", validators=[DataRequired()])
    submit = SubmitField("Start person search")
    submit2 = SubmitField("Start project analysis")



@app.route("/")
def home():
    Beruf = db.session.execute(db.select(DB.cis_classes.Beruf).order_by(DB.cis_classes.Beruf.ID)).scalars()
    print(header.calculate_mitarbeiter_dif_score(0))
    return render_template("login.html", Beruf=Beruf)


@app.route("/startseite")
def startseite():
    return render_template("startseite.html", active_page='startseite')


@app.route("/optionen")
def optionen():
    return render_template("options.html", active_page='optionen')


@app.route("/resultatseite")
def resultatseite():
    return render_template("resultatseite.html", active_page='resultatseite')


@app.route("/suche", methods=["GET", "POST"])
def suche():
    form = CreateForm()
    if form.validate_on_submit():
        Nachname = form.Nachname.data
        Vorname = form.Vorname.data

        print(Nachname)
        print(Vorname)

    return render_template("searchMenu.html", active_page='suche', form=form)


if __name__ == '__main__':
    app.run(debug=True)
