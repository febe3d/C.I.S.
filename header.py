from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
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
