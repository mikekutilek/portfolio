(function(){
    google.load('visualization', '1', { packages : ['controls'] } );
    google.setOnLoadCallback(function(){ 
        angular.bootstrap(document.getElementById('memory-app'), ['memory-app']);
    });

    var memoryApp = angular.module('memory-app', []);

    memoryApp.controller('memory-ctrl', ['$http', '$scope', function($http, $scope) {

        $scope.durations = [
            {
                "value": "Last hour",
                "start": 120
            },
            {
                "value": "Last 6 hours",
                "start": 720,
            },
            {
                "value": "Last 12 hours",
                "start": 1440
            },
            {
                "value": "Last 24 hours",
                "start": 2880
            },
            {
                "value": "Last week",
                "start": 20160
            },
            {
                "value": "Last month",
                "start": 604800
            },
            {
                "value": "Forever",
                "start": 0
            }
        ]

        $scope.dselected = $scope.durations[1].value;

        $scope.frequencies = [
            {
                "value": "30 seconds",
                "step": 1
            },
            {
                "value": "1 minute",
                "step": 2
            },
            {
                "value": "30 minutes",
                "step": 60
            },
            {
                "value": "1 hour",
                "step": 120
            },
            {
                "value": "6 hours",
                "step": 720
            },
            {
                "value": "12 hours",
                "step": 1440
            },
            {
                "value": "24 hours",
                "step": 2880
            }
        ]

        $scope.fselected = $scope.frequencies[0].value;
        
        
        $http.get("http://localhost:8080/api/v3/yarn/memory").then(
            function(result) {
                $scope.airavataData = result.data;
                var len = result.data.length;
                $scope.drawMemoryPlot('airavata', len - 720, 1);
            },
            function(httpErr){
                console.error(httpErr);
            }
        );

        $scope.generateOptions = function(){
            var options = {
                fontName: 'Open Sans',
                dataOpacity: 0.75,
                backgroundColor: { fill: 'transparent' },
                hAxis: {
                    title: 'Time',
                    textStyle: {
                        fontSize: 12
                    }
                },
                vAxis: {
                    title: 'Memory',
                    textStyle: {
                        fontSize: 12
                    }
                }
            };
            return options;
        };

        $scope.drawMemoryPlot = function(server, start, step){
            var g_data = new google.visualization.DataTable();
            g_data.addColumn('datetime', 'Time');
            g_data.addColumn('number', 'allocatedMB');
            g_data.addColumn('number', 'availableMB');

            if (server == 'airavata'){
                var memory = $scope.airavataData;
            }

            var chart_data = [];
            var len = memory.length;

            for (var i = start; i < len; i+=step){
                var time = memory[i].time;
                var separators = [' ', '-', ':'];
                var p = time.split(new RegExp(separators.join('|'), 'g'));
                var date = new Date(p[0], p[1], p[2], p[3], p[4], p[5]);
                console.log(date);
                var a = [date, parseInt(memory[i].allocatedMB), parseInt(memory[i].availableMB)];
                chart_data.push(a);
            }
            g_data.addRows(chart_data);

            var chart = new google.visualization.ChartWrapper({
                'chartType': 'LineChart',
                'containerId': document.getElementById(server+'-chart')
            });

            var control = new google.visualization.ControlWrapper({
                'controlType': 'ChartRangeFilter',
                'containerId': 'control',
                'options': {
                    'filterColumnLabel': 'Time',
                    'height': 5
                }
            });
            var dashboard = new google.visualization.Dashboard(document.getElementById('dashboard'));
            dashboard.bind(control, chart);
            dashboard.draw(g_data);
        };

        $scope.redraw = function() {
            var len = $scope.airavataData.length;

            var dur = document.getElementById("duration-select");
            var freq = document.getElementById("frequency-select");

            var dindex = dur.selectedIndex;
            var findex = freq.selectedIndex;
            var start = len - $scope.durations[dindex].start;
            var step = $scope.frequencies[findex].step;

            if (dur.selectedIndex == 6){
                start = 0
            }

            if (start < 0){
                start = 0;
            }

            if (step > len){
                step = len;
            }
            $scope.drawMemoryPlot('airavata', start, step);
        };

    }]);

})();

