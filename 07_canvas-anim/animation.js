/*
Kazi Jamal and Ahmed Sultan -- Team oldfirefoxdata
SoftDev1 pd9
K07 -- They lock us in the tower whenever we get caught
2020-02-13
*/

// retrieve node in DOM via ID
const canvas = document.getElementById('playground');

// instantiate a CanvasRenderingContext2D object
const ctx = canvas.getContext('2d');

var radius = 0;
var change = 1;
var animid;
var isRunning = false;

// clears the canvas
var clearCanvas = function() {
    console.log('clearing canvas');
    ldx = -1;
    ldy = -1;
    ctx.clearRect(0, 0, canvas.width, canvas.height);
};

var start = function() {
    console.log('start')
    if (!isRunning) {
        animate();
        isRunning = true;
    };
}

var animate = function() {
    clearCanvas();
    // Starts or resets current path
    ctx.beginPath();
    ctx.fillStyle = '#ff0000';
    // Draws an arc.
    ctx.arc(300, 300, radius, 0, 2 * Math.PI);
    ctx.fill();
    // Fills the interior of the path,
    // Will not work if the path has fewer than 3 points in it.
    ctx.lineWidth = 2;
    ctx.strokeStyle = '#000000';
    // Renders all the lines in the path, does not end the path.
    ctx.stroke()
    if (radius == 150) {
	change = -1;
    } else if (radius == 0) {
	change = 1;
    };
    radius += change;
    animid = window.requestAnimationFrame(animate);
};

var stop = function() {
    console.log('stop');
    window.cancelAnimationFrame(animid);
    isRunning = false;
}

// sets event listeners for animaniac
var animaniacBtn = document.getElementById('animaniac');
animaniacBtn.addEventListener('click', start);

// sets event listeners for clear
var stopBtn = document.getElementById('stop');
stopBtn.addEventListener('click', stop);
