//const text = document.getElementById("output").innerHTML
//document.getElementById("test").innerHTML = text;
//const jsonData= require('../../../output.json'); 

const text = JSON.parse(document.getElementById("output").innerHTML);

for (let [key, value] of Object.entries(text)) {
    console.log(key, value);
}
document.getElementById("test").innerHTML = text;

//createCourse(text[0]);

// const jsonData= require('../output.json'); 
// document.getElementById("test").innerHTML = "test2";

function createCourse(query) {
    const div = document.createElement('div');
    div.setAttribute('class', 'course');
    const span = document.createElement('span');
    span.innerHTML = query;

    div.appendChild(span);
    return div;
}