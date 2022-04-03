/**
 * These are the inputs this file manages:
 * 
 * A 2d array corresponding to the generated schedule
 * a nested list of the courses in conflict
 * 
 */

var Session = false

var Schedule1 = {0: ['', '', '', '', '', 'Course 4', 'Course 4', 'Course 4', '', '', 'Course 3', 'Course 3', 'Course 3', '', '', '', '', '', '', 'Course 1', 'Course 1', 'Course 1', '', '', '', '', '', ''], 
1: ['', '', '', '', '', '', 'Course 0', 'Course 0', 'Course 0', 'Course 0', 'Course 0', 'Course 0', 'Course 0', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''], 
2: ['', '', '', '', '', '', '', '', '', '', '', '', 'Course 1', 'Course 1', 'Course 1', '', 'Course 2', 'Course 2', 'Course 2', '', '', '', 'Course 1', 'Course 1', 'Course 1', '', '', ''], 
3: ['Course 2', 'Course 2', 'Course 2', 'Course 3', 'Course 3', 'Course 3', 'Course 4', 'Course 4', 'Course 4', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''], 
4: ['', '', '', '', '', 'Course 2', 'Course 2', 'Course 2', '', '', '', 'Course 3', 'Course 3', 'Course 3', '', '', 'Course 4', 'Course 4', 'Course 4', '', '', '', '', '', '', '', '', '']
}

var Schedule2 = {0: ['', '', '', '', '', '', '', '', '', '', 'Course A', 'Course A', 'Course A', '', '', '', '', '', '', 'Course C', 'Course C', 'Course C', '', '', '', '', '', ''], 
1: ['', '', '', '', '', '', 'Course B', 'Course B', 'Course B', '', '', '', '', 'Course C', 'Course C', '', '', '', 'Course A', 'Course A', 'Course A', '', '', '', '', '', '', ''], 
2: ['', '', 'Course D', 'Course D', 'Course D', '', '', '', '', '', '', '', '', '', '', '', 'Course C', 'Course C', 'Course C', '', '', '', '', '', 'Course E', 'Course E', '', ''], 
3: ['Course C', 'Course C', 'Course C', 'Course A', 'Course A', 'Course A', 'Course E', 'Course E', 'Course E', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''], 
4: ['', '', '', '', '', 'Course C', 'Course C', 'Course C', '', '', '', 'Course A', 'Course A', 'Course A', '', '', 'Course E', 'Course E', 'Course E', '', '', '', '', '', '', '', '', '']
}
//var colourOptions = ["tomato", "DodgerBlue", "rgb(146, 222, 76)", "rgb(106, 81, 255)", "rgb(255, 81, 81)", "rgb(255, 152, 77)"]
//var colourOptions = ["rgb(204, 237, 228)", "rgb(166, 210, 225)", "rgb(168, 166, 219)", "rgb(211, 186, 233)", "rgb(243, 208, 245)", "rgb(255, 231, 247)"] //Light Pastels
//var colourOptions = ["rgb(197, 232, 180)", "rgb(250, 243, 211)", "rgb(117, 207, 224)", "rgb(248, 204, 222)", "rgb(211, 197, 242)", "rgb(167, 187, 225)"]
//Pastel Rainbow https://www.schemecolor.com/house-party.php 

/** Testing Code as an intermediate apllication of fucntions */


var conflicts = [["Course 1", "Course 2"], ["Course 4", "Course 2"]]
getConflicts(conflicts)
generateTable(Schedule1)


/**End of testing code */


function getConflicts(conflict_list){ //Has to be a list of lists
    if (conflict_list.length > 0){
        var elem = document.getElementById("noConflicts")
        elem.parentNode.removeChild(elem);
        for (conflict in conflict_list){
            var node = document.createElement('li');
            messageString = "There was a conflict between these courses: " + conflict_list[conflict][0] + ', ' + conflict_list[conflict][1]
            node.appendChild(document.createTextNode(messageString));
            document.querySelector('ul').appendChild(node);

        }

    }
}

function generateTable(Schedule){

    var colourOptions = ["rgb(240, 119, 105)", "rgb(255, 189, 102)", "rgb(255, 244, 133)", "rgb(178, 230, 240)", "rgb(147, 171, 234)", "rgb(142, 118, 214)"]
    var courseColours = {} 

    for (Day in Schedule){
        var rowspan = 1
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
                        var colourIndex = Math.floor(Math.random() * colourOptions.length)
                        var randomColour = colourOptions[colourIndex];
                        document.getElementById("r" + j + "c" + Day).style.backgroundColor = randomColour
                        colourOptions.splice(colourIndex, 1); 
                        courseColours[cell] = randomColour
                    }
                }

            }
        } 
    }
}