var pic = document.getElementById("vimage");
var clearBtn = document.getElementById("clear");
var moveBtn = document.getElementById("move");
var stopBtn = document.getElementById("stop");
var xtraBtn = document.getElementById("xtra");

var createCircle = function(x, y) {
    var c = document.createElementNS("http://www.w3.org/2000/svg", "circle");
    c.setAttribute( "cx", x);
    c.setAttribute( "cy", y);
    c.setAttribute( "r", "25");
    c.setAttribute( "fill", "red");
    c.setAttribute( "x-direction", 3);
    c.setAttribute( "y-direction", 2);
    c.setAttribute( "r-change", 1);
    pic.appendChild(c);
    c.addEventListener("click", changeColor);
}

var addCircle = function(e) {
    if (e.target.id == "vimage") {
	createCircle(e.offsetX, e.offsetY);
    }
}

var changeColor = function(e) {
    const circle = e.target;
    circle.setAttribute("fill", "green");
    circle.addEventListener("click", randomCircle);
}

var randomCircle = function(e) {
    const circle = e.target;
    circle.remove()
    createCircle(Math.random() * 450 + 25, Math.random() * 450 + 25);
}

var moveRequestId;

var startMove = function(e) {
    window.cancelAnimationFrame(moveRequestId);

    circles = pic.children;
    
    for (var i = 0; i < circles.length; i++) {
	var c = circles[i];

	var cx = parseInt(c.getAttribute("cx"))
	var cy = parseInt(c.getAttribute("cy"))

	if (cx > 475 || cx < 25) {
	    c.setAttribute("x-direction", parseInt(c.getAttribute("x-direction")) * -1)
	}
	
	if (cy > 475 || cy < 25) {
	    c.setAttribute("y-direction", parseInt(c.getAttribute("y-direction")) * -1)
	}
	
	c.setAttribute("cx", parseInt(c.getAttribute("cx")) + parseInt(c.getAttribute("x-direction")));
	c.setAttribute("cy", parseInt(c.getAttribute("cy")) + parseInt(c.getAttribute("y-direction")));
    }

    moveRequestId = window.requestAnimationFrame(startMove);
}

var sizeRequestId;

var startSize = function(e) {
    window.cancelAnimationFrame(sizeRequestId);

    circles = pic.children;
    
    for (var i = 0; i < circles.length; i++) {
	var c = circles[i];
	var r = parseInt(c.getAttribute("r"));

	if (r == 100) {
	    c.setAttribute("r-change", -1);
	}

	if (r == 0) {
	    c.setAttribute("r-change", 1);
	}
	
	c.setAttribute("r", r + parseInt(c.getAttribute("r-change")));
    }

    sizeRequestId = window.requestAnimationFrame(startSize);
}

var stopMove = function(e) {
    window.cancelAnimationFrame(moveRequestId);
    window.cancelAnimationFrame(sizeRequestId);
}

pic.addEventListener("click", addCircle);
clearBtn.addEventListener("click", e => {pic.innerHTML = "";});
moveBtn.addEventListener("click", startMove);
stopBtn.addEventListener("click", stopMove);
xtraBtn.addEventListener("click", startSize);
