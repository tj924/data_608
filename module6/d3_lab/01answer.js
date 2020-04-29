d3.csv("ue_industry.csv", data => {
    // Define your scales and generator here.

    const xScale = d3.scaleLinear()
        .domain(d3.extent(data, d => +d.index))
        .range([20, 1180]);

    const yScale = d3.scaleLinear()
        .domain(d3.extent(data, d => +d.Agriculture))
        .range([580, 20]);

    const dataset = data
        .filter(row => Number.isInteger(+row.Agriculture || NaN))
        .map(row =>({
                "x": +row.index,
                "y": +row.Agriculture
        }));

    let line = d3.line()
        .x(d => xScale(+d.x))
        .y(d => yScale(+d.y));

    d3.select("#answer1")
        .append("path")
        .attr("d", line(dataset))
        .attr("stroke", "#2e2928")

});

