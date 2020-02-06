// Kazi Jamal
// SoftDev1 pd9
// K04 -- I See a Red Door...
// 2020-02-06

// retrieve node in DOM via ID
const canvas = document.getElementById('slate');

// instantiate a CanvasRenderingContext2D object
const ctx = canvas.getContext('2d');

var mode = "box"
var modeText = document.getElementById("mode-text");
modeText.innerHTML = "Current mode: " + mode;

var draw = function(e) {
    var rect = canvas.getBoundingClientRect();
    mouseX = e.clientX - rect.left;
    mouseY = e.clientY - rect.top;
    if (mode == "box") {
	drawBox(mouseX, mouseY);
    } else if (mode == "dot") {
	drawDot(mouseX, mouseY);
    };
};

var drawBox = function(x, y) {
    console.log("drawing box");
    fillCenteredBox(x, y, 100, "#000000");
    fillCenteredBox(x, y, 90, "#ff0000");
}

var fillCenteredBox = function(x, y, side, style) {
    var side = side;
    ctx.fillStyle = style;
    ctx.fillRect(x-(side/2), y-(side/2), side, side);
}

var drawDot = function(x,y) {
    console.log("drawing dot");
    var radius = 20;
    ctx.beginPath();
    ctx.fillStyle = "#ff0000";
    ctx.arc(x, y, radius, 0, 2 * Math.PI);
    ctx.fill();
    ctx.lineWidth = 2;
    ctx.strokeStyle = "#000000";
    ctx.stroke();
}

var clearCanvas = function() {
    console.log("clearing canvas");
    ctx.clearRect(0,0, canvas.width, canvas.height);
};

var toggleMode = function() {
    console.log("toggling mode");
    if (mode == "box") {
	mode = "dot";
    } else if (mode == "dot") {
	mode = "box";
    };
    modeText.innerHTML = "Current mode: " + mode;
};

canvas.addEventListener('click', draw);

var clearBtn = document.getElementById("clear-btn");
clearBtn.addEventListener('click', clearCanvas);

var togglemodeBtn = document.getElementById("togglemode-btn");
togglemodeBtn.addEventListener('click', toggleMode);
