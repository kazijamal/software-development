import animateMap from "./choropleth-utils/animate.js";
import setupMap from "./choropleth-utils/init-map.js";

setupMap();

let playing = false;

const startHandler = (event) => {
    event.preventDefault();

    if (!playing) {
        playing = true;
        animateMap();
    }
};

const startBtn = document.getElementById("start-btn");
startBtn.addEventListener("click", startHandler);