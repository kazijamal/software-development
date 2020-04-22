// Returns GeoJSON data
const getMapData = () => {
  return JSON.parse(localStorage.getItem('USStatesJSON'));
};

// Returns the COVID-19 data
const getCOVIDData = () => {
  return JSON.parse(localStorage.getItem('USStatesCOVIDCSV'));
};

// Initialize data caching
cacheData('USStatesJSON', '/static/json/us-states.json', 'JSON');
cacheData('USStatesCOVIDCSV', '/static/csv/us-states-covid.csv', 'CSV');
