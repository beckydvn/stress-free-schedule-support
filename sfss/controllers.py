from posixpath import split
from re import S
from flask import render_template, request, session, redirect
from sfss import app, handle_queries

@app.route('/', methods=['GET'])
def index_get():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def index_post():
    list = request.form.get("list")
    split_list = list.split(",")
    if split_list:
        split_list.remove("")
    print(handle_queries.get_query_results(split_list))
    return render_template('index.html')



