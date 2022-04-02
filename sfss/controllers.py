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

@app.route('/plan_table', methods=['GET'])
def plan_table_get():
    return render_template('plan_table.html')

@app.route('/table_results', methods=['GET'])
def table_results_get():
    return render_template('table_results.html')

@app.route('/', methods=['POST'])
def index_post():
    split_list = request.form.get("list").split(",")
    result = handle_queries.get_query_results(split_list)
    if len(result) <= 2:
        return render_template('index.html', message="No results were found! Please try entering different subjects.")    
    else:
        return render_template('course_result.html', output=result, message="Based on your preferences:")

'''
@app.route('/plan_table', methods=['POST'])
def table_post():
    for lesson in _:
        request.form.get(lesson_time)
'''

'''
@app.route('/course_results', methods=['POST'])
def elective_button():
    return render_template('index.html')
'''