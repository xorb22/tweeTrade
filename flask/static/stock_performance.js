  


  var seriesOptions1 = [],
        seriesCounter1 = 0,
        names1 = ['Performance'];

    /**
     * Create the chart when all data is loaded
     * @returns {undefined}
     */
    function createChart() {


        Highcharts.stockChart('container_performance', {
                    chart: {
            events: {
                load: function () {

                    // set up the updating of the chart each second
                    var series = this.series;
                    // var series1 = this.series[1];

                    setInterval(function () {

                        // for (j = 0; j <= names1.length; j += 1) {
                            // var x = (new Date()).getTime() // current time
    
                            // $.getJSON('/get_data', function (my_value) { 
                            //     y = my_value

                            // })
                            // console.log( "At least got here!" ); 
                            // $.getJSON('https://www.highcharts.com/samples/data/jsonp.php?filename=usdeur.json&callback=?', function (data) {
                                    // console.log(data) // y = my_value }); 
                                // }

                            // $.getJSON('/get_data',    function (my_value) {
// 
                            // }
                            $.ajax({
                                type: "GET",
                                url: "/get_data",
                                // data: data, // your "template" data goes here

                                success: function(my_value) {
                                    var obj = JSON.parse(my_value);
                                    // console.log(typeof obj.price);
                                    // console.log((new Date()).getTime());
                                    // console.log(new Date.parse(obj.timeStamp).getTime());

                                    var x = new Date.parse(obj.timeStamp).getTime();
                                    // var x = (new Date()).getTime(); // current time
                                    var y = parseFloat(obj.price);
                                    series[0].addPoint([x, y]);

                                    // series[0].addPoint([x, y], true, true);

                                },
                                  error: function (my_value) {
                                    // console.log(my_value);
                                 }

                            });

                            // var y = 100

                            // y = (j+1)*10+Math.round(Math.random() * 3);
                            // series[0].addPoint([x, y]);
                        


                            // }    
                    }, 5000);
                }
            }
        },
        title: {
            text: 'Performance'
        },
            rangeSelector: {
                inputEnabled: false,
                selected: 6
            },

            // yAxis: {
            //     labels: {
            //         formatter: function () {
            //             return (this.value > 0 ? ' + ' : '') + this.value + '%';
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

            tooltip: {
                pointFormat: '<span style="color:{series.color}">{series.name}</span>: <b>{point.y}</b> ({point.change}%)<br/>',
                valueDecimals: 2,
                split: true
            },

            series: seriesOptions1
        });
    }



    $.each(names1, function (i, name) {

        // $.getJSON('https://www.highcharts.com/samples/data/jsonp.php?filename=' + name.toLowerCase() + '-c.json&callback=?',    function (data) {

            seriesOptions1[i] = {
                name: name,
                data: []
            //     (function () {
            //     // generate an array of random data
            //     var data = [],
            //         time = (new Date()).getTime(),
            //         j;
            //         console.log(time)
            //     for (j = -999; j <= 0; j += 1) {
            //         data.push([
            //             time + j * 100,
            //             i*0+300*Math.sin(0)+Math.round(Math.random() * 0)
            //         ]);
            //     }
            //     return data;
            // }())
            };


            // As we're loading the data asynchronously, we don't know what order it will arrive. So
            // we keep a counter and create the chart when all the data is loaded.
            seriesCounter1 += 1;

            if (seriesCounter1 === names1.length) {
                createChart();
            }
        // });
    });