import {
    delay,
    setDate
} from '../utility.js';

export default class LineGraph {
    constructor(
        svg,
        data,
        xprop, yprop,
        toolformat,
        margin,
        id, xid, yid,
        {
            color = 'steelblue',
            timedelay = 4000,
            ease = d3.easeCubicInOut,
            strokewidth = 1.5,
        } = {}) {
        this.svg = svg;
        this.data = data;
        this.xprop = xprop;
        this.yprop = yprop;
        this.toolformat = toolformat;
        this.margin = margin;
        this.id = id;
        this.xid = xid;
        this.yid = yid;

        this.color = color;
        this.timedelay = timedelay;
        this.ease = ease;
        this.strokewidth = strokewidth;

        let pseudo = this.svg._groups[0][0];
        this.width = pseudo.clientWidth;
        this.height = pseudo.clientHeight;
    }

    renderAxes() {
        this.xAxis = g => g
            .attr('id', this.xid)
            .attr('transform', `translate(0, ${this.height - this.margin.bottom})`)
            .call(d3.axisBottom(this.x).ticks(this.width / 80).tickSizeOuter(0));

        this.yAxis = g => g
            .attr('id', this.yid)
            .attr('transform', `translate(${this.margin.left}, 0)`)
            .call(d3.axisLeft(this.y))

        this.svg.append('g').call(this.xAxis);
        this.svg.append('g').call(this.yAxis);
    }

    async renderLineGraph() {
        this.x = this.xScale();
        this.y = this.yScale();

        this.renderAxes();

        this.line = d3.line()
            .curve(d3.curveMonotoneX)
            .defined(d => !isNaN(d[this.yprop]))
            .x(d => this.x(d[this.xprop]))
            .y(d => this.y(d[this.yprop]))

        this.path = this.svg.append('path')
            .datum(this.data)
            .attr('id', this.id)
            .attr('fill', 'none')
            .attr('stroke', this.color)
            .attr('stroke-width', this.strokewidth)
            .attr('stroke-linejoin', 'round')
            .attr('stroke-linecap', 'round')
            .attr('d', this.line);

        let length = this.path.node().getTotalLength();

        this.path.attr('stroke-dasharray', `${length} ${length}`)
            .attr('stroke-dashoffset', length)
            .transition()
            .ease(this.ease)
            .duration(this.timedelay)
            .attr('stroke-dashoffset', 0);

        this.tooltip = this.svg.append("g");

        this.bisectListener(
            this.xprop,
            this.yprop,
            this.tooltip,
            this.toolformat,
            this.callout,
            this.x,
            this.y);

        return delay(this.timedelay);
    }

    async renderMultiLine(extent, colorMap) {
        setDate(extent[1], 1);
        let r = d3.timeDay.range(extent[0], extent[1]);
        this.x = d3.scaleTime()
            .domain(extent)
            .range([this.margin.left, this.width - this.margin.right]);

        this.y = d3.scaleLinear()
            .domain([0, d3.max(this.data, d => d3.max(d.values))]).nice()
            .range([this.height - this.margin.bottom, this.margin.top]);

        this.renderAxes();

        this.line = d3.line()
            .defined(d => !isNaN(d))
            .x((d, i) => this.x(r[i]))
            .y(d => this.y(d));

        this.path = this.svg.append('g')
            .attr('fill', 'none')
            .attr('id', this.id)
            .attr('stroke-width', this.strokewidth)
            .attr('stroke-linejoin', 'round')
            .attr('stroke-linecap', 'round')
            .selectAll('path')
            .data(this.data)
            .join('path')
            .attr('d', d => this.line(d.values))
            .attr('stroke', d => colorMap[d.name])
    }


    updateLineGraph(data, time) {
        this.data = data;
        this.x = this.xScale();
        this.y = this.yScale();

        let svg = this.svg.transition();

        let line = this.line;

        svg.select(`#${this.id}`)
            .duration(time)
            .attrTween('d', function () {
                let prev = d3.select(this).attr('d')
                let current = line(data);
                return d3.interpolatePath(prev, current);
            });

        svg.select(`#${this.xid}`)
            .duration(time)
            .call(this.xAxis);

        svg.select(`#${this.yid}`)
            .duration(time)
            .call(this.yAxis);

        this.bisectListener(
            this.xprop,
            this.yprop,
            this.tooltip,
            this.toolformat,
            this.callout,
            this.x,
            this.y);
    }

    xScale() {
        return d3.scaleTime()
            .domain(d3.extent(this.data, d => d[this.xprop]))
            .range([this.margin.left, this.width - this.margin.right]);
    }

    yScale() {
        return d3.scaleLinear()
            .domain([0, d3.max(this.data, d => d[this.yprop])]).nice()
            .range([this.height - this.margin.bottom, this.margin.top]);
    }

    callout(g, value) {
        if (!value) return g.style("display", "none");

        g
            .style("display", null)
            .style("pointer-events", "none")
            .style("font", "10px sans-serif");

        const path = g.selectAll("path")
            .data([null])
            .join("path")
            .attr("fill", "white")
            .attr("stroke", "black");

        const text = g.selectAll("text")
            .data([null])
            .join("text")
            .call(text => text
                .selectAll("tspan")
                .data((value + "").split(/\n/))
                .join("tspan")
                .attr("x", 0)
                .attr("y", (d, i) => `${i * 1.1}em`)
                .style("font-weight", (_, i) => i ? null : "bold")
                .text(d => d));

        const { x, y, width: w, height: h } = text.node().getBBox();

        text.attr("transform", `translate(${-w / 2},${15 - y})`);
        path.attr("d", `M${-w / 2 - 10},5H-5l5,-5l5,5H${w / 2 + 10}v${h + 20}h-${w + 20}z`);
    }

    bisect() {
        const bisect = d3.bisector(d => d.date).left;
        return mx => {
            const date = this.x.invert(mx);
            const index = bisect(this.data, date, 1);
            const a = this.data[index - 1];
            const b = this.data[index];
            return date - a.date > b.date - date ? b : a;
        }
    }

    bisectListener(xprop, yprop, tooltip, toolformat, callout, x, y) {
        let b = this.bisect();
        this.svg.on("touchmove mousemove", function () {
            const { [xprop]: xval, [yprop]: yval } = b(d3.mouse(this)[0]);
            tooltip
                .attr("transform", `translate(${x(xval)},${y(yval)})`)
                .call(callout, toolformat(xval, yval));
        });

        this.svg.on("touchend mouseleave", () => tooltip.call(callout, null));
    }

    yLabel(label) {
        this.svg.select(`#${this.yid}`)
            .call(g => g.select('.tick:last-of-type text').clone()
                .attr('x', 3)
                .attr('text-anchor', 'start')
                .attr('font-weight', 'bold')
                .text(label));
    }
}
