/*
Kevin Cai and Kazi Jamal -- Team Koding Kings
SoftDev1 pd9
K06 -- Dot Dot Dot
2020-02-11
*/

// retrieve node in DOM via ID
const canvas = document.getElementById('playground');

// instantiate a CanvasRenderingContext2D object
const ctx = canvas.getContext('2d');

ldx = -1;
ldy = -1;

// draws box or dot when canvas clicked
var draw = function(e) {
    // the offset in the X coordinate of the mouse pointer between that event and the padding edge of the target node
    mouseX = e.offsetX;
    // the offset in the Y coordinate of the mouse pointer between that event and the padding edge of the target node
    mouseY = e.offsetY;
    m = Math.sqrt(
        (mouseY - ldy) * (mouseY - ldy) + (mouseX - ldx) * (mouseX - ldx)
    );
    dx = ((mouseX - ldx) / m) * 5;
    dy = ((mouseY - ldy) / m) * 5;
    if (ldx != -1) {
        line(ldx + dx, ldy + dy, mouseX, mouseY);
    }
    drawDot(mouseX, mouseY);
    ldx = mouseX;
    ldy = mouseY;
};

var line = function(x0, y0, x1, y1) {
    // Starts or resets current path
    ctx.beginPath();
    // Moves path to position (x, y)
    // Does not result in a line or a filled in section
    ctx.moveTo(x0, y0);
    // Moves path to position (x, y)
    // will result in a line and a filled in section
    ctx.lineTo(x1, y1);
    // Renders all the lines in the path, does not end the path.
    ctx.stroke();
    // Results in a line from current position to start pos
    // Path can be continued after
    ctx.closePath();
};
// draws a dot with center at mouse location
var drawDot = function(x, y) {
    console.log('drawing dot');
    var radius = 5;
    // Starts or resets current path
    ctx.beginPath();
    ctx.fillStyle = '#ff0000';
    // Draws an arc.
    ctx.arc(x, y, radius, 0, 2 * Math.PI);
    ctx.fill();
    // Fills the interior of the path,
    // Will not work if the path has fewer than 3 points in it.
    ctx.lineWidth = 2;
    ctx.strokeStyle = '#000000';
    // Renders all the lines in the path, does not end the path.
    ctx.stroke();
};

// clears the canvas
var clearCanvas = function() {
    console.log('clearing canvas');
    ldx = -1;
    ldy = -1;
    ctx.clearRect(0, 0, canvas.width, canvas.height);
};

// sets event listener for canvas click
canvas.addEventListener('click', draw);

// sets event listeners for clear
var clearBtn = document.getElementById('clear');
clearBtn.addEventListener('click', clearCanvas);
