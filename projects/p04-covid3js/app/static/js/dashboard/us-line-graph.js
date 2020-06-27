import LineGraph from "../template/line.graph.js";

window.onload = async () => {
    await uslinegraph();
};

let uslinegraph = async () => {
    let data = await d3.csv("/data/dashboard/us");

    let minDate = new Date(`${data[0]["date"]}T00:00:00`);
    let maxDate = new Date(`${data[data.length - 1]["date"]}T00:00:00`);

    let cases = {
        name: "cases",
        values: [],
    };

    let deaths = {
        name: "deaths",
        values: [],
    };

    for (let i = 0; i < data.length; i++) {
        cases["values"].push(+data[i]["cases"]);
        deaths["values"].push(+data[i]["deaths"]);
    }

    let svg = d3
        .select("#us-line-container")
        .append("svg")
        .attr("id", "us-line-graph")
        .attr("width", "100%")
        .attr("height", "50vh");

    let margin = { top: 50, right: 50, bottom: 50, left: 100 };

    let usline = new LineGraph(
        svg,
        [cases, deaths],
        "date",
        "people",
        "",
        margin,
        "us-line",
        "date-x",
        "people-y",
        { strokewidth: 4 }
    );

    await usline.renderMultiLine([minDate, maxDate], {
        cases: "#2315ba",
        deaths: "#911111",
    });

    usline.yLabel('# of people');

    let legend = svg
        .append('g')
        .attr('transform', 'translate(100, 100)')

    legend.append("circle")
        .attr("cx", 70)
        .attr("cy", 30)
        .attr("r", 6)
        .style("fill", "#2315ba")

    legend.append("text")
        .attr("x", 90)
        .attr("y", 30)
        .text("cases")
        .style("font-size", "15px")
        .attr("alignment-baseline", "middle")


    legend.append("circle")
        .attr("cx", 70)
        .attr("cy", 60)
        .attr("r", 6)
        .style("fill", "#911111")

    legend.append("text")
        .attr("x", 90)
        .attr("y", 60)
        .text("deaths")
        .style("font-size", "15px")
        .attr("alignment-baseline", "middle")
};