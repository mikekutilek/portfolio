(function(){
	var app = angular.module('team-app', []);

	app.controller('ctrl', ['$http', '$scope', function($http, $scope){
		$http.get('http://localhost:8080/api/v1/sabr/opener/teams').then(function(data){
			$scope.teamData = data.data;
            $scope.teams = Object.keys(data.data);
        });
	    //$scope.players = [{"name": "Jameson Taillon", "pid": "11674"}, {"name": "Clayton Kershaw", "pid": "2036"}];

	    $scope.getCandidates = function(selection){
	    	data = $scope.teamData;
	    	//console.log(data)
	    	team_abbr = data[selection]
	        //console.log(team_abbr);
	        $http.get('http://localhost:8080/api/v1/sabr/opener/' + team_abbr).then(function(data){
	        	var rightyData = data.data['righties']
	        	var leftyData = data.data['lefties']
	        	var rplayers = [];
	        	var rwOBAs = [];
	        	var lplayers = [];
	        	var lwOBAs = [];
	        	for (var i = 0; i < rightyData.length; i++){
	        		var player = JSON.parse(rightyData[i]);
	        		rplayers.push(player['Player']);
	        		rwOBAs.push(player['wOBA']);
	        		//console.log(player['Player']);
	        		//console.log(player['wOBA']);
	        	}
	        	for (var i = 0; i < leftyData.length; i++){
	        		var player = JSON.parse(leftyData[i]);
	        		lplayers.push(player['Player']);
	        		lwOBAs.push(player['wOBA']);
	        	}
	            //console.log(data.data['righties']);
	            $scope.rplayers = rplayers;
	            $scope.rwOBAs = rwOBAs;
	            $scope.lplayers = lplayers;
	            $scope.lwOBAs = lwOBAs;
	            //$scope.rightyData = data.data['righties'];
	            //$scope.leftyData = data.data['lefties'];
	            //$scope.drawPlot();
	        });
	    }
	}]);

	angular.bootstrap(document.getElementById('team-app'), ['team-app']);
})();