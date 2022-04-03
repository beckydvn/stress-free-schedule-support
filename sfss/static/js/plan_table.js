var times = ["8:00AM", "8:30AM", "9:00AM", "9:30AM", "10:00AM", "10:30AM", "11:00AM", "11:30AM", "12:00PM", "12:30PM", "1:00PM", "1:30PM", "2:00PM", "2:30PM", "3:00PM", "3:30PM", "4:00PM", "4:30PM", "5:00PM", "5:30PM", "6:00PM", "6:30PM", "7:00PM", "7:30PM", "8:00PM", "8:30PM", "9:00PM", "9:30PM", "10:00PM"]
var days = ["MON", "TUES", "WED", "THURS", "FRI"]

//var courseDict = {document.getElementById("course-container") :{document.getElementById("")}}


// instantiate first time dropdown 
let timeDropdown = document.getElementById("start0");
instantiateStartTimeDropdown(timeDropdown);

// instantiate first day dropdown 
let dayDropdown = document.getElementById("day0");
instantiateDayDropdown(dayDropdown);

function instantiateStartTimeDropdown(dropdown){
    for(let i = 0; i < times.length-1; i++) {   // times.length-1 so it only includes up to 9:30 for start times
        let opt = times[i];
        let el = document.createElement("option");
    
        el.textContent = opt;
        el.value = opt;
        dropdown.appendChild(el);
    }
}

function instantiateDayDropdown(dropdown){
    for(let i = 0; i < days.length; i++) {   // times.length-1 so it only includes up to 9:30 for start times
        let opt = days[i];
        let el = document.createElement("option");
    
        el.textContent = opt;
        el.value = opt
        dropdown.appendChild(el);
    }
}


// display endtime dropdowns once they choose a starttime
function addEndTime(startTime){
    let value = startTime.value;
    let lesson = startTime.parentNode; 
    if (!value){
        let oldChild = lesson.querySelector("#endTime");
        if (oldChild){
            lesson.removeChild(oldChild);
        }
    }
    else{
        let endTime = document.createElement("select");
        let oldChild = lesson.querySelector("#endTime");
        endTime.classList.add("select");
        endTime.setAttribute("id", "endTime");
        if (oldChild){
            lesson.replaceChild(endTime, oldChild);
        }
        else{
            lesson.appendChild(endTime);    
        }    
        let index = times.indexOf(value);
        for (let i = index+1; i < Math.min(index+7, times.length); i++){  // go up to either 3 horus away or end of list, starting from half hour away
            let opt = times[i];
            let el = document.createElement("option");

            el.textContent = opt;
            el.value = opt;
            endTime.appendChild(el);
        }
    }
}

function newCourse(courseList){
    let course = generateCourse();
    courseList.appendChild(course);
}
function newSection(sectionList){
    let section = generateSection();
    sectionList.appendChild(section);
}
function newLesson(lessonList){
    let lesson = generateLesson();
    lessonList.appendChild(lesson);
}
function killSelf(me){
    parent = me.parentNode;
    me.remove();
    if (parent.childElementCount == 0 || me.childElementCount == 0)
    {
        killSelf(parent);
    }
}

function generateCourse(){
    let course = document.createElement("li");
    course.classList.add("course");
    let xButton = document.createElement("button");
    xButton.classList.add("x-button");
    xButton.textContent="x";
    xButton.onclick=function(){killSelf(course)};
    course.appendChild(xButton);
    let courseTitle = document.createElement("h1");
    courseTitle.innerHTML = "Course";
    course.appendChild(courseTitle);
    let sectionContainer = document.createElement("ul");
    sectionContainer.classList.add("section-container");
    let section = generateSection();
    let priority = generatePriority();
    course.appendChild(priority);
    let input = document.createElement("input");
    input.classList.add("course-input");
    input.placeholder="Enter course name.";
    course.appendChild(input);
    sectionContainer.appendChild(section);
    course.appendChild(sectionContainer);
    let newSectionButton = document.createElement("button");
    newSectionButton.classList.add("new-btn");
    newSectionButton.textContent = "+ Add another section...";
    newSectionButton.onclick = function(){newSection(sectionContainer)};
    course.appendChild(newSectionButton);
    return course; 
}
function generateSection(){
    let section = document.createElement("li");
    section.classList.add("section");
    let xButton = document.createElement("button");
    xButton.classList.add("x-button");
    xButton.textContent="x";
    xButton.onclick=function(){killSelf(section)};
    section.appendChild(xButton);
    let sectionTitle = document.createElement("h2");
    sectionTitle.innerHTML = "Section";
    let lessonContainer = document.createElement("ul");
    lessonContainer.classList.add("lesson-container");
    let lesson = generateLesson();
    section.appendChild(sectionTitle);
    lessonContainer.appendChild(lesson);
    section.appendChild(lessonContainer);
    let newLessonButton = document.createElement("button");
    newLessonButton.classList.add("new-btn");
    newLessonButton.onclick = function(){newLesson(lessonContainer)};
    newLessonButton.textContent = "+ Add another lesson...";
    section.appendChild(newLessonButton);
    return section;
}
function generateLesson(){
    let lesson = document.createElement("li");
    lesson.classList.add("lesson");
    let xButton = document.createElement("button");
    xButton.classList.add("x-button");
    xButton.textContent="x";
    xButton.onclick=function(){killSelf(lesson)};
    lesson.appendChild(xButton);
    let lessonTitle = document.createElement("h3");
    lessonTitle.innerHTML = "Lesson";
    lesson.appendChild(lessonTitle);
    dayDropdown = generateDay();
    lesson.appendChild(dayDropdown);
    start = generateStart();
    lesson.appendChild(start);
    return lesson;
}
function generateStart(){
    let start = document.createElement("select");
    start.classList.add("select");
    start.onchange = function(){addEndTime(start)};
    let def = document.createElement("option");
    def.textContent = "Pick a start time...";
    def.value = "";
    start.appendChild(def);
    instantiateStartTimeDropdown(start);
    return start;
}

function generateDay(){
    let dayDropdown = document.createElement("select");
    dayDropdown.classList.add("select");
    let def = document.createElement("option");
    def.textContent = "Pick a day...";
    def.value = "";
    dayDropdown.appendChild(def);
    instantiateDayDropdown(dayDropdown);
    return dayDropdown;
}

function generatePriority(){
    let priority  = document.createElement("select");
    priority.classList.add("select");
    let high = document.createElement("option");
    high.textContent = "High";
    high.value = "high";
    let medium = document.createElement("option");
    medium.textContent = "Medium";
    medium.value = "medium";
    let low = document.createElement("option");
    low.textContent = "Low";
    low.value = "low";
    priority.appendChild(high);
    priority.appendChild(medium);
    priority.appendChild(low);
    return priority;
}

function postInfo(form){
    let courseContainer = document.getElementById("course-container");
    // all course nodes
    let courses = courseContainer.querySelectorAll(".course");
    // course list to be returned
    let courseList = Array(courses.length);
    console.log(courses);
    for (let course=0; course<courses.length; course++){
        let prio = courses[course].querySelector(".select").value;
        let priorityReturn = document.createElement("input");
        priorityReturn.value = prio;
        priorityReturn.name = "priority" + course;
        priorityReturn.setAttribute("type", "hidden");
        form.appendChild(priorityReturn);
        let coursename = courses[course].querySelector(".course-input").value;
        let nameReturn = document.createElement("input");
        nameReturn.value = coursename;
        nameReturn.name = "name" + course;
        nameReturn.setAttribute("type", "hidden");
        form.appendChild(nameReturn);
        let sectionContainer = courses[course].querySelector(".section-container");
        // all section nodes in this course
        let sections = sectionContainer.querySelectorAll(".section");
        // section list to be placed in course
        sectionList = Array(sections.length);      
        for (let section=0; section<sections.length; section++){
            let lessonContainer = sections[section].querySelector(".lesson-container");
            // all lesson nodes in this section
            let lessons = lessonContainer.querySelectorAll(".lesson");
            // lesson list to be placed in section
            lessonList = Array(lessons.length);
                for (let lesson=0; lesson<lessons.length; lesson++){
                    let dayStartEnd = lessons[lesson].querySelectorAll(".select");
                    let day = dayStartEnd[0].value;
                    let start = dayStartEnd[1].value;
                    let end = dayStartEnd[2].value;
                    let lessonTime = [day, start, end];
                    let les = document.createElement("input");
                    les.value = lessonTime
                    les.name = "course" + course + "-section" + section + "-lesson" + lesson;
                    les.setAttribute("type", "hidden");
                    form.appendChild(les);
                    // form sent as { course(i)-section(x)-lesson(z) : "day", "start", "end"}
                }
        }    
    }
    let preference = document.createElement("input");
    preference.value = "early" // change to reflect their choice when dropdown added
    preference.name = "preference";
    preference.setAttribute("type", "hidden");
    form.appendChild(preference);
}