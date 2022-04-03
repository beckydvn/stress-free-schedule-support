const text = JSON.parse(document.getElementById("output").innerHTML);
const courseContainer = document.getElementById('course-container');

// let course_info = [];
let course_info = {};



for (let [key, value] of Object.entries(text)) {
    // var next = new String();
    course_info = [];
    for (let [key2, value2] of Object.entries(value)) {
        if (value2 != null) {
            course_info[key2] = ": " + value2.toString();
            // course_info(": " + value2.toString());
            console.log(course_info);
        }
    }
    courseContainer.append(createCourse(course_info));
}

function bold(element) {
    const b = document.createElement('b');
    const span = document.createElement('span')
    span.innerHTML = element;
    b.appendChild(span);
    return b;
}

function createCourse(course_info) {
    const div = document.createElement('li');
    div.setAttribute('class', 'course');

    for(let [key, value] of Object.entries(course_info)){
        const boldedkey = bold(key);
        const newvalue = document.createElement('span');
        const br = document.createElement('br');
        newvalue.innerHTML = value;
        div.appendChild(boldedkey);
        div.appendChild(newvalue);
        div.appendChild(br);
    }
    return div;
}