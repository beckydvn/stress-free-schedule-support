//const text = document.getElementById("output").innerHTML
//document.getElementById("test").innerHTML = text;
//const jsonData= require('../../../output.json'); 

const text = JSON.parse(document.getElementById("output").innerHTML);
const courseContainer = document.getElementById('course-container');
for (let [key, value] of Object.entries(text)) {
    for (let [key2, value2] of Object.entries(value)) {
        console.log(value2);
        courseContainer.append(createCourse(value2))
    }
}
//document.getElementById("test").innerHTML = text;

//createCourse(text[0]);

// const jsonData= require('../output.json'); 
// document.getElementById("test").innerHTML = "test2";

function createCourse(query) {
    const div = document.createElement('li');
    div.setAttribute('class', 'course');
    const span = document.createElement('span');
    span.innerHTML = query;

    div.appendChild(span);
    return div;
}