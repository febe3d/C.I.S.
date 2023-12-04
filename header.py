from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
import DB.cis_classes
import DB.ext_classes

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cisdb.db'
app.config['SQLALCHEMY_BINDS'] = {'extern': 'sqlite:///dbext.db', }
db = SQLAlchemy()
db.init_app(app)
