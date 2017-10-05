  


  var seriesOptions = [],
        seriesCounter = 0,
        names = searchterms;


    /**
     * Create the chart when all data is loaded
     * @returns {undefined}
     */
    function createChart(names, seriesOptions) {


        Highcharts.stockChart('container_MU_sentiment', {
                    chart: {
            events: {
                load: function () {

                    // set up the updating of the chart each second
                    var series = this.series;
                    var j = 0;
                    var obj, x, y;

                    setInterval(function () {
                        $.each(names, function (i, name) {

                            $.ajax({
                                type: "GET",
                                // async: false,
                                url: "/get_data_sentiment/"+name,
                                success: function(my_value) {
                                    obj = JSON.parse(my_value);
                                    x = new Date.parse(obj.timeStamp[0]).getTime();
                                    y = parseFloat(obj.sentiment[0]);

                                    // [Date.parse(obj.timeStamp[j]).getTime(),
                                    // parseFloat(obj.sentiment[j])]
                                    // console.
                                    series[i].addPoint([x, y]);

                                },
                                  error: function (my_value) {
                                    // console.log(my_value);
                                 }
                            });

                        });
                            

                    }, 5000);
                }
            }
        },
        title: {
            text: 'Sentiment Indicators'
        },
            rangeSelector: {
                inputEnabled: false,
                selected: 6
            },  

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

            series: seriesOptions
        });
    }



    $.each(names, function (i, name) {
            seriesOptions[i] = {
                name: name,
                data: //[]
                function () {
                    var data = [], j;
                    $.ajax({
                        type: "GET",
                        async: false,
                        url: "/get_data_sentiment/"+name,
                        success: function(my_value) {
                            var obj = JSON.parse(my_value);
                            for (j = 0; j < obj.timeStamp.length; j += 1) {
                                data.push([Date.parse(obj.timeStamp[j]).getTime(),
                                    parseFloat(obj.sentiment[j])]); 
                                }
                            },
                        error: function (my_value) {
                            }
                    });
                    return data;
                }()
            };


            // As we're loading the data asynchronously, we don't know what order it will arrive. So
            // we keep a counter and create the chart when all the data is loaded.
            seriesCounter += 1;

            if (seriesCounter === names.length) {
                createChart(names, seriesOptions);
            }
        // });
    });