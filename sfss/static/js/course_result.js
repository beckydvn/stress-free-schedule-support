for (let i = 0; i < document.getElementById("output").length; i++) { 
    print(i)
    createCourse(document.getElementById("output")[i]);
}

function createCourse(query) {
    const div = document.createElement('div');
    div.setAttribute('class', 'course');
    const span = document.createElement('span');
    span.innerHTML = query;

    div.appendChild(span);
    return div;
}