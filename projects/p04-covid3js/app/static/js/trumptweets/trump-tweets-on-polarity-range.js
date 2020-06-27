// Credits to https://bl.ocks.org/gordlea/27370d1eea8464b04538e6d8ced39e89 for showing how to create a line chart in d3.js v5

// Set the dimensions and margins of the graph
const margin = { top: 50, right: 50, bottom: 50, left: 50 };
const width = 800; // Use window's width
const height = window.innerHeight - margin.top - margin.bottom; // Use window's height

// TODO: extract numDatapoints dynamically
const numDatapoints = 1379;

// X scale maps the index of our data to the width of the graph
const xScale = d3
  .scaleLinear()
  .domain([0, numDatapoints - 1])
  .range([0, width]);

const pseudoXScale = d3
  .scaleTime()
  .domain([new Date('January 1, 2020'), new Date('April 15, 2020')])
  .range([0, width]);

// Y scale maps the polarity range [-1.0,1.0] to the height of the graph
// TODO: extract upper bound dynamically
const yScale = d3.scaleLinear().domain([-1, 1]).range([height, 0]);

// d3's line generator
const line = d3
  .line()
  .x((_, i) => xScale(i)) // Set x values for the line generator
  .y((d) => yScale(d.polarity)) // Set y values for the line generator
  .curve(d3.curveMonotoneX); // Apply smoothing to the curve

// Append the SVG object to the body of the page
const svg = d3
  .select('#scatterplot')
  .append('svg')
  .attr('width', 900)
  .attr('height', height + margin.top + margin.bottom)
  .append('g')
  .attr('transform', `translate(${margin.left}, ${margin.top})`)
  .attr('width', 900)
  .attr('height', height + margin.top + margin.bottom);

const numArticlesPerDay = {};

const dotColorInterpolator = d3
  .scaleSequential()
  .domain([-1.0, 1.0])
  .interpolator(d3.interpolateViridis);

// Define the div for the tooltip
const tooltip = d3.select('body').append('div').attr('class', 'toolTip');

// Read the data
// TODO: Split this chunk into smaller, intentional pieces
d3.csv('/data/sentiment/trumptweetspolarities')
  .then((numArticles) => {
    for (const day in numArticles) {
      numArticlesPerDay[day] = numArticles[day];
    }
    const numArticlesPerDayData = d3
      .range(numDatapoints)
      .map((d) => ({ polarity: +numArticlesPerDay[d].polarity }));

    // Call the x-axis in a group tag
    svg
      .append('g')
      .attr('class', 'x-axis')
      .attr('transform', `translate(0, ${height})`)
      .call(
        d3
          .axisBottom(pseudoXScale)
          .ticks(4)
          .tickFormat(d3.timeFormat('%B %d, %Y'))
      ); // Create an x-axis component with d3.axisBottom

    // Call the y-axis in a group tag
    svg.append('g').attr('class', 'y-axis').call(d3.axisLeft(yScale)); // Create a y-axis component with d3.axisLeft

    // Append a circle for each datapoint
    svg
      .selectAll('.dot')
      .data(numArticlesPerDayData)
      .enter()
      .append('circle')
      .attr('class', 'dot')
      .attr('cx', (_, i) => xScale(i))
      .attr('cy', (d) => yScale(d.polarity))
      .attr('r', 5)
      .attr('fill', (d) => dotColorInterpolator(d.polarity))
      .on('mousemove', function (d) {
        tooltip
          .style('left', d3.event.pageX - 50 + 'px')
          .style('top', d3.event.pageY - 70 + 'px')
          .style('display', 'inline-block')
          .html(`Polarity: ${d.polarity}`);
      })
      .on('mouseout', function (d) {
        tooltip.style('display', 'none');
      });
  })
  .catch((err) => console.log(err));
