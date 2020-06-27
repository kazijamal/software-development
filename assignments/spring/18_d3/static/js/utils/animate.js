import { getCOVIDData } from "./initData.js";

// Control the animation of the state labels and colors
const animateMap = () => {
    const data = getCOVIDData();

    // Map the domain difference between the beginning date of the dataset and the most recent date of the dataset to animation duration
    const delay = d3
        .scaleTime()
        .domain([new Date(data[0].date), new Date(data[data.length - 1].date)])
        .range([0, 10000]); // in milliseconds

    // Map the domain (COVID-19 cases) to a range of rgb values
    const stateColoring = d3
        .scaleLinear()
        .domain([0, 50000])
        .range(["white", "red"]);

    // Go through each of the datapoints in us-states-covid.csv
    for (const d of data) {
        const date = document.getElementById("date");
        const statePathElement = document.querySelector(
            `path[data-state="${d.state}"]`
        );
        const stateTextElement = document.getElementById(d.state);

        if (!date || !statePathElement || !stateTextElement) continue; // ex: Virgin Islands is not on the map so either date, statePathElement or stateTextElement would be null

        d3.timeout(() => {
            if (d.date == "2020-04-20") {
              date.textContent = `${d.date} 🥦`
            } else {
            date.textContent = d.date;
            }
            statePathElement.style.fill = stateColoring(+d.cases);
            stateTextElement.textContent = d.cases;
        }, delay(new Date(d.date))); // Like before, the date string must be wrapped in a Date object!
    }
};

export default animateMap;
