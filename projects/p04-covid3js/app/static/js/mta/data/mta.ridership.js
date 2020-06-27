import { toISO, createScaffold } from "../../utility.js";

let dayaverage = (data, day) => {
    let select = data.filter(d => d.date.getDay() == day);

    let total = select.reduce((acc, cur) => {
        return acc + cur.riders;
    }, 0)

    return Math.round(total / select.length);
}

let percentChange = (data, extent) => {

    let prev = extent.map(d => new Date(`${toISO(d)}T00:00:00`));
    prev[0].setFullYear(prev[0].getFullYear() - 1);
    prev[1].setFullYear(prev[1].getFullYear() - 1);

    let select2019 = {
        'New York County': 0,
        'Kings County': 0,
        'Queens County': 0,
        'Bronx County': 0,
        'Richmond County': 0
    };
    let select2020 = {
        'New York County': 0,
        'Kings County': 0,
        'Queens County': 0,
        'Bronx County': 0,
        'Richmond County': 0
    };

    data.forEach(d => {
        let date = new Date(`${d.date}T00:00:00`);
        if (date <= prev[1] && date >= prev[0]) {
            select2019[d.borough] += +d.enter;
        }
        if (date >= extent[0] && date <= extent[1]) {
            select2020[d.borough] += +d.enter;
        }
    })

    let obj = new Object();

    for (const borough in select2019) {
        obj[borough] = change(select2019[borough], select2020[borough])
    }

    return obj;
}

let change = (prev, curr) => ((prev - curr) / prev * 100).toFixed(2);

let boroughParse = (data, extent) => {
    let scaffold = {
        'Kings County': createScaffold(extent, 1, 'riders'),
        'New York County': createScaffold(extent, 1, 'riders'),
        'Richmond County': createScaffold(extent, 1, 'riders'),
        'Queens County': createScaffold(extent, 1, 'riders'),
        'Bronx County': createScaffold(extent, 1, 'riders')
    }

    data.forEach(d => {
        if (d.date in scaffold[d.borough]) {
            scaffold[d.borough][d.date]['riders'] += +d['enter'];
            delete scaffold[d.borough][d.date]['date'];
        }
    })

    let master = new Array();

    for (const borough in scaffold) {
        let arr = new Array();
        for (const date in scaffold[borough]) {
            arr.push(scaffold[borough][date]['riders'])
        }
        scaffold[borough] = arr;
        master.push({
            'name': borough,
            'values': scaffold[borough]
        })
    }

    return master;
}

let stopdrop = (stations, ridership, prev, curr) => {
    ridership.forEach(d => {
        if (d.station in stations) {
            let date = new Date(`${d.date}T00:00:00`);
            if (date <= prev[1] && date >= prev[0]) {
                stations[d.station]['prev'] += +d.enter;
            }
            if (date >= curr[0] && date <= curr[1]) {
                stations[d.station]['curr'] += +d.enter;
            }
        }
    })

    for (const station in stations) {
        let obj = stations[station];
        if (obj.prev == 0 || obj.curr == 0) {
            delete stations[station]
        } else {
            stations[station] = +change(obj.prev, obj.curr);
        }
    }
}

export { dayaverage, boroughParse, percentChange, stopdrop };
