import header
from header import app, db, DB, render_template
from sqlalchemy import select
from datetime import datetime
import statistics

def __number_is_in(allowed_value, margin, check_value):
    return bool(check_value >= (allowed_value - margin)) & bool(check_value <= (allowed_value + margin))

def __projektpruefung_logik(budget_geplant, budget_eingetroffen, first_abgelaufen_seit):
    budget_eingetroffen_prozent = (budget_eingetroffen / budget_geplant)
    budget_margin_percent = 0.025
    if __number_is_in(1, budget_margin_percent, budget_eingetroffen_prozent): # alles ist da
        return 0
    elif budget_eingetroffen_prozent >= 1.15: # es ist viel zu viel Geld da
        return 100
    elif bool(first_abgelaufen_seit == 2) & bool(budget_eingetroffen_prozent == 0): # nichts ist eingetroffen 2 Tage nach Ablauf der Frist
        return 100
    elif bool(first_abgelaufen_seit == 1) & bool(budget_eingetroffen_prozent == 0): # nichts ist eingetroffen 1 Tage nach Ablauf der Frist
        return 85
    elif __number_is_in(4, 1, first_abgelaufen_seit): # die Frist ist vor kurzem abgelaufen
        if budget_eingetroffen_prozent <= 0.75: # mindestens 25% des Geldes fehlen
            return 95
        elif budget_eingetroffen_prozent > 0.75: # weniger als 25% des Geldes fehlen
            return 50
    return 100 # Frist ist vor längerer Zeit abgelaufen und es fehlt Geld

def projektpruefung_mit_sql(projektid):
    result = db.session.execute(db.select(DB.cis_classes.Projekt).where(DB.cis_classes.Projekt.ID == projektid)).scalar()
    date_format = "%Y-%M-%d"
    budget_geplant = float(getattr(result, 'Eingeplantes_Budget'))
    budget_eingetroffen = float(getattr(result, 'Eingetroffenes_Budget'))
    first_abgelaufen_seit = datetime.now() - datetime.strptime(getattr(result, 'Datum_Geldeingang'), date_format)
    return __projektpruefung_logik(budget_geplant, budget_eingetroffen, first_abgelaufen_seit)

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
    return __limit_score( 40*((__mitarbeiter_gehalt(mb_id)/average_beruf) -1.5))

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

# Vetternwirtschaft
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

def geldfluss(zweck):
    verdacht = ["Neue Werkzeuge", "Diebstahl", "Steuerhinterziehung"]

    if zweck in verdacht:
        return 10


def verdaechtiger_empfaenger(id):
    verdacht = [1, 666, 69]
    if id in verdacht:
        return 15
