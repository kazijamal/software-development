import cacheData from "./cache.js";

// Returns GeoJSON data
const getMapData = () => {
	return JSON.parse(localStorage.getItem("USStatesJSON"));
};

// Returns the COVID-19 data
const getCOVIDData = async () => {
    // return JSON.parse(localStorage.getItem("USStatesCOVIDCSV"));
	return await d3.csv("/data/dashboard/states");
};

// Initialize data caching
cacheData("USStatesJSON", "/static/json/us_states.json", "JSON");
// cacheData("USStatesCOVIDCSV", "/data/dashboard/states", "CSV");

export { getMapData, getCOVIDData };
