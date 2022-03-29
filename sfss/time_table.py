import copy
from enum import Enum
from functools import total_ordering
from random import Random
from typing import Dict
from pip import main
from tabulate import tabulate

class Days(Enum):
    MON = 1
    TUES = 2
    WED = 3
    THURS = 4
    FRI = 5
    
class TimePreference(Enum):
    EARLY = 1
    MID = 2
    LATE = 3
    SPREAD = 4
    NA = 5

# lower number represents higher priority
# each priority value must be at least 24 apart from the last for heuristic to work
# heuristic adds priority to score, (score between 0-23 (based on hours)) keeps priorities in seperate score tiers
class Priority(Enum):
    HIGH = 0
    MID = 50
    LOW = 100

'''
class CompactnessPreference(Enum):
    COMPACT = 1
    SPREAD = 2
    NA = 3
'''

class Time():
    def __init__(self, hour:int, min:int=0, pm=False):
        self.time_string = "%d:%s%s"%(hour,str(min) if min>=10 else str(min)+"0","pm" if pm else "am")       
        if pm:
            hour += 12
        min = (min/60) % 1
        self.mil_time = hour+min # 24h time

    def __str__(self):
        return self.time_string
    def __repr__(self):
        return self.time_string

class LessonTime():
    ''' has start time, end time of a class (24hour clock) '''
    def __init__(self, start:Time, end:Time, day:Days):
        self.start = start.mil_time
        self.end = end.mil_time
        self.day = day

        self.start_string = start.time_string
        self.end_string = end.time_string

    def __str__(self):
        return "%s-%s" %(self.start_string, self.end_string)
    def __repr__(self):
        return "%s-%s" %(self.start_string, self.end_string)

class Section: 
    ''' list of times course runs '''
    def __init__(self, lessons_list:list[LessonTime], name="Section"):
        self.lessons_list = lessons_list
        self.ave_start_time = sum([course.start for course in  lessons_list])/len(lessons_list) # used for determinig timezone of the section (early/miday/late)
        self.name = name

    def __str__(self):
        return self.name + ": " + " ".join(["[" + str(lesson) + "]" for lesson in self.lessons_list])
    def __repr__(self):
        return self.name + ": " + " ".join(["[" + str(lesson) + "]" for lesson in self.lessons_list])

class Course:
    ''' has list of sections course can be taken, potentially priorities depending on how much student wants to take it '''
    def __init__(self, name:str, section_list: list[Section], priority:Priority=Priority.LOW):
        self.section_list = section_list
        self.priority = priority
        self.name = name
    
    def __str__(self):
        return self.name + ": " + " ".join(["\n\t" + str(section) for section in self.section_list])
    def __repr__(self):
        return self.name + ": " + " ".join(["\n\t" + str(section) for section in self.section_list])

class Query:
    ''' list of courses student wants to take, flags for preferences (time)/ (table compactness) '''
    def __init__(self, course_list:list[Course], time_preference:TimePreference=TimePreference.NA):
        self.course_list = course_list
        self.time_preference = time_preference
        # private vars for table generation
        # overall ave start time
        self.__ave_start_time = 0
        # total number of lessons added to the table
        self.__lessons_added = 0
        # flag for when remaining courses need to be sorted again
        self.table, self.conflicting = self.generate_table()
    
    def __str__(self):
        return str(self.table)
    def __repr__(self):
        return str(self.table)
    
    def show_table(self):
        start_time = 7
        end_time = 23
        times = [Time(hour%12 if hour >= 13 else hour, min, True if hour>=12 else False) for hour in range(start_time,end_time) for min in range(0,60,30) ]

        '''
        for hour in range (start_time, end_time):
            for min in range (0,60,30):
                print(Time(hour%12 if hour >= 13 else hour, min, True if hour>=12 else False))
        '''
        # every row represents 30 mins, every col represents a day
        table = [[0 for _ in range(len(Days)+1)] for _ in range(len(times))]

        for row in range(len(times)):
            for col in range(len(Days)+1):
                if col == 0:
                    table[row][col] = times[row].time_string
                else:
                    for course_lesson in self.table[Days(col)]:
                        if times[row].mil_time >= course_lesson[1].start and times[row].mil_time <= course_lesson[1].end:
                            table[row][col] = course_lesson[0]
                            break
        print(tabulate(table, headers=["Times","Mond", "Tues", "Wed", "Thurs", "Fri"]))

    def generate_table(self):
        '''
        Returns tuple (dictionary with days mapping to (course name, Time), conflicting courses not included in table)
        '''
        # courses still needing to be added to schedule
        remaining = copy.deepcopy(self.course_list)
        new_remaining = remaining
        # set of conflicting courses (not included in final table)
        conflicting = set()
        # dictionary representing schedule of each day
        table_dict = {day: set() for day in Days}

        # sort sections within courses
        self.__sort_sections(remaining)
        # sort courses by best section
        remaining.sort(key=lambda s: self.__time_heuristic(s.section_list[0]))
        while remaining:
            for course in remaining:
                old_lessons = self.__lessons_added
                self.__try_to_add(course, table_dict, conflicting, new_remaining)
                                
                # if they want spread and new section was added
                if self.time_preference == TimePreference.SPREAD and  old_lessons != self.__lessons_added:
                    # update priority based on new mean
                    self.__sort_sections(new_remaining)
                    remaining.sort(key=lambda s: self.__time_heuristic(s.section_list[0],s.priority))
            
            # take out the courses that were added
            remaining = new_remaining
        return table_dict, conflicting
                
    def __sort_sections(self, remaining):
        for course in remaining:
            # sort sections within courses
            if len(course.section_list) > 1:
                course.section_list.sort(key=lambda s: self.__time_heuristic(s))

    def __time_heuristic(self, section:Section, priority:Priority=Priority.LOW):
        # priority value is high enough to bump courses of dif priorities out of each other's tiers
        # time preference will only be relevant against other courses of same priority
        if self.time_preference == TimePreference.EARLY:
            return section.ave_start_time + priority.value  
        elif self.time_preference == TimePreference.MID:
            return abs(12 - section.ave_start_time) + priority.value
        elif self.time_preference == TimePreference.LATE:
            return 24 - section.ave_start_time + priority.value
        elif self.time_preference == TimePreference.SPREAD:
            return abs(self.__ave_start_time - section.ave_start_time) * priority.value
        else:
            return Random.random()

    def __no_conflict(self, course:Course, table:Dict[Days, tuple]):
        ''' return true if no conflict, false if conflict '''
        for lesson_time in course.section_list[0].lessons_list:
            if lesson_time in [x[1] for x in table[lesson_time.day]]:
                return False
        return True
    
    def __add_to_table(self, course:Course, table:Dict[Days, tuple], new_remaining):
        for lesson_time in course.section_list[0].lessons_list:
            self.__lessons_added += 1
            # total + new / size
            self.__ave_start_time = ((self.__ave_start_time * (self.__lessons_added-1)) + lesson_time.start) / self.__lessons_added
            table[lesson_time.day].add((course.name, lesson_time))
        new_remaining.remove(course)
        
    def __try_to_add(self, course:Course, table_dict:Dict[Days, tuple], conflicting:set, new_remaining):
        # only 1 section, just try to add it immediately
        if len(course.section_list) == 1:
            if self.__no_conflict(course, table_dict):
                self.__add_to_table(course, table_dict, new_remaining)
                self.__dirty = True
            else:
                conflicting.add(course.name)
                new_remaining.remove(course)
        # multiple sections
        else:
            if self.__no_conflict(course, table_dict):
                self.__add_to_table(course, table_dict, new_remaining)
                self.__dirty = True
            else:
                course.section_list.pop(0)
                # re-sort courses to set this course to the right index based on new best section 
                new_remaining.sort(key=lambda s: self.__time_heuristic(s.section_list[0]))
    





if __name__ == "__main__":
    class1 = LessonTime(Time(8,30), Time(9,30), Days.MON)
    class2 = LessonTime(Time(10,30), Time(11,30), Days.TUES)
    class3 = LessonTime(Time(9,30), Time(10,30), Days.WED)
    print(class1)

    section1 = Section([class1, class2, class3], "Section 1")
    #print(section1.ave_start_time)

    class4 = LessonTime(Time(5,30, True), Time(6,30, True), Days.WED)
    class5 = LessonTime(Time(4,30, True), Time(5,30, True), Days.THURS)
    class6 = LessonTime(Time(8,30, True), Time(9,30, True), Days.FRI)

    section2 = Section([class4, class5, class6], "Section 2")
    #print(section2.ave_start_time)

    course1 = Course("course 1", [section1, section2])

    class7 = LessonTime(Time(10,30), Time(11,30), Days.WED)
    class8 = LessonTime(Time(2, 0,True), Time(3, 0, True), Days.THURS)
    class9 = LessonTime(Time(9), Time(10), Days.FRI)

    section3 = Section([class7, class8, class9], "Section 3")
    #print(section3.ave_start_time)

    course2 = Course("course 2", [section3, section2])
    
    query1 = Query([course1, course2], TimePreference.LATE)
    query1.show_table()
    print(query1)
    print(course1)
    print(course2)





