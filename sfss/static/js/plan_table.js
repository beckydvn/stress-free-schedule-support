var select = document.getElementById("start0");
var times = ["8:00AM", "8:30AM", "9:00AM", "9:30AM", "10:00AM", "10:30AM", "11:00AM", "11:30AM", "12:00PM", "12:30PM", "1:00PM", "1:30PM", "2:00PM", "2:30PM", "3:00PM", "3:30PM", "4:00PM", "4:30PM", "5:00PM", "5:30PM", "6:00PM", "6:30PM", "7:00PM", "7:30PM", "8:00PM", "8:30PM", "9:00PM", "9:30PM", "10:00PM"]


for(let i = 0; i < times.length-1; i++) {   // times.length-1 so it only includes up to 9:30 for start times
    let opt = times[i];
    let el = document.createElement("option");

    el.textContent = opt;
    el.value = opt
    select.appendChild(el);
}

// display endtime dropdowns once they choose a starttime
function startChosen(parentid, value){
    lesson = document.getElementById(parentid);
    endTime = document.createElement("select");
    let oldChild = lesson.querySelector("#endTime");
    endTime.classList.add("select");
    endTime.setAttribute("id", "endTime");
    console.log(oldChild);
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

function newLesson(parentid){

}