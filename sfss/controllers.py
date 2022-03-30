from flask import render_template, request, session, redirect
from sfss import app, handle_queries

@app.route('/', methods=['GET'])
def index_get():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def index_post():
    return "TEST"
    # return handle_queries.get_query_results(request.form.get('userInput'))


