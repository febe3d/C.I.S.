from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Fahrzeugtyp(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    Fahrzeugart = db.Column(db.String(50))
    Model = db.Column(db.String(50))
    Wert = db.Column(db.Float)
    Farbe = db.Column(db.String(30))

class Eigentuemer(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    Vorname = db.Column(db.String(50), nullable=False)
    Nachname = db.Column(db.String(50), nullable=False)

class Besitzer(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    Vorname = db.Column(db.String(50), nullable=False)
    Nachname = db.Column(db.String(50), nullable=False)
    Besitzbeginn = db.Column(db.Date, nullable=False)
    Besitzende = db.Column(db.Date)

class Besitzer_Eigentuemer_Verwandschaft(db.Model):
    Besitzer = db.Column(db.Integer, db.ForeignKey("Eigentuemer.ID"), nullable=False)
    Eigentuemer = db.Column(db.Integer, db.ForeignKey("Besitzer.ID"), nullable=False)

class Kennzeichen(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    Besitzer = db.Column(db.Integer, db.ForeignKey("Besitzer.ID"), nullable=False)
    Fahrzeugtyp = db.Column(db.Integer, db.ForeignKey("Fahrzeugtyp.ID"))
    KennzeichenText = db.Column(db.String(50), nullable=False)
    Land = db.Column(db.String(3))
    Eigentuemer = db.Column(db.Integer, db.ForeignKey("Eigentuemer.ID"), nullable=False)