const data = [4, 8, 15, 16, 23, 42];
const scale = d3.scaleLinear()
      .domain([0, d3.max(data)])
      .range([0, 420])

const createChart = function() {
  div = d3.create("div");

  // Apply some styles to the chart container.
  div.style("font", "10px sans-serif")
     .style("text-align", "right")
     .style("color", "white")
     .style("background", "white");
  // Join the selection and the data, appending the entering bars.
  barNew = div.selectAll("div")
                    .data(data)
                    .join("div")
                    .style("background", "steelblue")
                    .style("padding", "3px")
                    .style("margin", "1px")
                    .style("width", d => `${scale(d)}px`)
                    .text(d => d);
  return div.node();
}

var chart = document.getElementsByClassName("chart");
chart[0].appendChild(createChart());
