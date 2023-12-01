from flask import Flask, render_template
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
                .filter(DB.cis_classes.Beruf.ID.is_(beruf_id))
        ).scalar()
    beruf_gehalt = db.session.execute(
            db.select(DB.cis_classes.Gehalt.Durchschn_Gehalt)
                .filter(DB.cis_classes.Gehalt.ID.is_(beruf_gehalt_id))
        ).scalar()
    
    return __limit_score( 40*(__mitarbeiter_gehalt(mb_id)/beruf_gehalt) -0.5)
    
def mitarbeiter_dif(mb_id):
    betrag = db.session.execute(
            db.select(DB.cis_classes.Gehalt.Durchschn_Gehalt)
                .filter(DB.cis_classes.Gehalt.ID.is_(0)) #TODO
        ).scalar()
    return __limit_score( betrag/__mitarbeiter_gehalt(mb_id)-3)

#region Vetternwirtschaft
def __versicherungsnummer_mb(mb_id):
    return db.session.execute(
        db.select(DB.cis_classes.Mitarbeiter.ID)
            .filter(DB.cis_classes.Mitarbeiter.ID.is_(mb_id))
        ).scalar()

def __eigentumer_id_from_mitarbeiter(mb_id):
    return db.session.execute(
        db.select(DB.ext_classes.Eigentuemer.ID)
            .filter(DB.ext_classes.Eigentuemer.Versicherungsnummer.is_(__versicherungsnummer_mb(mb_id)))
        ).scalar()

def __besitzer_id_from_mitarbeiter(mb_id):
    return db.session.execute(
        db.select(DB.ext_classes.Besitzer.ID)
            .filter(DB.ext_classes.Besitzer.Versicherungsnummer.is_(__versicherungsnummer_mb(mb_id)))
        ).scalar()

def vetternwirtschaft_ext(mb_id):
    eigentumer_id = __eigentumer_id_from_mitarbeiter(mb_id)
    besitzer_id = __besitzer_id_from_mitarbeiter(mb_id)
    verwandte_eigentuemer = db.session.execute(
        db.select(DB.ext_classes.Besitzer_Eigentuemer_Verwandschaft.Eigentuemer)
            .filter(DB.ext_classes.Besitzer_Eigentuemer_Verwandschaft.Besitzer.is_(besitzer_id))
        ).scalars()
    verwandte_besitzer = db.session.execute(
        db.select(DB.ext_classes.Besitzer_Eigentuemer_Verwandschaft.Besitzer)
            .filter(DB.ext_classes.Besitzer_Eigentuemer_Verwandschaft.Eigentuemer.is_(eigentumer_id))
        ).scalars()
    if not (verwandte_besitzer or verwandte_eigentuemer):
        return 0
    
    return __limit_score( 20 * (verwandte_eigentuemer.__sizeof__() + verwandte_besitzer.__sizeof__() - 2) )


def vetternwirtschaft(mb_id):
    eigentumer_id = __eigentumer_id_from_mitarbeiter(mb_id)
    besitzer_id = __besitzer_id_from_mitarbeiter(mb_id)
    verwandte_eigentuemer = db.session.execute(
        db.select(DB.ext_classes.Besitzer_Eigentuemer_Verwandschaft.Eigentuemer)
            .filter(DB.ext_classes.Besitzer_Eigentuemer_Verwandschaft.Besitzer.is_(besitzer_id))
        ).scalars()
    verwandte_besitzer = db.session.execute(
        db.select(DB.ext_classes.Besitzer_Eigentuemer_Verwandschaft.Besitzer)
            .filter(DB.ext_classes.Besitzer_Eigentuemer_Verwandschaft.Eigentuemer.is_(eigentumer_id))
        ).scalars()
    if not (verwandte_besitzer or verwandte_eigentuemer):
        return 0
    
    return __limit_score( 20 * (verwandte_eigentuemer.__sizeof__() + verwandte_besitzer.__sizeof__() - 2) )
#endregion