  var seriesOptions = [],
        seriesCounter = 0,
        names = ['MSFT', 'AAPL', 'GOOG'];

    /**
     * Create the chart when all data is loaded
     * @returns {undefined}
     */
    function createChart() {

        Highcharts.stockChart('container_MU', {
                    chart: {
            events: {
                load: function () {

                    // set up the updating of the chart each second
                    var series = this.series;
                    // var series1 = this.series[1];

                    setInterval(function () {

                        for (j = 0; j <= 2; j += 1) {
                            var x = (new Date()).getTime(), // current time
                            y = 100+Math.round(Math.random() * 3);
                            series[j].addPoint([x, y]);
                            }    
                    }, 5000);
                }
            }
        },

            rangeSelector: {
                inputEnabled: false,
                selected: 6
            },

            // yAxis: {
            //     labels: {
            //         formatter: function () {
            //             return (this.value > 0 ? ' + ' : '') + this.value;
            //         }   
            //     },
            //     plotLines: [{
            //         value: 0,
            //         width: 2,
            //         color: 'silver'
            //     }]
            // },

            plotOptions: {
                series: {
                    // compare: 'percent',
                    showInNavigator: true
                }
            },
        title: {
            text: 'Portfolio'
        },
            tooltip: {
                pointFormat: '<span style="color:{series.color}">{series.name}</span>: <b>{point.y}</b> ({point.change}%)<br/>',
                valueDecimals: 2,
                split: true
            },

            series: seriesOptions
        });
    }

    $.each(names, function (i, name) {

        // $.getJSON('https://www.highcharts.com/samples/data/jsonp.php?filename=' + name.toLowerCase() + '-c.json&callback=?',    function (data) {

            seriesOptions[i] = {
                name: name,
                data: (function () {
                // generate an array of random data
                var data = [],
                    time = (new Date()).getTime(),
                    j;

                for (j = -999; j <= 0; j += 1) {
                    data.push([
                        time + j * 100,
                        20+Math.round(Math.random() * 15)
                    ]);
                }
                return data;
            }())
            };


            // As we're loading the data asynchronously, we don't know what order it will arrive. So
            // we keep a counter and create the chart when all the data is loaded.
            seriesCounter += 1;

            if (seriesCounter === names.length) {
                createChart();
            }
        // });
    });