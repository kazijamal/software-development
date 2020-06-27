let view = 'daily';

import LineGraph from '../template/line.graph.js';

import { tooldate, getData } from '../utility.js';

let svg;

window.onload = async () => {
  let tool = (x, y) =>
    `${y} articles \n${x.toLocaleString(undefined, tooldate)}`;

  let data = await d3.csv('/data/sentiment/publicmedia');

  const { daily, weekly, monthly } = getData(
    data,
    5,
    4,
    'numArticles',
    'numArticles'
  );

  svg = d3
    .select('#line-chart')
    .append('svg')
    .attr('id', 'line')
    .attr('width', '100%')
    .attr('height', '50vh');

  let margin = { top: 50, right: 50, bottom: 50, left: 50 };

  let linegraph = new LineGraph(
    svg,
    daily,
    'date',
    'numArticles',
    tool,
    margin,
    'num-articles-line',
    'articles-x',
    'articles-y',
    {
      color: '#ffab00',
      strokewidth: 3,
    }
  );

  await linegraph.renderLineGraph();

  listen(linegraph, 'toggle-daily-view', daily);
  listen(linegraph, 'toggle-weekly-view', weekly);
  listen(linegraph, 'toggle-monthly-view', monthly);
};

let listen = (graph, id, data) => {
  let button = document.getElementById(id);
  button.disabled = false;
  button.addEventListener('click', () => {
    update(graph, id, data);
  });
};

let update = (graph, id, data) => {
  if (view !== id) {
    view = id;
    graph.updateLineGraph(data, 1000);
  }
};
