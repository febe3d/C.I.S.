import header
from header import app, db, DB, render_template
from sqlalchemy import select

def __number_is_in(allowed_value, margin, check_value):
    return bool(check_value >= (allowed_value - margin)) & bool(check_value <= (allowed_value + margin))
#variablen
def __projektpruefung_logik(budget_geplant, budget_eingetroffen, frist_ablaufdatum):
    first_abgelaufen_seit = 0 # TODO
    budget_eingetroffen_prozent = (budget_eingetroffen / budget_geplant)
    budget_margin_percent = 0.025
#pruefung
    if __number_is_in(1, budget_margin_percent, budget_eingetroffen_prozent): # alles ist da
        return 0
    elif budget_eingetroffen_prozent >= 1.15: # es ist viel zu viel Geld da
        return 100
    elif first_abgelaufen_seit == 2 & budget_eingetroffen_prozent == 0: # nichts ist eingetroffen 2 Tage nach Ablauf der Frist
        return 100
    elif first_abgelaufen_seit == 1 & budget_eingetroffen_prozent == 0: # nichts ist eingetroffen 1 Tage nach Ablauf der Frist
        return 85
    elif __number_is_in(4, 1, first_abgelaufen_seit): # die Frist ist vor kurzem abgelaufen
        if budget_eingetroffen_prozent < 0.25: # weniger als 25% des Geldes fehlen
            return 50
        elif budget_eingetroffen_prozent >= 0.25: # mindestens 25% des Geldes fehlen
            return 75
    return 100 # Frist ist vor längerer Zeit abgelaufen und es fehlt Geld

def projektpruefung_mit_sql(projektname):
    result = db.session.execute(db.select(DB.cis_classes.Projekt).where(DB.cis_classes.Projekt.Name == projektname)).scalar()
    budget_geplant = getattr(result, 'Eingeplantes_Budget')
    budget_eingetroffen = getattr(result, 'Eingetroffenes_Budget')
    frist_ablaufdatum = getattr(result, 'Datum_Geldeingang')
    return __projektpruefung_logik(budget_geplant, budget_eingetroffen, frist_ablaufdatum)


# benutzer startet prüfung
# wir holen einmal alle Daten per select und spiechern die
# die Koruptionstest bekommen die Daten, aber machne sleber keine selects