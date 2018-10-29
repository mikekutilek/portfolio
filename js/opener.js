(function(){
	var app = angular.module('opener-app', []);

	app.controller('ctrl', ['$http', '$scope', function($http, $scope){
		$scope.tbl = false;
		
		$http.get('/api/v1/sabr/opener/teams').then(function(data){
			$scope.teamData = data.data;
            $scope.teams = Object.keys(data.data).slice(1);
            //console.log($scope.teams.slice(1));
        });

        $scope.hands = ['R', 'L'];

        var phrases = ['Hanging curveballs', 'Not bunting', 'Hitting dingers'];

	    $scope.getCandidates = function(selection){
	    	data = $scope.teamData;
	    	console.log(selection);
	    	team_abbr = data[selection];
	    	$scope.loading = true;
	    	
	    	$http.get('/api/v1/sabr/opener/' + team_abbr + '/RP/L').then(function(data){
	    		var p_data = data.data['candidates']
	    		var pitchers = [];
	    		if (p_data.length == 0){
	    			pitchers.push({"name": "N/A", "wOBA": "N/A"});
	    		}
	    		for (var i = 0; i < p_data.length; i++){
	    			var player = JSON.parse(p_data[i]);
	    			pitchers.push({"name": player['Player'], "wOBA": player['wOBA']});
	    		}
	    		$scope.lrps = pitchers;
	    		
	    	});

	    	$http.get('/api/v1/sabr/opener/' + team_abbr + '/RP/R').then(function(data){
	    		var p_data = data.data['candidates']
	    		var pitchers = [];
	    		if (p_data.length == 0){
	    			pitchers.push({"name": "N/A", "wOBA": "N/A"});
	    		}
	    		for (var i = 0; i < p_data.length; i++){
	    			var player = JSON.parse(p_data[i]);
	    			pitchers.push({"name": player['Player'], "wOBA": player['wOBA']});
	    		}
	    		$scope.rrps = pitchers;
	    	});

	    	$http.get('/api/v1/sabr/opener/' + team_abbr + '/SP/L').then(function(data){
	    		var p_data = data.data['candidates']
	    		var pitchers = [];
	    		if (p_data.length == 0){
	    			pitchers.push({"name": "N/A", "wOBA": "N/A"});
	    		}
	    		for (var i = 0; i < p_data.length; i++){
	    			var player = JSON.parse(p_data[i]);
	    			pitchers.push({"name": player['Player'], "wOBA": player['wOBA']});
	    		}
	    		$scope.lsps = pitchers;
	    	});

	    	$http.get('/api/v1/sabr/opener/' + team_abbr + '/SP/R').then(function(data){
	    		var p_data = data.data['candidates']
	    		var pitchers = [];
	    		if (p_data.length == 0){
	    			pitchers.push({"name": "N/A", "wOBA": "N/A"});
	    		}
	    		for (var i = 0; i < p_data.length; i++){
	    			var player = JSON.parse(p_data[i]);
	    			pitchers.push({"name": player['Player'], "wOBA": player['wOBA']});
	    		}
	    		$scope.rsps = pitchers;
	    	});

	    	$http.get('/api/v1/sabr/opener/' + team_abbr).then(function(data){
	    		$scope.loading = false;
	        	$scope.teamName = selection
	    		var chunkData = data.data['chunk']
	    		$scope.chunk = chunkData;
	            $scope.tbl = true;
	            if (team_abbr == 'ANY'){
		        	$scope.desc = false;
		        }
		        else{
		        	$scope.desc = true;
		        }
	    	});

	    	/*
	        $http.get('/api/v1/sabr/opener/' + team_abbr + '/SP/R').then(function(data){
	        	$scope.loading = false;
	        	$scope.teamName = selection
	        	var rightyRPData = data.data['rp_righties']
	        	var leftyRPData = data.data['rp_lefties']
	        	var rightySPData = data.data['sp_righties']
	        	var leftySPData = data.data['sp_lefties']
	        	var chunkData = data.data['chunk']
	        	var r_rps = [];
	        	var l_rps = [];
	        	var r_sps = [];
	        	var l_sps = [];
	        	if (rightyRPData.length == 0){
	        		r_rps.push({"name": "N/A", "wOBA": "N/A"});
	        	}
	        	if (leftyRPData.length == 0){
	        		l_rps.push({"name": "N/A", "wOBA": "N/A"});
	        	}
	        	if (rightySPData.length == 0){
	        		r_sps.push({"name": "N/A", "wOBA": "N/A"});
	        	}
	        	if (leftySPData.length == 0){
	        		l_sps.push({"name": "N/A", "wOBA": "N/A"});
	        	}
	        	for (var i = 0; i < rightyRPData.length; i++){
	        		var player = JSON.parse(rightyRPData[i]);
	        		r_rps.push({"name": player['Player'], "wOBA": player['wOBA']});
	        	}
	        	for (var i = 0; i < leftyRPData.length; i++){
	        		var player = JSON.parse(leftyRPData[i]);
	        		l_rps.push({"name": player['Player'], "wOBA": player['wOBA']});
	        	}
	        	for (var i = 0; i < rightySPData.length; i++){
	        		var player = JSON.parse(rightySPData[i]);
	        		r_sps.push({"name": player['Player'], "wOBA": player['wOBA']});
	        	}
	        	for (var i = 0; i < leftySPData.length; i++){
	        		var player = JSON.parse(leftySPData[i]);
	        		l_sps.push({"name": player['Player'], "wOBA": player['wOBA']});
	        	}
	            $scope.rrps = r_rps;
	            $scope.lrps = l_rps;
	            $scope.rsps = r_sps;
	            $scope.lsps = l_sps;
	            $scope.chunk = chunkData;
	            $scope.tbl = true;
	            if (team_abbr == 'ANY'){
		        	$scope.desc = false;
		        }
		        else{
		        	$scope.desc = true;
		        }
	        });
	        */

	    }
	}]);

	angular.bootstrap(document.getElementById('opener-app'), ['opener-app']);
})();