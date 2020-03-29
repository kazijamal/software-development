const pic = document.getElementById("vimage");
const clearBtn = document.getElementById("clearBtn");
const xmlns = "http://www.w3.org/2000/svg";
var firstClick = true;
var lastClickCoords = {
    x: null,
    y: null
};

var draw = function(event) {
    const mouseX = event.offsetX;
    const mouseY = event.offsetY;
    const mouseCoordsString = `${mouseX},${mouseY}`;
    console.log(`Drawing a circle at (${mouseCoordsString})`);
    const dot = document.createElementNS(xmlns, "circle");
    dot.setAttribute("cx", mouseX);
    dot.setAttribute("cy", mouseY);
    dot.setAttribute("r", 10);
    dot.setAttribute("fill", "lightgreen");
    pic.appendChild(dot);
    if (!firstClick) {
	const line = document.createElementNS(xmlns, "line");
	line.setAttribute("x1", lastClickCoords.x)
	line.setAttribute("y1", lastClickCoords.y)
	line.setAttribute("x2", mouseX)
	line.setAttribute("y2", mouseY)
	line.setAttribute("stroke", "black")
	pic.appendChild(line);
    }
    lastClickCoords.x = mouseX
    lastClickCoords.y = mouseY
    if (firstClick) {
	firstClick = false;
    };
};

var clear = function(event) {
    event.preventDefault();
    console.log("Clearing svg");
    const blank = document.createElementNS(xmlns, "rect")
    blank.setAttribute("height", 500);
    blank.setAttribute("width", 500);
    blank.setAttribute("fill", "white");
    pic.appendChild(blank);
    firstClick = true;
}

pic.addEventListener("mousedown", draw);
clearBtn.addEventListener("click", clear);
