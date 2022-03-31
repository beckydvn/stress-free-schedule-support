from posixpath import split
from re import S
from flask import render_template, request, session, redirect
from sfss import app, handle_queries

@app.route('/', methods=['GET'])
def index_get():
    return render_template('index.html')

@app.route('/course_result', methods=['GET'])
def course_result_get():
    return render_template('course_result.html')

@app.route('/', methods=['POST'])
def index_post():
    split_list = request.form.get("list").split(",")
    exclusive = request.form.get("course-search-mode")
    if exclusive:
        result = handle_queries.get_query_results(split_list, exclusive=True)
    else:
        result = handle_queries.get_query_results(split_list, exclusive=False)
    f = open("output.json", "w")
    f.write(result)
    return render_template('course_result.html', output=result)
