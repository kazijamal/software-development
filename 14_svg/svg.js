var pic = document.getElementById("vimage");
var btn = document.getElementById("clear");


var addCircle = function(e) {
    if (e.target.id == "vimage") {
	var c = document.createElementNS("http://www.w3.org/2000/svg", "circle");
	c.setAttribute( "cx", e.offsetX);
	c.setAttribute( "cy", e.offsetY);
	c.setAttribute( "r", "25");
	c.setAttribute( "fill", "red");
	//c.setAttribute( "stroke", "black" );
	pic.appendChild(c);
	c.addEventListener("click", changeColor);
	//c.addEventListener("click", e => {c.remove();});
    }
}

var changeColor = function(e) {
    const circle = e.target;
    circle.setAttributeNS(null, "fill", "green");
    circle.addEventListener("click", randomCircle);
}

var randomCircle = function(e) {
    const circle = e.target;
    circle.remove()
    var c = document.createElementNS("http://www.w3.org/2000/svg", "circle");
    c.setAttribute("cx", Math.random() * 450 + 25)
    c.setAttribute("cy", Math.random() * 450 + 25)
    c.setAttribute( "r", "25");
    c.setAttribute( "fill", "red");
    //c.setAttribute( "stroke", "black" );
    pic.appendChild(c);
    c.addEventListener("click", changeColor);
}

//pic.appendChild( c );
pic.addEventListener("click", addCircle)
btn.addEventListener("click", e => {pic.innerHTML = "";})
