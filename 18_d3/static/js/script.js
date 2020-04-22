// App states
let renderMap = false;
let playing = false;

// Handlers
const toggleMapHandler = (event) => {
  event.preventDefault();

  if (!renderMap) {
    renderMap = true;
    setupMap();
  }
};

const startHandler = (event) => {
  event.preventDefault();

  if (renderMap && !playing) {
    playing = true;
    animateMap();
  }
};

const renderBtn = document.getElementById('render-btn');
renderBtn.addEventListener('click', toggleMapHandler);

const startBtn = document.getElementById('start-btn');
startBtn.addEventListener('click', startHandler);
