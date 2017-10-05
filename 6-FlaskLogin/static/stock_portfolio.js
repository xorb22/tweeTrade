    Highcharts.setOptions({
        global: {
            useUTC: false
        }
    });
    // Create the chart
    
    Highcharts.stockChart('container', {
        chart: {
            events: {
                load: function () {

                    // set up the updating of the chart each second
                    var series = this.series[0];
                    setInterval(function () {


                    var x = (new Date()).getTime();
                    // get data from python script
                    $.ajax({
                        type: "GET",
                        url: "/get_data",
                        data: data, // your "template" data goes here
                        success: function(my_value) {
                            var y = my_value;
                            series.addPoint([x, y], true, true);
                            }
                        });


                        var x = (new Date()).getTime(), // current time
                        y = 200+Math.round(Math.random() * 15);
                        series.addPoint([x, y], true, true);
                    }, 5000);
                }
            }
        },
        rangeSelector: {
            buttons: [{
                count: 1,
                type: 'minute',
                text: '1M'
            }, {
                count: 5,
                type: 'minute',
                text: '5M'
            }, {
                type: 'all',
                text: 'All'
            }],
            inputEnabled: false,
            selected: 3
        },

        title: {
            text: 'Performance'
        },

        exporting: {
            enabled: false
        },

        tooltip: {
            pointFormat: '<span style="color:{series.color}">{series.name}</span>: <b>{point.y}</b> ({point.change}%)<br/>',
            valueDecimals: 2,
            split: true
        },

        series: [{
            name: 'AAPL',
            data: (function () {
                // generate an array of random data
                var data = [],
                time = (new Date()).getTime(),
                i;

                for (i = -999; i <= 0; i += 1) {
                    data.push([
                        time + i * 1000,
                        100+Math.round(Math.random(time) * 10)
                        ]);
                }
                return data;
            }())
        }]
    });
    //
    Highcharts.stockChart('container3', {
        chart: {
            events: {
                load: function () {

                    // set up the updating of the chart each second
                    var series = this.series[0];
                    setInterval(function () {
                        var x = (new Date()).getTime(), // current time
                        y = 200+Math.round(Math.random(x) * 100);
                        series.addPoint([x, y], true, true);
                    }, 1000);
                }
            }
        },
        rangeSelector: {
            buttons: [{
                count: 1,
                type: 'minute',
                text: '1M'
            }, {
                count: 5,
                type: 'minute',
                text: '5M'
            }, {
                type: 'all',
                text: 'All'
            }],
            inputEnabled: false,
            selected: 3
        },

        title: {
            text: 'Sentiment Indicator'
        },

        exporting: {
            enabled: false
        },

        tooltip: {
            pointFormat: '<span style="color:{series.color}">{series.name}</span>: <b>{point.y}</b> ({point.change}%)<br/>',
            valueDecimals: 2,
            split: true
        },

        series: [{
            name: 'AAPL',
            data: (function () {
                // generate an array of random data
                var data = [],
                time = (new Date()).getTime(),
                i;

                for (i = -99; i <= 0; i += 1) {
                    data.push([
                        time + i * 1000,
                        100+Math.round(Math.random(time) * 100)
                        ]);
                }
                return data;
            }())
        }]
    });
    // Create the chart
    Highcharts.stockChart('container2', {
        chart: {
            events: {
                load: function () {

                    // set up the updating of the chart each second
                    var series = this.series[0];
                    setInterval(function () {
                        var x = (new Date()).getTime(), // current time
                        y = 200+Math.round(Math.random(x) * 100);
                        series.addPoint([x, y], true, true);
                    }, 5000);
                }
            }
        },
        rangeSelector: {
            buttons: [{
                count: 1,
                type: 'minute',
                text: '1M'
            }, {
                count: 5,
                type: 'minute',
                text: '5M'
            }, {
                type: 'all',
                text: 'All'
            }],
            inputEnabled: false,
            selected: 0
        },

        title: {
            text: 'Portfolio Individuals'
        },

        exporting: {
            enabled: false
        },

        tooltip: {
            pointFormat: '<span style="color:{series.color}">{series.name}</span>: <b>{point.y}</b> ({point.change}%)<br/>',
            valueDecimals: 2,
            split: true
        },

        series: [{
            name: 'AAPL',
            data: (function () {
                // generate an array of random data
                var data = [],
                time = (new Date()).getTime(),
                i;

                for (i = -999; i <= 0; i += 1) {
                    data.push([
                        time + i * 1000,
                        100+Math.round(Math.random(time) * 100)
                        ]);
                }
                return data;
            }())
        }]
    });