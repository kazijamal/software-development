// data from https://github.com/nytimes/covid-19-data

var chart = document.getElementById("chart");
var rendered = false;

const parseData = async function() {
    return await d3.csv("/static/csv/us-states-coviid.csv", function(d) {
        return {
            date: d.date,
            state: d.state,
            cases: +d.cases,
            deaths: +d.deaths
        };
    });
};

const parseLatestData = async function() {
    return await d3.csv("/static/csv/us-states-covid.csv", function(d) {
        if (d.date == '2020-04-15') {
            return {
                date: d.date,
                state: d.state,
                cases: +d.cases,
                deaths: +d.deaths
            };
        };
    });
};


const renderData = async function() {
    console.log('rendering data');
    let data = await parseLatestData();
    var states = new Set(data.map(d => d.state));

    scale = d3.scaleLinear().domain([0, d3.max(data)]).range([0, 420])

    const div = d3.create("div")
        .style("font", "10px sans-serif")
        .style("text-align", "right")
        .style("color", "white");

    div.selectAll("div")
        .data(data)
        .join("div")
        .style("background", "steelblue")
        .style("padding", "3px")
        .style("margin", "1px")
        .style("width", d => `${scale(d.deaths)}px`)
        .text(d => d.deaths);

    if (!rendered) {
        chart.appendChild(div.node());
        rendered = true
    }
};

var renderButton = document.getElementById('render-btn');
renderButton.addEventListener('click', renderData);