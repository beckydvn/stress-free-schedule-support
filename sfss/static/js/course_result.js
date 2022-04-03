const text = JSON.parse(document.getElementById("output").innerHTML);
const courseContainer = document.getElementById('course-container');

let course_info = {};

for (let [key, value] of Object.entries(text)) {
    for (let [key2, value2] of Object.entries(value)) {
        if (value2 != null) {
            if(key2 != "id" && key2 != "course_name")
            {
                course_info[key2.toUpperCase().replace("_", " ")] = ": " + value2.toString();
            }
            else
            {
                course_info[key2] = value2.toString();
            }
        }
    }
    courseContainer.append(createCourseContainer(courseContainer, course_info));
}

function bold(element, type) {
    const b = document.createElement('b');
    const span = document.createElement(type);
    span.innerHTML = element;
    b.appendChild(span);
    return b;
}

function createCourseContainer(overallContainer, course_info) {
    const div = document.createElement('li');
    div.setAttribute('class', 'course');

    const container = document.createElement('ul');
    container.setAttribute('class', 'course-name-container')
    const containerLi = document.createElement('li');

    //for the ID
    var value = course_info["id"];
    var boldedvalue = bold(value, 'h1');
    boldedvalue.setAttribute('align', 'center');
    containerLi.appendChild(boldedvalue);     
    const br = document.createElement('br');
    containerLi.appendChild(br);
    // for the course name
    value = course_info["course_name"];
    boldedvalue = bold(value, 'h2');
    boldedvalue.setAttribute('align', 'center');
    containerLi.appendChild(boldedvalue);     
    containerLi.appendChild(br);
    container.appendChild(containerLi);
    div.appendChild(container)

    var see_more_btn = document.createElement('button');
    see_more_btn.textContent = "see more..."
    see_more_btn.onclick=function(){showMore(overallContainer, container, course_info, see_more_btn)};
    div.append(see_more_btn);

    return div;
}

function showMore(overallContainer, container, course_info, me) {
    const info_container = document.createElement('ul');
    info_container.setAttribute('class', 'info-container');
    const div = document.createElement('li')
    for(let [key, value] of Object.entries(course_info)){
        if(key != "id" && key!= "course_name")
        {
            var boldedkey = bold(key, 'span');
            div.appendChild(boldedkey);
            var newvalue = document.createElement('span');
            newvalue.innerHTML = value;
            const br = document.createElement('br');
            div.appendChild(newvalue);
            div.appendChild(br);
        }
    }
    info_container.appendChild(div);
    container.append(info_container);
    me.remove();
    var see_less_btn = document.createElement('button');
    see_less_btn.textContent = "see less..."
    see_less_btn.onclick=function(){showLess(overallContainer, container, div, course_info, see_less_btn)};
    container.append(see_less_btn);
}

function showLess(overallContainer, container, div, course_info, see_less_btn) {
    div.remove();
    see_less_btn.remove();
    var see_more_btn = document.createElement('button');
    see_more_btn.textContent = "see more..."
    see_more_btn.onclick=function(){showMore(overallContainer, container, course_info, see_more_btn)};
    container.append(see_more_btn);    
}