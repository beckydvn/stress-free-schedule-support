// for (let i = 0; i < document.getElementById("output").length; i++) { 
//     createCourse(document.getElementById("output"));
// }

for (const [key, value] of Object.entries(document.getElementById("output"))) {
    console.log(key, value);
}

function createCourse(query) {
    const div = document.createElement('div');
    div.setAttribute('class', 'course');
    const span = document.createElement('span');
    span.innerHTML = query;

    div.appendChild(span);
    return div;
}