// Credit: http://bl.ocks.org/michellechandra/0b2ce4923dc9b5809922 for showing how to display an interactable US map

let playing = false;

// Setup map
const setMap = (json) => {
    // Width and height of map
    const width =
        window.innerWidth ||
        document.documentElement.clientWidth || // for IE8 and earlier
        document.body.clientWidth;
    const height =
        window.innerHeight ||
        document.documentElement.clientHeight || // for IE8 and earlier
        document.body.clientHeight;

    // D3 Projection
    const projection = d3
        .geoAlbersUsa()
        .translate([width / 2, height / 3]) // translate to center of screen
        .scale([1300]); // scale things down so see entire US

    // Define path generator
    const path = d3.geoPath(projection); // path generator that will convert GeoJSON to SVG paths and tell path generator to use albersUsa projection

    // Create SVG element and append map to the SVG
    const svg = d3
        .select("#map")
        .append("svg")
        .attr("width", width)
        .attr("height", height);

    // Create paths for all states using GeoJSON data
    svg.selectAll("path")
        .data(json.features)
        .enter()
        .append("path")
        .attr("d", path)
        .attr("data-state", (d) => d.properties.name) // Associate path's custom data attribute with corresponding state
        .style("stroke", "salmon")
        .style("stroke-width", "1")
        .style("fill", () => "#fff");
};

// const drawMap = (json) => {
//   d3.csv('/static/csv/states.csv', (data) => {
//     for (let i = 0; i < 50; i++) {
//       const dataState = data[i].state;
//       console.log;
//     }
//     drawUSStatesPath(json);
//   });
// };

// Returns GeoJSON data for setMap to use
const setMapData = () => {
    const cachedUSStatesJSON = JSON.parse(localStorage.getItem("USStatesJSON"));

    if (!cachedUSStatesJSON) {
        // Load GeoJSON data and merge with states data
        d3.json("/static/json/us-states.json")
            .then((json) => {
                // Bind the data to the SVG and create one path per GeoJSON feature
                localStorage.setItem("USStatesJSON", JSON.stringify(json));
                return json;
            })
            .catch((err) => {
                console.log(err);
            });
    }
    return cachedUSStatesJSON;
};

// Initialize map setup
const init = () => {
    setMap(setMapData());
};

let delay = null;
// Load US states JSON with forwarded geocoding (latitude and longitude)
d3.csv("/static/csv/us-states-geocoded.csv")
    .then((data) => {
        // Map the domain difference between the beginning date of the dataset and the most recent date of the dataset to 20 seconds (20,000 milliseconds)
        delay = d3
            .scaleTime()
            .domain([
                new Date(data[0].date),
                new Date(data[data.length - 1].date),
            ])
            .range([0, 20000]);

        // Still need to make sense of this
        // const svg = d3.select('svg');
        // for (const d of data) {
        //   d3.timeout(() => {
        //     svg
        //       .append('circle')
        //       .attr('transform', `translate(${d})`)
        //       .attr('r', 3)
        //       .attr('fill-opacity', 1)
        //       .attr('stroke-opacity', 0)
        //       .transition()
        //       .attr('fill-opacity', 0)
        //       .attr('stroke-opacity', 1);
        //   }, delay(d.date));
        // }

        // svg
        //   .transition()
        //   .ease(d3.easeLinear)
        //   .duration(delay.range()[1])
        //   .tween('date', () => {
        //     const i = d3.interpolateDate(...delay.domain());
        //     return (t) => {
        //       return new Date(d3.timeDay(i(t)));
        //     };
        //   });
    })
    .catch((err) => {
        console.log(err);
    });

const replayHandler = () => {
    playing = true;
};

const renderBtn = document.getElementById("render-btn");
renderBtn.addEventListener("click", init);

const replayBtn = document.getElementById("replay-btn");
replayBtn.addEventListener("click", replayHandler);
