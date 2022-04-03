import copy
from enum import Enum
#from random import Random
import random
from typing import Dict, List
from tabulate import tabulate

class Days(Enum):
    MON = 0
    TUES = 1
    WED = 2
    THURS = 3
    FRI = 4
    
class TimePreference(Enum):
    EARLY = 1
    MID = 2
    LATE = 3
    SPREAD = 4
    NA = 5

# lower number represents higher priority
# each priority value must be at least 48 apart from the last for heuristic to work
# heuristic adds priority to score, (score between 0-23 (based on hours) + variance of up to 23 for midday hueristic) 
# keeps priorities in seperate score tiers
class Priority(Enum):
    HIGH = 0
    MID = 50
    LOW = 100

class AmPm(Enum):
    AM = 1
    PM = 2

'''
class CompactnessPreference(Enum):
    COMPACT = 1
    SPREAD = 2
    NA = 3
'''

class Time():
    def __init__(self, hour:int, min:int=0, am_pm:AmPm=AmPm.AM):     
        if hour%12 == 0:
            hour = 12 
        elif hour>12:   # if spilled over midnight or noon, change time of day
            hour = hour%12
            if am_pm == AmPm.AM:
                am_pm = AmPm.PM
            else:
                am_pm = AmPm.AM
        self.time_string = "%d:%s%s"%(hour,str(min) if min>=10 else str(min)+"0","pm" if am_pm == AmPm.PM else "am")

        if am_pm == AmPm.PM:
            hour = hour + 12 if hour != 12 else hour
        hour = hour % 24
        min = (min/60) % 1
        self.min = min
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

        self.start_time = start
        self.end_time = end

        self.start_string = start.time_string
        self.end_string = end.time_string

    def __str__(self):
        return "%s-%s (%s)" %(self.start_string, self.end_string, self.day.name)
    def __repr__(self):
        return "%s-%s (%s)" %(self.start_string, self.end_string, self.day.name)

class Section: 
    ''' list of times course runs '''
    def __init__(self, lessons_list:List[LessonTime], name="Section"):
        self.lessons_list = lessons_list
        self.ave_start_time = sum([lesson.start for lesson in  lessons_list])/len(lessons_list) # used for determinig timezone of the section (early/miday/late)
        self.name = name
    
    def get_variance(self):
        #average variance between lessons
        variance = 0
        for lesson in self.lessons_list:
            # ave dist of lesson from other lessons
            variance += sum([abs(lesson.start-other_lesson.start) for other_lesson in self.lessons_list]) / len(self.lessons_list)
        # ave dist a lesson is from all other lessons
        variance /= len(self.lessons_list)
        return variance

    def __str__(self):
        return self.name + ": " + " ".join(["[" + str(lesson) + "]" for lesson in self.lessons_list])
    def __repr__(self):
        return self.name + ": " + " ".join(["[" + str(lesson) + "]" for lesson in self.lessons_list])

class Course:
    ''' has list of sections course can be taken, potentially priorities depending on how much student wants to take it '''
    def __init__(self, name:str, section_list: List[Section], priority:Priority=Priority.LOW):
        self.section_list = section_list
        self.priority = priority
        self.name = name
    
    def __str__(self):
        return self.name + " (Priority %s)"%(self.priority.name) + ": " + " ".join(["\n\t" + str(section) for section in self.section_list])
    def __repr__(self):
        return self.name + ": " + " ".join(["\n\t" + str(section) for section in self.section_list])

class Query:
    ''' list of courses student wants to take, flags for time preference '''
    def __init__(self, course_list:List[Course], time_preference:TimePreference=TimePreference.NA):
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

    def get_better_dict(self,table_start:Time=Time(8,0,AmPm.AM), table_end:Time=Time(10,0,AmPm.PM)):
        '''
        input: 
        table_start = Time object representing first time slot of the dictionary (inclusive) ex Time(8) = start at 8AM
        table_end = Time object representing last time slot of the dictionary (exlusive, goes to 30 min before end time provided) ex) Time(9,30,AmPm.PM) = end at 9PM
        Returns a dictionary:
        day enum value (0-4) : list of timeslots for that day, ""no class, "class name" = that class at that time slot
        '''
        times = [Time(hour%12 if hour >= 13 else hour, min, AmPm.PM if hour>=12 else AmPm.AM).time_string for hour in range(int(table_start.mil_time),int(table_end.mil_time)+1) for min in range(0,60,30) ]  # 30 min time chunks between start time and end time
        # if they wanted it to end at hour without extra minutes
        if table_end.min == 0:
            times.pop(-1)   # pop off last 30 min (example they wanted stop time 10pm, remove 10:30pm)
        new_dict = {day.value: [""]*len(times) for day in Days}
        for day in Days:
            # for each (class, lesson) tuple in this day
                for course_lesson in self.table[day]:
                    for i in range(times.index(course_lesson[1].start_time.time_string),times.index(course_lesson[1].end_time.time_string)):
                        new_dict[day.value][i] = course_lesson[0]
        return new_dict

    def show_table(self):
        start_time = 7
        end_time = 23
        times = [Time(hour%12 if hour >= 13 else hour, min, AmPm.PM if hour>=12 else AmPm.AM).time_string for hour in range(start_time,end_time) for min in range(0,60,30) ]

        '''
        for hour in range (start_time, end_time):
            for min in range (0,60,30):
                print(Time(hour%12 if hour >= 13 else hour, min, True if hour>=12 else False))
        '''
        # every row represents 30 mins, every col represents a day
        table = [[[] for _ in range(len(Days)+1)] for _ in range(len(times))]

        for row in range(len(times)):
            table[row][0] = times[row]
        for day in Days:
            # for each (class, lesson) tuple in this day
            for course_lesson in self.table[day]:
                #print(type(times[0]), type(course_lesson[1].start_time))
                for i in range(times.index(course_lesson[1].start_time.time_string),times.index(course_lesson[1].end_time.time_string)):
                    table[i][day.value+1].append(course_lesson[0])
        print(tabulate(table, headers=["Times","Mon", "Tues", "Wed", "Thurs", "Fri"]))
        return table

    def generate_table(self):
        '''
        Returns tuple (dictionary with days mapping to (course name, Time), conflicting courses not included in table)
        '''
        # courses still needing to be added to schedule
        remaining = copy.deepcopy(self.course_list)
        # set of conflicting courses (not included in final table)
        conflicting = set()
        # dictionary representing schedule of each day
        table_dict = {day: set() for day in Days}

        # sort sections within courses
        self.__sort_sections(remaining)
        # sort courses by best section
        remaining.sort(key=lambda s: self.__time_heuristic(s.section_list[0], s))
        new_remaining = remaining
        while remaining:
            for course in remaining:
                # do highest priority stuff first
                if course.priority != remaining[0].priority:
                    break 
                old_lessons = self.__lessons_added
                self.__try_to_add(course, table_dict, conflicting, new_remaining)
                                
                # if they want spread and new section was added
                if self.time_preference == TimePreference.SPREAD and  old_lessons != self.__lessons_added:
                    # update priority based on new mean
                    self.__sort_sections(new_remaining)
                    remaining.sort(key=lambda s: self.__time_heuristic(s.section_list[0],s))
            
            # take out the courses that were added
            remaining = new_remaining
        return table_dict, conflicting
                
    def __sort_sections(self, remaining):
        for course in remaining:
            # sort sections within courses
            if len(course.section_list) > 1:
                course.section_list.sort(key=lambda s: self.__time_heuristic(s, course))

    def __time_heuristic(self, section:Section, course:Course):
        # priority value is high enough to bump courses of dif priorities out of each other's tiers
        # time preference will only be relevant against other courses of same priority
        if len(course.section_list) == 1:
            return course.priority.value    # single section courses are put in first because if that one doesn't fit they don't have other options
        if self.time_preference == TimePreference.EARLY:
            return section.ave_start_time + course.priority.value  
        elif self.time_preference == TimePreference.MID:
            midday = 14
            dist_from_midday = abs(midday - section.ave_start_time) 
            total_score = dist_from_midday + section.get_variance()  # more spread out
            return total_score + course.priority.value
        elif self.time_preference == TimePreference.LATE:
            return 24 - section.ave_start_time + course.priority.value
        elif self.time_preference == TimePreference.SPREAD:
            return abs(self.__ave_start_time - section.ave_start_time) * course.priority.value
        else:
            return random.random()

    def __no_conflict(self, course:Course, table:Dict[Days, tuple]):
        ''' return true if no conflict, false if conflict '''
        own_lessons = course.section_list[0].lessons_list
        for lesson_time in course.section_list[0].lessons_list:
            # checking against other lessons in the section in case user is an idiot
            counter = 0
            for own_lesson in own_lessons:
                if lesson_time.start <= own_lesson.end and lesson_time.end >= own_lesson.start and lesson_time.day == own_lesson.day:
                    counter += 1
                    if counter >1:  # to account for itself in the lesson list
                        return False
            dict_entries = [x[1] for x in table[lesson_time.day]]
            for entry in dict_entries:
                if (lesson_time.start < entry.end and lesson_time.end > entry.start) or (lesson_time.start == entry.start and lesson_time.end == entry.end):
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
            else:
                conflicting.add(course.name)
                new_remaining.remove(course)
        # multiple sections
        else:
            if self.__no_conflict(course, table_dict):
                self.__add_to_table(course, table_dict, new_remaining)
            else:
                course.section_list.pop(0)
                # re-sort courses to set this course to the right index based on new best section 
                new_remaining.sort(key=lambda s: self.__time_heuristic(s.section_list[0], s))
    


    





if __name__ == "__main__":
    
    '''
    class1 = LessonTime(Time(8,30), Time(9,30), Days.MON)
    class2 = LessonTime(Time(10,30), Time(11,30), Days.TUES)
    class3 = LessonTime(Time(9,30), Time(10,30), Days.WED)
    #print(class1)

    section1 = Section([class1, class2, class3], "Section 1")
    #print(section1.ave_start_time)

    class4 = LessonTime(Time(5,30, AmPm.PM), Time(6,30, AmPm.PM), Days.WED)
    class5 = LessonTime(Time(4,30, AmPm.PM), Time(5,30, AmPm.PM), Days.THURS)
    class6 = LessonTime(Time(8,30, AmPm.PM), Time(9,30, AmPm.PM), Days.FRI)

    section2 = Section([class4, class5, class6], "Section 2")
    #print(section2.ave_start_time)

    course1 = Course("course 1", [section1, section2])

    class7 = LessonTime(Time(10,30), Time(11,30), Days.WED)
    class8 = LessonTime(Time(2, 0, AmPm.PM), Time(3, 0, AmPm.PM), Days.THURS)
    class9 = LessonTime(Time(9), Time(10), Days.FRI)

    section3 = Section([class7, class8, class9], "Section 3")
    #print(section3.ave_start_time)

    course2 = Course("course 2", [section3, section2])
    
    query1 = Query([course1, course2], TimePreference.LATE)
    query1.show_table()
    print(query1.conflicting)
    print(query1)
    print(course1)
    print(course2)
    '''


    lessons = 3
    sections = 30
    courses = 15
    course_list = []
    for i in range(courses):
        section_list = []    
        for x in range(sections):
            lesson_list = []
            for _ in range(lessons):
                am_pm = AmPm.AM if random.randint(1,10) <= 5 else AmPm.PM
                if am_pm == AmPm.AM:
                    hour = random.randint(8,12)
                    if hour == 12:
                        am_pm = AmPm.PM # becomes noon
                else:
                    hour = random.randint(1,8)
                min = random.randrange(0,60,30)                
                day = Days(random.randint(0,4))
                lesson_list.append(LessonTime(Time(hour, min, am_pm), Time((hour+1)%12,min,am_pm if hour != 11 else AmPm.PM), day))
            section_list.append(Section(lesson_list,"Section %i"%(x)))
        rng = random.randint(1,3)
        priority = Priority.LOW if rng == 1 else Priority.MID if rng == 2 else Priority.HIGH
        course_list.append(Course("Course %i"%(i), section_list, priority))

    print("Courses: \n")
    for course in course_list:
        print(course)

    for preference in TimePreference:
        query = Query(course_list, preference)
        print("Preference = " + preference.name)
        print("missing courses: ", query.conflicting)
        query.show_table()
        #print("HERE:", query.show_table())
        print(query.get_better_dict(Time(8), Time(10,00,AmPm.PM)))
    
    
    #class1 = LessonTime(Time(8,30), Time(9,30), Days.MON)
    #class2 = LessonTime(Time(10,30), Time(11,30), Days.TUES)
    #class3 = LessonTime(Time(9,30), Time(10,30), Days.WED)
    #print(query2.get_better_dict())
        


