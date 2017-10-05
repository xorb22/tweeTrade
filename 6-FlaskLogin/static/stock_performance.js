  var seriesOptions = [],
        seriesCounter = 0,
        names = tickers

    function getCol(matrix, col){
       var column = [];
       for(var i=0; i<matrix.length; i++){
          column.push(matrix[i][col]);
       }
       return column;
    }
    /**
     * Create the chart when all data is loaded
     * @returns {undefined}
     */
    function createChart(names, seriesOptions) {

        Highcharts.stockChart('container_performance', {
            chart: {
        events: {
            load: function () {
                var x; //Array.apply(null, Array(2)).map(Number.prototype.valueOf,0);
                var y = 0;
                var series = this.series[0];
                setInterval(function () {

                 $.each(names, function (i, name) {

                            $.ajax({
                                type: "GET",
                                // async: false,
                                url: "/get_data/"+name,
                                success: function(my_value) {
                                    obj = JSON.parse(my_value);
                                    x = Date.parse(obj.timeStamp[0]).getTime();
                                    console.log("value before");
                                    console.log(y);
                                    y = math.add(y,parseFloat(obj.price[0]));
                                    console.log("value after");
                                    console.log(y);
                                    // console.log(y);

                                },
                                  error: function (my_value) {
                                    // console.log(my_value);
                                 }
                            });

                 });


                 if (y != 0) {       
                        series.addPoint([x, y], true, true);
                        console.log(x);
                        console.log(y);
                        console.log("added above two");
                    }
                y = 0;
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
        selected: 2
    },

    title: {
        text: 'Stock Investment Valuation'
    },

    exporting: {
        enabled: false
    },

            series: seriesOptions
        });
    }


    var data = 0, valV; //Array.apply(null, Array(2)).map(Number.prototype.valueOf,0);
    $.each(names, function (i, name) {
         valV = function () {
                    var data = [], j;
                    $.ajax({
                        type: "GET",
                        async: false,
                        url: "/get_data/"+name,
                        success: function(my_value) {
                            var obj = JSON.parse(my_value);
                            for (j = 0; j < obj.price.length; j += 1) {
                                data.push( [ Date.parse(obj.timeStamp[j]).getTime(), parseFloat(obj.price[j]) ]); 
                                }
                            },
                        error: function (my_value) {
                            }
                    });
                    return data;
                }();


        valsum = getCol(valV,1);
        valDate = getCol(valV,0);
        // console.log(valV);
        data = math.add(data,valsum)
    });

    var valGraph = [];

       for(var i=0; i<valsum.length; i++){
          valGraph.push([valDate[i], data[i]]);
       }
        console.log(valGraph);

    seriesOptions = [{
        name: 'Stock Investment Valuation',
        data: valGraph
    }];
    console.log(seriesOptions);
    createChart(names, seriesOptions);
