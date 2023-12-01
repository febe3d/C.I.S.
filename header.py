from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
import statistics
import DB.cis_classes
import DB.ext_classes

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cisdb.db'
app.config['SQLALCHEMY_BINDS'] = {'extern' : 'sqlite:///dbext.db',}
db = SQLAlchemy()
db.init_app(app)

def geldfluss():
    verwendungszwecke = db.session.execute(
        db.select(DB.cis_classes.Geldfluss.Verwendungszweck).order_by(DB.cis_classes.Geldfluss.ID)).scalars()
    verdächtig = ["Neue Werkzeuge", "Diebstahl", "Steuerhinterziehung"]
    for zweck in verwendungszwecke:

        if zweck in verdächtig:
            print("Aha " + zweck)
    empfanger = db.session.execute(
        db.select(DB.cis_classes.Geldfluss.EmpfaengerKonto).order_by(DB.cis_classes.Geldfluss.ID)).scalars()
    verdächtige = [1, 666, 69]
    for verdächtiger in empfanger:

        if verdächtiger in verdächtige:
            print("Aha " + str(verdächtiger))

def __limit_score(score):
    return min(100, max(0, score))

def __mitarbeiter_gehalt(mb_id):
    mb_gehalt_id = db.session.execute(
            db.select(DB.cis_classes.Mitarbeiter.Gehalt)
                .filter(DB.cis_classes.Mitarbeiter.ID.is_(mb_id))
        ).scalar()
    return db.session.execute(
            db.select(DB.cis_classes.Gehalt.Durchschn_Gehalt)
               .filter(DB.cis_classes.Gehalt.ID.is_(mb_gehalt_id))
        ).scalar()

def mitarbeiter_dif(mb_id):
    beruf_id = db.session.execute(
            db.select(DB.cis_classes.Mitarbeiter.Beruf)
                .filter(DB.cis_classes.Mitarbeiter.ID.is_(mb_id))
        ).scalar()
    alle_mit_beruf_gehalt_ids = db.session.execute(
            db.select(DB.cis_classes.Mitarbeiter.Gehalt)
                .filter(DB.cis_classes.Mitarbeiter.Beruf.is_(beruf_id))
        ).scalars()
    
    alle_gehaelter_beruf = db.session.execute(
            db.select(DB.cis_classes.Gehalt.Durchschn_Gehalt)
                .where(DB.cis_classes.Gehalt.ID.in_(alle_mit_beruf_gehalt_ids))
        ).scalars()
    average_beruf = statistics.mean([float(gehalt) for gehalt in alle_gehaelter_beruf])
    return __limit_score( 40*(__mitarbeiter_gehalt(mb_id)/average_beruf) -0.5)

def mitarbeiter_beruf_dif(mb_id):
    #Beruf Gehalt ermitteln
    beruf_id = db.session.execute(
            db.select(DB.cis_classes.Mitarbeiter.Beruf)
                .filter(DB.cis_classes.Mitarbeiter.ID.is_(mb_id))
        ).scalar()
    beruf_gehalt_id = db.session.execute(
            db.select(DB.cis_classes.Beruf.ID)
                .filter(DB.cis_classes.Mitarbeiter.ID.is_(beruf_id))
        ).scalar()
    beruf_gehalt = db.session.execute(
            db.select(DB.cis_classes.Gehalt.Durchschn_Gehalt)
                .filter(DB.cis_classes.Gehalt.ID.is_(beruf_gehalt_id))
        ).scalar()
    
    return __limit_score( 40*(__mitarbeiter_gehalt(mb_id)/beruf_gehalt) -0.5)
    
def mitarbeiter_dif():
    #Konto mit Mitarbeiter verknüpfen?
    return False

# def vetternwirtschaft(ID):
#query_vsnr = "Select Versicherungsnummer from cis where ID = " + ID
#query_mitarbeiter = "Select from cis where Versicherungsnummer = " + query_vsnr
#query_eigentuemer = "Select from ext where Versicherungsnummer = " + query_vsnr
#versicherungsnummer =
#mitarbeiter = (db.session.execute(db.select(DB.cis_classes.Mitarbeiter.Versicherungsnummer).order_by(DB.ext_classes.Mitarbeiter.ID)).scalar()
#eigentumer = (db.session.execute(db.select(DB.ext_classes.Eigentuemer.Versicherungsnummer).order_by(DB.ext_classes.Eigentuemer.ID)).scalar()
#if query_vsnr == 1 in mitarbeiter.Versicherungsnummer = query_vsnr == 1 in eigentuemer.Versicherungsnummer:
#verdaechtigkeitsgrad += 20