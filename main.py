from flask import request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests
import header
from header import app, db, DB, render_template
import korruptionspruefung

class CreateForm(FlaskForm): # todo get mitarbieter id from name # todo what if name % mitarbeiter id is there?
    # Nachname = StringField("Nachname")
    # Vorname = StringField("Vorname")
    Projektname = StringField("Projektname")
    # Versicherungsnummer = StringField("Versicherungsnummer")
    Mitarbeiter_ID = StringField("Mitarbeiter-ID", validators=[DataRequired()])
    # IBAN = StringField("IBAN")
    submit = SubmitField("Prüfung Starten")
    # submit2 = SubmitField("Start project analysis")

@app.route("/")
def home():
    return render_template("login.html")

@app.route("/startseite")
def startseite():
    return render_template("startseite.html", active_page='startseite')

@app.route("/optionen")
def optionen():
    return render_template("options.html", active_page='optionen')

class resultat():
    def __init__(self):
        self.mitarbeiter_beruf_dif = 0
        self.mitarbeiter_dif = 0
        self.vetternwirtschaft = 0
        self.projekt = 0

@app.route("/resultatseite")
def resultatseite():
    return render_template("resultatseite.html", active_page='resultatseite')

@app.route("/suche", methods=["GET", "POST"])
def suche():
    form = CreateForm()
    if form.validate_on_submit():
        Mitarbeiter_ID = form.Mitarbeiter_ID.data
        # TODO erstellen von resulat in eigene funktion?
        #Suche nach Mitarbeiter_ID
        mb_id = db.session.execute(
            db.select(DB.cis_classes.Mitarbeiter.ID)
            .filter(DB.cis_classes.Mitarbeiter.ID.is_(Mitarbeiter_ID))
        ).scalar()

        projektname = form.Projektname.data
        #TODO if no projektname entered what then?

        if mb_id is None:
            return render_template("searchMenu.html", active_page='suche', form=form)

        r = resultat()
        r.mitarbeiter_beruf_dif = header.mitarbeiter_beruf_dif(mb_id)
        r.mitarbeiter_dif = header.mitarbeiter_dif(mb_id)
        r.vetternwirtschaft = 0
        #TODO can i gve string here?
        r.projekt = korruptionspruefung.projektpruefung_mit_sql(projektname) if len(projektname) > 0 else 'No Project has been checked'

        return render_template("resultatseite.html", active_page='resultatseite', r=r)

    return render_template("searchMenu.html", active_page='suche', form=form)

if __name__ == '__main__':
    app.run(debug=True)