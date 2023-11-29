from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Gehalt(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    Durchschn_Gehalt = db.Column(db.Float, nullable=False)
    Durchschn_Boni = db.Column(db.Float, nullable=False)

class KontoInhaber(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    Vorname = db.Column(db.String(50), nullable=False)
    Nachname = db.Column(db.String(50), nullable=False)

class Konto(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    Inhaber = db.Column(db.Integer, db.ForeignKey("KontoInhaber.ID"), nullable=False)
    Kontotyp = db.Column(db.String(20))
    Kontonummer = db.Column(db.String(50), nullable=False)
    Land = db.Column(db.String(3), nullable=False)
    IBAN = db.Column(db.String(34), nullable=False)
    Betrag = db.Column(db.DECIMAL, nullable=False)

class Geldfluss(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    Verwendungszweck = db.Column(db.String(255))
    Waehrung = db.Column(db.String(3), nullable=False)
    EmpfaengerKonto = db.Column(db.Integer, db.ForeignKey("Konto.ID"), nullable=False)
    AufraggeberKonto = db.Column(db.Integer, db.ForeignKey("Konto.ID"), nullable=False)
    Betrag = db.Column(db.Float, nullable=False)

class Projekt(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    Konto = db.Column(db.Integer, db.ForeignKey("Konto.ID"), nullable=False)
    Name = db.Column(db.String(50), nullable=False)
    Eingeplantes_Budget = db.Column(db.DECIMAL, nullable=False)
    Eingetroffenes_Budget = db.Column(db.DECIMAL, nullable=False)
    Datum_Geldeingang = db.Column(db.Date, nullable=False)

class Beruf(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    Gehalt = db.Column(db.Integer, db.ForeignKey("Gehalt.ID"), nullable=False)
    Berufname = db.Column(db.String(50), nullable=False)

class Mitarbeiter(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    Beruf = db.Column(db.Integer, db.ForeignKey("Beruf.ID"), nullable=False)
    Projekzugehoerigkeit = db.Column(db.Integer, db.ForeignKey("Projekt.ID"), nullable=False)
    KontoInhaber = db.Column(db.Integer, db.ForeignKey("KontoInhaber.ID"), nullable=False)
    Gehalt = db.Column(db.Integer, db.ForeignKey("Gehalt.ID"), nullable=False)
    Versicherungsnummer = db.Column(db.String(12), nullable=False)

class Verwandschaft(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    Verwandschaft1 = db.Column(db.Integer, db.ForeignKey("Mitarbeiter.ID"), nullable=False)
    Verwandschaft2 = db.Column(db.Integer, db.ForeignKey("Mitarbeiter.ID"), nullable=False)

class Gehaltbestimmung(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    GehaltGeber = db.Column(db.Integer, db.ForeignKey("Mitarbeiter.ID"), nullable=False)
    GehaltNehmer = db.Column(db.Integer, db.ForeignKey("Mitarbeiter.ID"), nullable=False)