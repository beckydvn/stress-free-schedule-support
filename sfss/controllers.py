import json
from re import S
import time
from flask import render_template, request, session, redirect
from sfss import app, handle_queries, time_table
import ast

@app.route('/', methods=['GET'])
def index_get():
    return render_template('index.html')

@app.route('/elective_suggestion', methods=['GET'])
def elective_suggestion_get():
    return render_template('/elective_suggestion.html')

@app.route('/elective_suggestion', methods=['POST'])
def elective_suggestion_post():
    split_list = request.form.get("list").split(",")
    result = handle_queries.get_query_results(split_list)
    if len(result) <= 2:
        return render_template('elective_suggestion.html', message="No results were found! Please try entering different subjects.")    
    else:
        return render_template('course_result.html', output=result, message="BASED ON YOUR PREFERENCES:")

@app.route('/course_result', methods=['GET'])
def course_result_get():
    return render_template('course_result.html')

@app.route('/plan_table', methods=['GET'])
def plan_table_get():
    return render_template('plan_table.html')

@app.route('/table_results', methods=['GET'])
def table_results_get():
    return render_template('table_results.html')




@app.route('/plan_table', methods=['POST'])
def table_post():
    # form sent as { course(i)-section(x)-lesson(z) : "day", "start", "end"} 
    # and {priority(i) : (high/medium/low)}
    # and {name(i) : course name of course i}
    # and {preference : early/mid/late/spread/na } 
    dict_given = request.form
    last_course = 0
    last_section = 0
    course_list = []
    section_list = []
    lesson_list = []    
    # for entry in dict_given:
    #     if not dict_given[entry]:
    #         return render_template('plan_table.html', warning="Please fill in all the required fields before submitting.")
    for entry in dict_given:
        # if this key is one of the lesson keys (course(i)-section(x)-lesson(z)) create the associated lesson object
        if entry[0] == 'c':
            info = entry.split("-")
            course_num = int(info[0][-1])
            section_num = int(info[1][-1])
            lesson_time = dict_given[entry]
            time_info = lesson_time.split(",")
            # setup day enum
            day = time_info[0]
            if day == "MON":
                day = time_table.Days.MON
            elif day == "TUES":
                day = time_table.Days.TUES
            elif day == "WED":
                day = time_table.Days.WED
            elif day == "THURS":
                day = time_table.Days.THURS
            elif day == "FRI":
                day = time_table.Days.FRI
            # setup start time object
            start = time_info[1].split(":")
            hr = int(start[0])
            min = int(start[1][0:2])
            # setup am/pm start time enum
            am_pm = time_table.AmPm.AM if start[1][-2:] == "AM" else time_table.AmPm.PM
            start_time = time_table.Time(hr, min, am_pm)
            # setup end time object
            end = time_info[2].split(":")
            hr = int(end[0])
            min = int(end[1][0:2])
            # setup am/pm end time enum
            am_pm = time_table.AmPm.AM if end[1][-2:] == "AM" else time_table.AmPm.PM
            end_time = time_table.Time(hr, min, am_pm)
            if course_num == last_course:
                # if course and section is the same
                if section_num == last_section:
                    # add new lesson to the current lesson list
                    lesson_list.append(time_table.LessonTime(start_time, end_time, day))
                    print(lesson_list)
                # if same course but new section
                else:
                    # create previous section using built up lesson list
                    section_list.append(time_table.Section(lesson_list, "Section %s"%(last_section)))
                    # reset lesson list for new section, and add this to new one for this section 
                    lesson_list = []
                    lesson_list.append(time_table.LessonTime(start_time, end_time, day))
            # if new course entirely
            else:
                # create the last section we were building up, add it to current section list
                section_list.append(time_table.Section(lesson_list, "Section %s"%(last_section)))
                # create previous course using built up section list 
                priority = request.form.get("priority%s"%(last_course))
                if priority == "high":
                    priority = time_table.Priority.HIGH
                elif priority == "medium":
                    priority = time_table.Priority.MID
                else:
                    priority = time_table.Priority.LOW
                course_name = request.form.get("name%s"%(last_course))
                prev_course = time_table.Course(course_name, section_list, priority)
                course_list.append(prev_course)
                print(course_list)
                # clear lesson and section lists for next course, add this new one as first lesson
                section_list = []
                lesson_list = []
                lesson_list.append(time_table.LessonTime(start_time, end_time, day))
            last_course = course_num
            last_section = section_num
    
    # add the final lesson list to the last section and build the last course
    section_list.append(time_table.Section(lesson_list, "Section %s"%(last_section)))
    # get priority for this last course
    priority = request.form.get("priority%s"%(course_num))
    if priority == "high":
        priority = time_table.Priority.HIGH
    elif priority == "medium":
        priority = time_table.Priority.MID
    else:
        priority = time_table.Priority.LOW
    course_name = request.form.get("name%s"%(course_num))
    prev_course = time_table.Course(course_name, section_list, priority)
    course_list.append(prev_course)

    preference = request.form.get("preference")
    if preference == "early":
        preference = time_table.TimePreference.EARLY
    elif preference == "mid":
        preference = time_table.TimePreference.MID
    elif preference == "late":
        preference = time_table.TimePreference.LATE
    elif preference == "spread":
        preference = time_table.TimePreference.SPREAD
    elif preference == "na":
        preference = time_table.TimePreference.NA
        
    print(course_list)
    query = time_table.Query(course_list, preference)
    query.show_table()
    return_dict = query.get_better_dict()
    if query.conflicting:
        return render_template('table_results.html', message="The following courses could not be included due to conflicts: " + ", ".join(query.conflicting), output=json.dumps(return_dict))    
    else:
        return render_template('table_results.html', output=json.dumps(return_dict))
