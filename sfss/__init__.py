from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import nltk

# NOTE: test this
if not nltk.download:
    nltk.download('omw-1.4')
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
db.drop_all()
db.create_all()
