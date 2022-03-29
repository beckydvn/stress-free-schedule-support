from flask import render_template, request, session, redirect
from sfss import app

@app.route('/')
def home():
    return render_template('index.html')

