
var Schedule = {
    0: ["", "", "", "", "course1", "course1", "", "", "", "", "", "", "course3", "course3"]
}
var colourOptions = ["tomato", "DodgerBlue", "rgb(146, 222, 76)", "rgb(106, 81, 255)", "rgb(255, 81, 81)", "rgb(255, 152, 77)"]
var courseColours = {}
for (Day in Schedule){
    //I value corresponds to column number 
    for (var j = 0; j < Schedule[Day].length; j++) {
        cell = Schedule[Day][j]
        if (cell != ""){
            document.getElementById("r" + j + "c" + Day).innerHTML = cell
            if (cell in courseColours){
                document.getElementById("r" + j + "c" + Day).style.backgroundColor = courseColours[cell]
            }
            else{
                //var randomColour = Math.floor(Math.random()*16777215).toString(16);
                var randomColour = colourOptions[Math.floor(Math.random() * colourOptions.length)];
                document.getElementById("r" + j + "c" + Day).style.backgroundColor = randomColour
                courseColours[cell] = randomColour
            }
        }
    } 
}
//Translate: MON = rxc0
//Tues = rxc1
//WeD = rxc2
//THURS = rxc3
//FRI = rxc4

//Rows align with time