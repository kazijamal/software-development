// Set the dimensions and margins of the graph
const margin = { top: 50, right: 50, bottom: 50, left: 50 };
const width = 800; // Use window's width
const height = 800 - margin.top - margin.bottom; // Use window's height

d3.csv('/data/sentiment/namedentitiesfrequencies').then(
  (namedEntitiesFrequencies) => {
    const font = d3.scaleLinear().domain([0, 48000]).range([5, 120]);

    const data = [];
    for (const namedEntityFrequency in namedEntitiesFrequencies) {
      const namedEntityVal = namedEntitiesFrequencies[namedEntityFrequency];
      data.push({ ...namedEntityVal, size: font(namedEntityVal.value) });
    }

    const color = d3
      .scaleLinear()
      .domain([0, 1, 2, 3, 4, 5, 6, 10, 15, 20, 100])
      .range([
        '#ddd',
        '#ccc',
        '#bbb',
        '#aaa',
        '#999',
        '#888',
        '#777',
        '#666',
        '#555',
        '#444',
        '#333',
        '#222',
      ]);

    // Define the div for the tooltip
    const tooltip = d3.select('body').append('div').attr('class', 'toolTip');

    const draw = (words) => {
      console.log('[wordcloud.js] draw');
      d3.select('#wordcloud')
        .append('svg')
        .attr('width', 1000)
        .attr('height', 350)
        .attr('class', 'wordcloud')
        .append('g')
        // without the transform, words words would get cutoff to the left and top, they would
        // appear outside of the SVG area
        .attr('transform', 'translate(450,200)')
        .selectAll('text')
        .data(words)
        .enter()
        .append('text')
        .style('font-size', function (d) {
          return d.size + 'px';
        })
        .style('fill', function (d, i) {
          return color(i);
        })
        .attr('transform', function (d) {
          return 'translate(' + [d.x, d.y] + ')rotate(' + d.rotate + ')';
        })
        .text(function (d) {
          return d.text;
        })
        .on('mousemove', function (d) {
          tooltip
            .style('left', d3.event.pageX - 50 + 'px')
            .style('top', d3.event.pageY - 70 + 'px')
            .style('display', 'inline-block')
            .html(`Frequency of "${d.text}": ${d.value}`);
        })
        .on('mouseout', function (d) {
          tooltip.style('display', 'none');
        });
    };

    d3.layout
      .cloud()
      .size([800, 300])
      .words(data)
      .rotate(0)
      .fontSize(function (d) {
        return d.size;
      })
      .on('end', draw)
      .start();
  }
);
