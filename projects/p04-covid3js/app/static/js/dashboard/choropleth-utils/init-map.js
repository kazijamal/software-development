// Credits to http://bl.ocks.org/michellechandra/0b2ce4923dc9b5809922 for showing how to display an interactable US map

import { getMapData } from "./init-data.js";

// Create paths for all states using GeoJSON data
const createStatePaths = (svg, path) => {
    const json = getMapData();

    // Draw the path for each state
    svg.selectAll("path")
        .data(json.features)
        .enter()
        .append("path")
        .attr("d", path)
        .attr("data-state", (d) => d.properties.name) // Associate path's custom data attribute with corresponding state
        .attr("data-cases", 0) // Initialize all states with 0 cases
        .style("stroke", "salmon")
        .style("stroke-width", "1")
        .style("fill", "#fff");
};

// Create labels for all states
const labelStatePaths = (svg, path) => {
    const json = getMapData();

    // Initialize each state label with "0", or 0 cases of COVID-19
    svg.selectAll("text")
        .data(json.features)
        .enter()
        .append("text")
        .text("0")
        .attr("x", (d) => {
            const xCentroid = path.centroid(d)[0]; // Check for paths where their centroid is NaN (ex: Puerto Rico)
            if (Number.isNaN(xCentroid)) return; // Solves console error: <text> attribute x: Expected length, “NaN”
            return xCentroid;
        })
        .attr("y", (d) => {
            const yCentroid = path.centroid(d)[1];
            if (Number.isNaN(yCentroid)) return;
            return yCentroid;
        })
        .attr("id", (d) => d.properties.name) // Associate text's custom data attribute with corresponding state
        .style("color", "black");
};

// Setup map
const setupMap = () => {
    const width = 1010;
    const height = 600;

    const projection = d3
        .geoAlbersUsa()
        .translate([width / 2, height / 2])
        .scale([1300]);

    const path = d3.geoPath(projection);

    const svg = d3
        .select("#states-choropleth-container")
        .append("svg")
        .attr("width", width)
        .attr("height", height);

    createStatePaths(svg, path);
    labelStatePaths(svg, path);
};

export default setupMap;
