
var Schedule = {0: ['', '', '', '', '', 'Course 4', 'Course 4', 'Course 4', '', '', 'Course 3', 'Course 3', 'Course 3', '', '', '', '', '', '', 'Course 1', 'Course 1', 'Course 1', '', '', '', '', '', ''], 
1: ['', '', '', '', '', '', 'Course 0', 'Course 0', 'Course 0', 'Course 0', 'Course 0', 'Course 0', 'Course 0', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''], 
2: ['', '', '', '', '', '', '', '', '', '', '', '', 'Course 1', 'Course 1', 'Course 1', '', 'Course 2', 'Course 2', 'Course 2', '', '', '', 'Course 1', 'Course 1', 'Course 1', '', '', ''], 
3: ['Course 2', 'Course 2', 'Course 2', 'Course 3', 'Course 3', 'Course 3', 'Course 4', 'Course 4', 'Course 4', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''], 
4: ['', '', '', '', '', 'Course 2', 'Course 2', 'Course 2', '', '', '', 'Course 3', 'Course 3', 'Course 3', '', '', 'Course 4', 'Course 4', 'Course 4', '', '', '', '', '', '', '', '', '']
}
var colourOptions = ["tomato", "DodgerBlue", "rgb(146, 222, 76)", "rgb(106, 81, 255)", "rgb(255, 81, 81)", "rgb(255, 152, 77)"]
var courseColours = {} 

for (Day in Schedule){
    var rowspan = 1
    var courseTracking = "None"
    var cellToStartMerge = ["None", "None"] //The row and column of the starting cell [j, Day]
    var courseIndex = "None" //[index of last cell with course, the course name]
    var currCourse = "None"
    //I value corresponds to column number 
    for (var j = 0; j < Schedule[Day].length; j++) {
        cell = Schedule[Day][j]
 
        if (cell != currCourse && rowspan > 1){
            var stringSpan = rowspan.toString(10)
            document.getElementById("r" +cellToStartMerge[0] + "c" + cellToStartMerge[1]).setAttribute("rowspan", stringSpan)
            rowspan = 1
        }

        if (cell != ""){
            if ((cell == currCourse) && (courseIndex == j-1)){
                rowspan += 1
                courseIndex = j
                //var row = document.getElementById("r"+j);
                //row.deleteCell(Day+1);
                document.getElementById("r" + j + "c" + Day).style.display= 'none';
            }
            else{
                cellToStartMerge = [j, Day]
                courseIndex = j
                currCourse = cell
                document.getElementById("r" + j + "c" + Day).innerHTML = cell //Add our current cell
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
}

/*
for (Day in Schedule){
    //I value corresponds to column number 
    for (var j = 0; j < Schedule[Day].length; j++) {
        cell = Schedule[Day][j]
        rowspan = 1
        courseTracking = "None"
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
*/

//Translate: MON = rxc0
//Tues = rxc1
//WeD = rxc2
//THURS = rxc3
//FRI = rxc4

//Rows align with time