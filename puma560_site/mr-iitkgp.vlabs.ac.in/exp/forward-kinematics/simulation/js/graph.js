/**
 * 
 *  Document     : graph.js
 *  Created on   : 13 April, 2016, 4:45:25 PM
 *  Author       : Ujjal Dey
 *  Organization : IIT Khatagpur
 *  
 */
var trace1 = {
    x: [],
    y: [],
    z: [],
    mode: 'markers',
    marker: {
        size: 4,
        line: {
            color: 'rgba(227, 237, 217, 0.24)',
            width: 0.5
        },
        opacity: 1
    },
    type: 'scatter3d'
};
 var data = [trace1];
    var layout = {margin: {
            l: 0,
            r: 0,
            b: 0,
            t: 0
        }};
    Plotly.newPlot('myDiv', data, layout);
