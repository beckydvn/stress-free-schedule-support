from posixpath import split
from re import S
from flask import render_template, request, session, redirect
from sfss import app, handle_queries

@app.route('/', methods=['GET'])
def index_get():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def index_post():
    split_list = request.form.get("list").split(",")
    exclusive = request.form.get("course-search-mode")
    if exclusive:
        output = handle_queries.get_query_results(split_list, exclusive=True)
    else:
        output = handle_queries.get_query_results(split_list, exclusive=False)
    return render_template('index.html')
