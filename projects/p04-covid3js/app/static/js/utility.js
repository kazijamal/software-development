const setDate = (date, diff) => {
    if (diff == 'month') {
        date.setMonth(date.getMonth() + 1);
    } else {
        date.setDate(date.getDate() + diff);
    }
}

const delay = (time) => {
    return new Promise(resolve => {
        setTimeout(() => {
            resolve();
        }, time);
    });
};

const toISO = (date) => {
    let iso = date.toISOString();
    return iso.substring(0, iso.indexOf('T'));
}

const parseData = (data, extent, step, property, subprop) => {

    let scaffold = createScaffold(extent, step, property);

    fillScaffold(scaffold, data, step, property, subprop);

    let arr = new Array();

    for (const date in scaffold) {
        arr.push(scaffold[date]);
    }

    return arr;
}

const createScaffold = (extent, step, property) => {
    let copy = extent.map(d => new Date(`${toISO(d)}T00:00:00`));

    let scaffold = new Object();

    if (step == 'month') {
        copy.forEach(d => { d.setDate(1) });
    }
    for (let i = copy[0]; i <= copy[1]; setDate(i, step)) {
        let iso = i.toISOString();
        let subiso = iso.substring(0, iso.indexOf('T'));

        scaffold[subiso] = { date: new Date(iso), [property]: 0 };
    }

    return scaffold;
}

const fillScaffold = (scaffold, data, step, property, subprop) => {
    if (step == 1) {
        data.forEach(d => {
            if (d.date in scaffold) {
                scaffold[d.date][property] += +d[subprop];
            }
        });
    } else if (step == 7) {
        data.forEach(d => {
            let current = new Date(`${d.date}T00:00:00`);
            let day = current.getDay();

            setDate(current, (day < 6) ? 6 - day : 7);

            scaffold[toISO(current)][property] += +d[subprop];
        })
    } else if (step == 'month') {
        data.forEach(d => {
            let current = new Date(`${d.date}T00:00:00`);
            current.setDate(1);

            if (current.getFullYear() !== 2018) {
                scaffold[toISO(current)][property] += +d[subprop];
            }
        })
    }
}

let tooldate = { month: "short", day: "numeric", year: "numeric" };

let getData = (data, bshift, eshift, prop, subprop) => {
    let extent = d3.extent(data, d => `${d.date}T00:00:00`).map(d => new Date(d));

    let daily = parseData(data, extent, 1, prop, subprop);

    setDate(extent[0], bshift); // set beginning date to 2019-01-05
    setDate(extent[1], eshift); // set       end date to 2020-05-02

    let weekly = parseData(data, extent, 7, prop, subprop);

    let monthly = parseData(data, extent, 'month', prop, subprop);

    return { daily, weekly, monthly, extent };
}

let average = (data, year) => {
    const select = data.filter(d => d.date.getFullYear() == year);

    let total = select.reduce((acc, cur) => {
        return acc + cur.riders;
    }, 0)

    return Math.round(total / select.length);
}

export { setDate, delay, parseData, tooldate, getData, average, toISO, createScaffold };