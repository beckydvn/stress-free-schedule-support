const tagContainer = document.getElementById('tag-container')
const input = document.getElementById('userInput')

let tags = [];

input.addEventListener('keyup', function(e) {
    if (e.key === 'Enter') {
        tags.push(input.value);
        addTags();
        // input.value = '';
        //var text = document.getElementById("userInput").value; 
        //var br = text + ",";
        document.getElementById("list").value = tags;
        document.getElementById("userInput").value = ""; // clear the value
    }
})

function addTags() {
    reset();
    tags.slice().reverse().forEach(function(tag) {
        const input = createTag(tag);
        tagContainer.prepend(input);
    })
}

function reset() {
    document.querySelectorAll('.tag').forEach(function(tag) {
        tag.parentElement.removeChild(tag);
    })
}

function createTag(label) {
    const div = document.createElement('div');
    div.setAttribute('class', 'tag');
    const span = document.createElement('span');
    span.innerHTML = label;
    const closeBtn = document.createElement('i');
    closeBtn.setAttribute('class', 'material-icons');
    closeBtn.setAttribute('data-item', label);
    closeBtn.innerHTML = 'close';

    div.appendChild(span);
    div.appendChild(closeBtn);
    return div;
}

document.addEventListener('click', function(e) {
    if (e.target.tagName === 'I') {
        const value = e.target.getAttribute('data-item');
        const index = tags.indexOf(value);
        tags = [...tags.slice(0, index), ...tags.slice(index + 1)];
        addTags();
        document.getElementById("list").value = tags;
    }
})

function search() {
    valid = true;

    tags.forEach(function(tag) {
        if (!validateCourse(tag)) {
            valid = false;
        };
    })

    if (valid == true) {
        searchElective();
    }
    else {
        document.getElementById('error').style.display = 'block';
    }
}

function validateCourse(subject) {
    const re = /^[A-Za-z]+$/;
    return re.test(subject);
}

function searchElective() {
    // get_query_results[tags];
}