// Credit: http://bl.ocks.org/michellechandra/0b2ce4923dc9b5809922 for showing how to display an interactable US map

let renderMap = false;
let playing = false;

// Setup map
const setMap = (json) => {
  // Width and height of map
  const width = 1200;
  const height = 600;

  // D3 Projection
  const projection = d3
    .geoAlbersUsa()
    .translate([width / 2, height / 2]) // translate to center of screen
    .scale([1300]); // scale things down so see entire US

  // Define path generator
  const path = d3.geoPath(projection); // path generator that will convert GeoJSON to SVG paths and tell path generator to use albersUsa projection

  // Create SVG element and append map to the SVG
  const svg = d3
    .select('#map')
    .append('svg')
    .attr('width', width)
    .attr('height', height);

  // Create paths for all states using GeoJSON data
  svg
    .selectAll('path')
    .data(json.features)
    .enter()
    .append('path')
    .attr('d', path)
    .attr('data-state', (d) => d.properties.name) // Associate path's custom data attribute with corresponding state
    .attr('data-cases', 0) // Initialize all states with 0 cases
    .style('stroke', 'salmon')
    .style('stroke-width', '1')
    .style('fill', '#fff');

  // Create labels for all states
  svg
    .selectAll('text')
    .data(json.features)
    .enter()
    .append('text')
    .text('0')
    .attr('x', (d) => path.centroid(d)[0])
    .attr('y', (d) => path.centroid(d)[1])
    .attr('id', (d) => d.properties.name) // Associate text's custom data attribute with corresponding state
    .style('color', 'black');
};

// Returns GeoJSON data for setMap to use
const setMapData = () => {
  const cachedUSStatesJSON = JSON.parse(localStorage.getItem('USStatesJSON'));

  if (!cachedUSStatesJSON) {
    // Load GeoJSON data and merge with states data
    d3.json('/static/json/us-states.json')
      .then((json) => {
        // Bind the data to the SVG and create one path per GeoJSON feature
        localStorage.setItem('USStatesJSON', JSON.stringify(json));
        return json;
      })
      .catch((err) => {
        console.log(err);
      });
  }
  return cachedUSStatesJSON;
};

// Control the animation of the state labels and colors
const animateMap = () => {
  // Load US states JSON with forwarded geocoding (latitude and longitude)
  d3.csv('/static/csv/us-states-covid.csv')
    .then((data) => {
      // Map the domain difference between the beginning date of the dataset and the most recent date of the dataset to 20 seconds (20,000 milliseconds)
      const delay = d3
        .scaleTime()
        .domain([new Date(data[0].date), new Date(data[data.length - 1].date)])
        .range([0, 20000]);
      const stateColoring = d3
        .scaleLinear()
        .domain([0, 50000 ])
        .range(['white', 'red']);
      // console.log(stateColoring(242817));
      for (const d of data) {
        const date = document.getElementById('date');
        const statePathElement = document.querySelector(
          `path[data-state="${d.state}"]`
        );
        const stateTextElement = document.getElementById(d.state);
        if (!date || !stateTextElement) continue; // ex: Virgin Islands is not on the map so either date or stateTextElement would be null
        d3.timeout(() => {
          // console.log(delay(new Date(d.date)));
          date.textContent = d.date;
          statePathElement.style.fill = stateColoring(+d.cases);
          stateTextElement.textContent = d.cases;
        }, delay(new Date(d.date))); // Like before, the date string must be wrapped in a Date object!
      }
    })
    .catch((err) => {
      console.log(err);
    });
};

// Initialize map setup
const init = () => {
  setMap(setMapData());
};

const toggleMapHandler = (event) => {
  renderMap = !renderMap;
  event.preventDefault();
  if (renderMap) {
    init();
  } else {
    const el = document.getElementById('map');
    while (el.firstChild) el.removeChild(el.firstChild);
    const date = document.getElementById('date');
    date.textContent = '2020-01-21';
    playing = false;
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
