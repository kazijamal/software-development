export default class Choropleth {
    constructor(
        svg, areaclass, borderclass,
        geoarea, geoborder, path,
        datamap, colormap,
        getprop,
        legendlabel, legendcolor,
        legendticks, tickcontainer
    ) {
        this.svg = svg;
        this.areaclass = areaclass;
        this.borderclass = borderclass;
        this.geoarea = geoarea;
        this.geoborder = geoborder;
        this.path = path;
        this.datamap = datamap;
        this.colormap = colormap;
        this.getprop = getprop;
        this.legendlabel = legendlabel;
        this.legendcolor = legendcolor;
        this.legendticks = legendticks;
        this.tickcontainer = tickcontainer;
    }

    colorfunction(d) {
        let c = this.colormap(this.datamap[d]);
        return (c == undefined) ? 'lightgrey' : c;
    }

    render() {
        this.svg.selectAll(`.${this.areaclass}`)
            .data(this.geoarea)
            .join(
                enter => {
                    return enter.append('path')
                        .attr('d', this.path)
                        .attr('class', this.areaclass)
                        .attr('fill', d => this.colorfunction(this.getprop(d)));
                }
            ).append('title')
            .text(d => `${this.getprop(d)}, ${this.datamap[this.getprop(d)]} cases`);

        this.addBorder();

        this.legend(6, 320, 50, 18, 0, 22, 0, 5, 'd');
    }

    add(features, classname, colorfunct, opacityfunct, label) {
        this.svg.selectAll(`.${classname}`).remove();
        this.svg.selectAll(`.${classname}`)
            .data(features)
            .join(
                enter => {
                    return enter.append('path')
                        .attr('d', this.path)
                        .attr('class', classname)
                        .attr('fill', d => colorfunct(d))
                        .attr('opacity', d => opacityfunct(d))
                }
            ).append('title')
            .text(d => label(d));
    }

    removeAll(classname) {
        this.svg.selectAll(`.${classname}`).remove();
    }

    update(area, border, getprop, datamap, colormap) {
        this.geoarea = area;
        this.geoborder = border;
        this.getprop = getprop;
        this.datamap = datamap;
        this.colormap = colormap;

        this.svg.selectAll(`.${this.areaclass}`).remove();
        this.svg.selectAll(`.${this.borderclass}`).remove();
        this.render();
    }

    addBorder() {
        this.svg.append('path')
            .datum(this.geoborder)
            .attr('fill', 'none')
            .attr('class', this.borderclass)
            .attr('stroke', 'black')
            .attr('stroke-linejoin', 'round')
            .attr('d', this.path);
    }

    legend(
        tickSize = 6,
        width = 320,
        height = 44 + tickSize,
        marginTop = 18,
        marginRight = 0,
        marginBottom = 16 + tickSize,
        marginLeft = 0,
        ticks = width / 64,
        tickFormat,
        tickValues) {

        let x = d3.scaleLinear()
            .domain([-1, this.colormap.range().length - 1])
            .rangeRound([marginLeft, width - marginRight]);

        d3.select(`#${this.legendcolor}`)
            .selectAll('rect')
            .data(this.colormap.range())
            .join(
                enter => enter.append('rect')
                    .attr('x', (d, i) => x(i - 1))
                    .attr('y', marginTop)
                    .attr('width', (d, i) => x(i) - x(i - 1))
                    .attr('height', height - marginTop - marginBottom)
                    .attr('fill', d => d)
            );

        let tickAdjust = g => g.selectAll(".tick line").attr("y1", marginTop + marginBottom - height);
        const thresholds = this.colormap.thresholds();
        const thresholdFormat = d => Math.round(d);
        tickValues = d3.range(thresholds.length);
        tickFormat = i => thresholdFormat(thresholds[i], i);

        d3.select(`#${this.legendticks}`).remove();

        d3.select(`#${this.tickcontainer}`)
            .append("g")
            .attr("transform", `translate(0,${height - marginBottom})`)
            .attr('id', this.legendticks)
            .call(d3.axisBottom(x)
                .ticks(ticks, typeof tickFormat === "string" ? tickFormat : undefined)
                .tickFormat(typeof tickFormat === "function" ? tickFormat : undefined)
                .tickSize(tickSize)
                .tickValues(tickValues))
            .call(tickAdjust)
            .call(g => g.select(".domain").remove())
            .call(g => g.append("text")
                .attr("x", -marginLeft)
                .attr("y", marginTop + marginBottom - height - 6)
                .attr("fill", "currentColor")
                .attr("text-anchor", "start")
                .attr("font-weight", "bold")
                .text(this.legendlabel));
    }
}