import header
from header import app, db, DB, render_template
from sqlalchemy import select
# TODO pruefungen hier hin verlagern?
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

def projektpruefung_mit_sql(projektname):
    result = db.session.execute(db.select(DB.cis_classes.Projekt).where(DB.cis_classes.Projekt.Name == projektname)).scalar()
    budget_geplant = getattr(result, 'Eingeplantes_Budget')
    budget_eingetroffen = getattr(result, 'Eingetroffenes_Budget')
    first_abgelaufen_seit = getattr(result, 'Datum_Geldeingang') # TODO calc how?
    return __projektpruefung_logik(budget_geplant, budget_eingetroffen, first_abgelaufen_seit)