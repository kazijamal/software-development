let reqcasedata = async (keyword) => await d3.csv(`/data/transportation/covid/${keyword}`);

let zipdata = async () => {
    let cases = await reqcasedata('tests-by-zcta');
    cases.shift();

    let casemap = new Object();
    cases.forEach(zip => {
        casemap[zip.modzcta] = +zip.Positive
    });

    let colormap = colorMapper(cases, 'Positive');

    return { casemap, colormap };
}

let borodata = async () => {
    let cases = await reqcasedata('boro');
    cases.pop();

    cases[0]['BOROUGH_GROUP'] = 'Bronx';

    let casemap = new Object();
    cases.forEach(boro => {
        casemap[boro.BOROUGH_GROUP] = +boro.COVID_CASE_COUNT;
    })

    let colormap = colorMapper(cases, 'COVID_CASE_COUNT');

    return { casemap, colormap };
}

let colorMapper = (cases, prop) => {
    return d3.scaleQuantize()
        .domain([0, d3.max(cases, d => +d[prop])])
        .range(d3.schemeBlues[9]);
}

export { zipdata, borodata };