// Kazi Jamal and ray. lee. -- Team coronacation
// SoftDev1 pd9
// K13 -- Ask Circles [Change || Die]
// 2020-03-31

const pic = document.getElementById("vimage");
const clearBtn = document.getElementById("clearBtn");
const xmlns = "http://www.w3.org/2000/svg";
let onDot = false;

const createDotElement = (dotX, dotY) => {
    const dot = document.createElementNS(xmlns, "circle");
    dot.setAttributeNS(null, "cx", dotX);
    dot.setAttributeNS(null, "cy", dotY);
    dot.setAttributeNS(null, "r", 30);
    dot.setAttributeNS(null, "fill", "lightgreen");
    dot.setAttributeNS(null, "data-num-clicks", 0);
    dot.addEventListener("mouseover", () => (onDot = true));
    dot.addEventListener("mouseout", () => (onDot = false));
    dot.addEventListener("click", e => mutateDot(e));
    // console.log(dot);
    return dot;
};

const drawDot = (dotX, dotY) => {
    // console.log("draw dot");
    if (!onDot) {
	const dot = createDotElement(dotX, dotY);
	pic.appendChild(dot);
	const dotCoordsString = `${dotX},${dotY}`;
	console.log(`Drawing a circle at (${dotCoordsString})`);
    }
};

const mutateDot = event => {
    const dot = event.target;
    var numClicks = parseInt(dot.getAttributeNS(null, "data-num-clicks"));
    numClicks++;
    if (numClicks == 1) {
	dot.setAttributeNS(null, "fill", "green");
    }
    else if (numClicks == 2){ 
	pic.removeChild(dot);
	const randomX = Math.random() * 440 + 30;
	const randomY = Math.random() * 440 + 30;
	onDot = false;
	drawDot(randomX, randomY);
	// console.log("create random dot");
    };
    dot.setAttributeNS(null, "data-num-clicks", numClicks);
};

const clear = () => {
    var fc = pic.firstChild;
    while(fc) {
	console.log("removing " + fc + "...");
	pic.removeChild(fc);
	fc = pic.firstChild;
    }
    onDot = false;
};

const draw = event => {
    const mouseX = event.offsetX;
    const mouseY = event.offsetY;
    drawDot(mouseX, mouseY);
    // console.log(onDot);
};

pic.addEventListener("mousedown", draw);
clearBtn.addEventListener("click", clear);
