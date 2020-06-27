const svg = d3
  .select('#bar-chart')
  .append('svg')
  .attr('width', '960')
  .attr('height', '600');

const margin = { top: 20, right: 20, bottom: 40, left: 40 };
const width = +svg.attr('width') - margin.left - margin.right;
const height = +svg.attr('height') - margin.top - margin.bottom;

const x = d3.scaleBand().rangeRound([0, width]).padding(0.1);
const y = d3.scaleLinear().rangeRound([height, 0]);

const g = svg
  .append('g')
  .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

const barColorInterpolator = d3
  .scaleSequential()
  .domain([-1.0, 1.0])
  .interpolator(d3.interpolateViridis);

const tooltip = d3.select('body').append('div').attr('class', 'toolTip');

d3.csv('/data/sentiment/trumptweetspolaritiesonranges')
  .then((data) => {
    return data.map((d) => {
      d.numTweets = +d.numTweets;

      return d;
    });
  })
  .then((data) => {
    x.domain(
      data.map(function (d) {
        return d.rangeBracket;
      })
    );
    y.domain([0, 600]);

    g.append('g')
      .attr('class', 'axis axis--x')
      .attr('transform', 'translate(0,' + height + ')')
      .call(d3.axisBottom(x))
      .selectAll('text')
      .style('text-anchor', 'end')
      .attr('transform', 'translate(-10,0)rotate(-45)');

    g.append('g')
      .attr('class', 'axis axis--y')
      .call(d3.axisLeft(y).ticks(10))
      .append('text')
      .attr('transform', 'rotate(-90)')
      .attr('y', 6)
      .attr('dy', '0.71em')
      .attr('text-anchor', 'end')
      .text('Frequency');

    g.selectAll('.bar')
      .data(data)
      .enter()
      .append('rect')
      .attr('class', 'bar')
      .attr('x', (d) => {
        return x(d.rangeBracket);
      })
      .attr('y', (d) => {
        return y(d.numTweets);
      })
      .attr('width', x.bandwidth())
      .attr('height', (d) => {
        return height - y(d.numTweets);
      })
      .style('fill', (d) => {
        switch (d.rangeBracket) {
          case '-1.0 to -0.8':
            return barColorInterpolator(-1.0);
          case '-0.8 to -0.6':
            return barColorInterpolator(-0.8);
          case '-0.6 to -0.4':
            return barColorInterpolator(-0.6);
          case '-0.4 to -0.2':
            return barColorInterpolator(-0.4);
          case '-0.2 to 0.0':
            return barColorInterpolator(-0.2);
          case '0.0 to 0.2':
            return barColorInterpolator(0.0);
          case '0.2 to 0.4':
            return barColorInterpolator(0.2);
          case '0.4 to 0.6':
            return barColorInterpolator(0.4);
          case '0.6 to 0.8':
            return barColorInterpolator(0.6);
          case '0.8 to 1.0':
            return barColorInterpolator(0.8);
          default:
            break;
        }
      })
      .on('mousemove', function (d) {
        tooltip
          .style('left', d3.event.pageX - 50 + 'px')
          .style('top', d3.event.pageY - 70 + 'px')
          .style('display', 'inline-block')
          .html(`Number of Tweets: ${d.numTweets}`);
      })
      .on('mouseout', function (d) {
        tooltip.style('display', 'none');
      });

    svg.attr('height', '660');
  })
  .catch((error) => {
    throw error;
  });
