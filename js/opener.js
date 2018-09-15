(function(){
	var app = angular.module('opener-app', []);

	app.controller('ctrl', ['$http', '$scope', function($http, $scope){
		$scope.tbl = false;
		
		$http.get('http://localhost:8080/api/v1/sabr/opener/teams').then(function(data){
			$scope.teamData = data.data;
            $scope.teams = Object.keys(data.data).slice(1);
            //console.log($scope.teams.slice(1));
        });

	    $scope.getCandidates = function(selection){
	    	data = $scope.teamData;
	    	console.log(selection);
	    	team_abbr = data[selection];
	    	
	        $http.get('http://localhost:8080/api/v1/sabr/opener/' + team_abbr).then(function(data){
	        	var rightyData = data.data['righties']
	        	var leftyData = data.data['lefties']
	        	var chunkData = data.data['chunk']
	        	var rplayers = [];
	        	var lplayers = [];
	        	if (rightyData.length == 0){
	        		rplayers.push({"name": "N/A", "wOBA": "N/A"});
	        	}
	        	if (leftyData.length == 0){
	        		lplayers.push({"name": "N/A", "wOBA": "N/A"});
	        	}
	        	for (var i = 0; i < rightyData.length; i++){
	        		var player = JSON.parse(rightyData[i]);
	        		rplayers.push({"name": player['Player'], "wOBA": player['wOBA']});
	        	}
	        	for (var i = 0; i < leftyData.length; i++){
	        		var player = JSON.parse(leftyData[i]);
	        		lplayers.push({"name": player['Player'], "wOBA": player['wOBA']});
	        	}
	            $scope.rplayers = rplayers;
	            $scope.lplayers = lplayers;
	            $scope.chunk = chunkData;
	            $scope.tbl = true;
	            if (team_abbr == 'ANY'){
		        	$scope.desc = false;
		        }
		        else{
		        	$scope.desc = true;
		        }
	        });
	    }
	}]);

	angular.bootstrap(document.getElementById('opener-app'), ['opener-app']);
})();