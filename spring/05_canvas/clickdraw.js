// Kevin Cai and Kazi Jamal -- Team Koding Kings
// SoftDev1 pd9
// K05 -- ...and I want to Paint It Better
// 2020-02-07

// retrieve node in DOM via ID
const canvas = document.getElementById('slate');

// instantiate a CanvasRenderingContext2D object
const ctx = canvas.getContext('2d');

// displays current mode
var mode = "box"
var modeText = document.getElementById("mode-text");
modeText.innerHTML = "Current mode: " + mode;

// draws box or dot when canvas clicked
var draw = function(e) {
    // the offset in the X coordinate of the mouse pointer between that event and the padding edge of the target node
    mouseX = e.offsetX;
    // the offset in the Y coordinate of the mouse pointer between that event and the padding edge of the target node
    mouseY = e.offsetY;
    if (mode == "box") {
	drawBox(mouseX, mouseY);
    } else if (mode == "dot") {
	drawDot(mouseX, mouseY);
    };
};

// draws a box with upper left corner at mouse location
var drawBox = function(x, y) {
    console.log("drawing box");
    ctx.fillStyle = "#ff0000";
    ctx.strokeStyle = "#000000";
    ctx.lineWidth = 5;
    ctx.fillRect(x, y, 100, 100);
    ctx.strokeRect(x, y, 100, 100);
}

// draws a dot with center at mouse location
var drawDot = function(x,y) {
    console.log("drawing dot");
    var radius = 20;
    // starts a new path by emptying the list of sub-paths
    ctx.beginPath();
    ctx.fillStyle = "#ff0000";
    ctx.arc(x, y, radius, 0, 2 * Math.PI);
    ctx.fill();
    ctx.lineWidth = 2;
    ctx.strokeStyle = "#000000";
    ctx.stroke();
}

// clears the canvas
var clearCanvas = function() {
    console.log("clearing canvas");
    ctx.clearRect(0,0, canvas.width, canvas.height);
};

// toggles mode between box and dot
var toggleMode = function() {
    console.log("toggling mode");
    if (mode == "box") {
	mode = "dot";
    } else if (mode == "dot") {
	mode = "box";
    };
    modeText.innerHTML = "Current mode: " + mode;
};

// sets event listener for canvas click
canvas.addEventListener('click', draw);

// sets event listeners for clear and toggle mode buttons
var clearBtn = document.getElementById("clear-btn");
clearBtn.addEventListener('click', clearCanvas);

var togglemodeBtn = document.getElementById("togglemode-btn");
togglemodeBtn.addEventListener('click', toggleMode);
