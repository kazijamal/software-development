import LineGraph from '../../template/line.graph.js';
import Choropleth from '../../template/choropleth.js';

import {
    dayaverage,
    boroughParse,
    percentChange,
    stopdrop
} from '../data/mta.ridership.js';

import {
    parseData,
    setDate,
    tooldate,
    getData,
    average,
    delay
} from '../../utility.js';

import {
    borodata,
    zipdata
} from '../data/nyc.corona.js';

let view = 'daily';
let choroview = 'borough';
let checked = false;
let svg, margin;
let ridership, gextent, tool;
let projection = d3.geoMercator()
    .scale(70000)
    .center([-73.94, 40.70]);
let path = d3.geoPath(projection);

let boroughdata, zipcodedata,
    geoboro, boroarea, boroborder, borogetprop,
    geozip, ziparea, zipborder, zipgetprop;

window.onload = async () => {
    await ridership20192020();
    await ridership2020();
    await ridershipborough();
    await choropleth();
}

let ridership20192020 = async () => {
    tool = (x, y) => `${y} riders \n${x.toLocaleString(undefined, tooldate)}`;

    ridership = await d3.csv('/data/transportation/mta');

    let { daily, weekly, monthly, extent } = getData(ridership, 7, 1, 'riders', 'enter');

    gextent = extent;

    document.getElementById('ridership-line-container').innerHTML += `
    <p class="article-content">New York City is synonymous with a lot: Times Square, Central Park, the Empire
        State Building. But the thing that holds the city together is the MTA Subway system. In the midst of the
        COVID-19 pandemic, the iconic image of crowded trains is not to be found.
        <br><div id="avg"></div>
    </p>
    <p class="article-content">
        The following line chart shows the number of times people enter an MTA Subway turnstile since 2019. Note
        that on the daily view, there are drops on the weekends, regardless of the pandemic. Use the buttons to
        switch time intervals and hover over the line to view a more specific tooltip.</p>
    <div class="toggle-view-btns">
        <div class="btn-group" role="group">
            <button type="button" class="btn btn-primary" id="daily" disabled>Daily</button>
            <button type="button" class="btn btn-primary" id="weekly" disabled>Weekly</button>
            <button type="button" class="btn btn-primary" id="monthly" disabled>Monthly</button>
        </div>
    </div>`;

    document.getElementById('avg').innerHTML = `
    In 2019, there was an average of <b>${d3.format(",")(average(daily, 2019))}</b> swipes per day.
    This year, it's down to <b>${d3.format(",")(average(daily, 2020))}</b>.`;

    svg = d3.select('#ridership-line-container')
        .append('svg')
        .attr('id', 'ridership-graph')
        .attr('width', '100%')
        .attr('height', '50vh');

    margin = { 'top': 20, 'right': 50, 'bottom': 50, 'left': 100 };

    let riderline = new LineGraph(
        svg, daily,
        'date', 'riders',
        tool, margin,
        'ride-line',
        'ride-x', 'ride-y');
    await riderline.renderLineGraph();

    listen(riderline, 'daily', daily);
    listen(riderline, 'weekly', weekly);
    listen(riderline, 'monthly', monthly);
}

let ridership2020 = async () => {
    let extent2020 = [new Date('2020-01-01T00:00:00'), gextent[1]];
    setDate(gextent[1], -1);

    let data = parseData(ridership, extent2020, 1, 'riders', 'enter');

    let mextent = [new Date('2020-01-01T00:00:00'), new Date('2020-03-09T00:00:00')]

    let temp = parseData(ridership, mextent, 1, 'riders', 'enter');

    document.getElementById('ridership-2020').innerHTML = `
    <div class="article-content mb-2">
        Now let's take a look at data just from this year.
        We can see that the first major dip in ridership occurs on the week of March 8th.
        Schools officially closed on Sunday, March 15th. On Monday, March 16th, ridership dropped
        to <b>2,180,285</b> swipes. Previous Mondays in the year had an average of <b>${d3.format(",")(dayaverage(temp, 1))}</b> swipes.
    </div>`

    let svg2020 = d3.select('#ridership-2020')
        .append('svg')
        .attr('id', 'ridership-2020-graph')
        .attr('width', '100%')
        .attr('height', '50vh');

    let graph = new LineGraph(
        svg2020, data, 'date', 'riders',
        tool, margin, 'line-2020', 'x-2020', 'y-2020',
        { timedelay: 2000 });

    await graph.renderLineGraph();
    graph.yLabel('# of swipes');
}

let ridershipborough = async () => {
    let extent2020 = [new Date('2020-03-01T00:00:00'), gextent[1]];

    let data = boroughParse(ridership, extent2020);

    let {
        'New York County': manhattan,
        "Kings County": brooklyn,
        "Queens County": queens,
        "Bronx County": bronx,
        "Richmond County": staten
    } = percentChange(ridership, extent2020);

    document.getElementById('ridership-borough').innerHTML = `
    <div class="article-content mb-2">
        The following graph breaks down MTA ridership by borough since the beginning of March.
        Though ridership in all boroughs have fallen to relatively similar numbers,
        the percentage decrease for each borough is clearly different. Lets calculate ther percentage difference
        by comparing ridership from March 1st - May 2nd 2020 to the same timeframe from the previous year.<br><br>
        <b><span style="color: #CF5C36">Manhattan</span></b> has seen a <b>${manhattan}%</b> decrease, the largest out of all boroughs.
        <b><span style="color: #C2CFB2">Staten Island</span></b> has the second largest decrease with <b>${staten}%</b>
        though it should be noted that the Subway system is not used as much in Staten Island regardless of COVID.
        <b><span style="color: #A09EBB">Brooklyn</span></b> comes in third with a <b>${brooklyn}%</b> decrease, followed by
        <b><span style="color: #7C7C7C">Queens</span></b> with a <b>${queens}%</b> decrease.
        <b><span style="color: #EFC88B">The Bronx</span></b> has experienced the least percentage decrease with <b>${bronx}%.</b><br>
    </div>`

    let svgborough = d3.select('#ridership-borough')
        .append('svg')
        .attr('id', 'ridership-borough-graph')
        .attr('width', '100%')
        .attr('height', '50vh');

    let graph = new LineGraph(
        svgborough, data, 'date', 'riders',
        tool, margin, 'borough-line', 'borough-x', 'borough-y',
        {
            timedelay: 1000,
            color: 'red',
            strokewidth: 2,
        });

    let ex = [new Date('2020-03-01T00:00:00'), gextent[1]]
    await graph.renderMultiLine(
        ex, {
        'Kings County': '#A09EBB',
        'New York County': '#CF5C36',
        'Richmond County': '#C2CFB2',
        'Queens County': '#7C7C7C',
        'Bronx County': '#EFC88B'
    });
    graph.yLabel('# of swipes');
}

let mapScaffold = (container, id, legendid, colorid, tickcontainerid) => {
    let map = d3.select(`#${container}`)
        .append('svg')
        .attr('id', id)
        .attr('width', '100%')
        .attr('viewBox', [-147.88 * 1.2, -81.4 * 1.5, 975 * 1.2, 610 * 1.2])
        .append('g')
        .attr('transform', 'translate(-50)');

    let legend = map.append('g')
        .attr('id', legendid)
        .attr("width", 320)
        .attr("height", 50)
        .attr('transform', 'translate(100)')
        .attr("viewBox", [0, 0, 320, 50]);

    legend.append('g').attr('id', colorid);
    legend.append('g').attr('id', tickcontainerid);

    return { map, colorid, tickcontainerid };
}

let initMapData = async () => {
    boroughdata = await borodata();
    zipcodedata = await zipdata();
    geoboro = await d3.json('/static/json/boroughs.json');
    boroarea = topojson.feature(geoboro, geoboro.objects.boroughs).features;
    boroborder = topojson.mesh(geoboro, geoboro.objects.boroughs);
    geozip = await d3.json('/static/json/zip_codes.json');
    ziparea = topojson.feature(geozip, geozip.objects.zip_codes).features;
    zipborder = topojson.mesh(geozip, geozip.objects.zip_codes);
    zipgetprop = (d) => d.properties.zcta;
    borogetprop = (d) => d.properties.bname;
}

let choropleth = async () => {
    await initMapData();

    document.getElementById('choro-container').innerHTML = `
    Let's take a look at a map of New York City's coronavirus cases.
    Switch between borough and zipcode cases by using the buttons below.
    Hover over each area to see the number of cases. Zipcode areas that
    are grey do not have any COVID case data associated with them.<br>
    Toggle the subway stops to see the percentage decrease in ridership from
    March 1st to May 2nd of last year to this year. Not all subway stops are represented
    because of data inconsistencies. Hover over the stops to see the percentage decrease.
    Stops that are darker saw more decrease than lighter stops.<br><br>
    This map shows that the fact that ridership has decreased most dramatically in Manhattan.
    The outer boroughs have experienced significantly less decrease, which is correlated with
    an increased number of COVID-19 cases. Even though Manhattan is less populous than Queens
    and Brooklyn, it does have more population density which would theoretically lead to higher
    spread. But as seen when viewing the map with borough outlines, Manhattan is fourth in
    number of COVID-19 cases.<br>
    When we switch to the zipcode view, we can see that the area with the most number of cases
    (<b>3884</b>) has zipcode <b>11368</b>, the aptly named neighborhood of <b>Corona, Queens</b>.
    <div class="toggle-view-btns">
        <div class="btn-group" role="group">
            <button type="button" class="btn btn-primary" id="borough-toggle">Borough</button>
            <button type="button" class="btn btn-primary" id="zip-toggle">Zipcode</button>
        </div>
    </div>
    <div class="text-center noselect custom-control custom-switch">
      <input type="checkbox" class="custom-control-input" id="subwayswitch" name="subwayswitch">
      <label class="custom-control-label" for="subwayswitch">Subway Toggle</label>
    </div>`

    let { map, colorid, tickcontainerid } = mapScaffold(
        'choro-container', 'choro-map',
        'choro-legend', 'choro-color', 'choro-tick-container'
    );

    let tickid = 'choro-tick';
    let legendlabel = 'Number of COVID-19 cases';

    let choro = new Choropleth(
        map, 'choro-area', 'choro-border',
        boroarea, boroborder, path,
        boroughdata.casemap, boroughdata.colormap,
        borogetprop, legendlabel,
        colorid, tickid, tickcontainerid);

    choro.render();

    let stops = await d3.json('/static/json/subway_stops.json')
    let geostops = topojson.feature(stops, stops.objects.subway_stops).features;

    let stations = new Object();
    geostops.forEach((stop, i) => {
        let name = stop.properties.stop_name;
        if (name in stations) {
            geostops.splice(i, 1);
        } else {
            stations[name] = { 'prev': 0, 'curr': 0 };
        }
    })

    let prev = [new Date('2019-03-01T00:00:00'), new Date('2019-05-02T00:00:00')];
    let curr = [new Date('2020-03-01T00:00:00'), new Date('2020-05-02T00:00:00')];

    stopdrop(stations, ridership, prev, curr);

    let mapper = d3.scaleQuantize()
        .domain([0, 100])
        .range(d3.schemeReds[9]);

    let opacitymap = d3.scaleLinear()
        .domain([0, 100])
        .range([0.75, 1])

    let stopcolor = (d) => {
        let c = mapper(stations[d.properties.stop_name])
        return (c == undefined) ? 'transparent' : c;
    }

    let stopopacity = (d) => {
        let c = opacitymap(stations[d.properties.stop_name])
        return (c == undefined) ? 0 : c;
    }

    let stoplabel = (d) => `${d.properties.stop_name}, ${stations[d.properties.stop_name]}% decrease`

    document.getElementById('subwayswitch').addEventListener('change', (event) => {
        if (event.target.checked) {
            choro.add(geostops, 'subway-stops', stopcolor, stopopacity, stoplabel);
            checked = true;
        } else {
            choro.removeAll('subway-stops');
            checked = false;
        }
    })

    maplisten(choro, 'borough',
        boroarea, boroborder, borogetprop,
        boroughdata.casemap, boroughdata.colormap,
        geostops, 'subway-stops', stopcolor, stopopacity, stoplabel);

    maplisten(choro, 'zip',
        ziparea, zipborder, zipgetprop,
        zipcodedata.casemap, zipcodedata.colormap,
        geostops, 'subway-stops', stopcolor, stopopacity, stoplabel);

    $("#sources").css('display', 'block');
}

let maplisten = (map, type, area, border, prop, casemap, colormap,
    stops, stopsclass, stopcolor, stopopacity, stoplabel) => {
    document.getElementById(`${type}-toggle`).addEventListener('click', () => {
        if (choroview !== type) {
            map.update(area, border, prop, casemap, colormap);
            if (checked) {
                map.add(stops, stopsclass, stopcolor, stopopacity, stoplabel);
            }
            choroview = type;
        }
    })
}

let listen = (graph, id, data) => {
    let button = document.getElementById(id);
    button.disabled = false;
    button.addEventListener('click', () => {
        updateline(graph, id, data);
    })
}

let updateline = (graph, id, data) => {
    if (view !== id) {
        view = id;
        graph.updateLineGraph(data, 1000);
    }
}