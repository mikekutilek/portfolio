(function(){
	var app = angular.module('fp-app', []);

	app.controller('fp-ctrl', ['$http', '$scope', function($http, $scope){
		//$scope.getNHL = function(selection){
		$scope.loading = true;
		$http.get('/api/v1/corsica/fp/skater').then(function(data){
			console.log(data.data);
			$scope.players = data.data;
			$scope.loading = false;
		});
		$('.skater').on('click', function() {
			$scope.loading = true;
			$('.goalie').removeClass('active');
    		$('.skater').addClass('active');
			$http.get('/api/v1/corsica/fp/skater').then(function(data){
				console.log(data.data);
				$scope.players = data.data;
				$scope.loading = false;
			});
   		});
	    $('.goalie').on('click', function() {
	    	$scope.loading = true;
	    	$('.skater').removeClass('active');
    		$('.goalie').addClass('active');
	    	$http.get('/api/v1/corsica/fp/goalie').then(function(data){
				console.log(data.data);
				$scope.players = data.data;
				$scope.loading = false;
			});
	    });

	    $('.nfl').on('click', function() {
	    	$scope.loading = true;
	    	//$('.nfl-stats').removeClass('active');
    		//$('.goalie').removeClass('active');
	    	$http.get('/api/v1/wopr/fp/RB').then(function(data){
				console.log(data.data);
				$scope.players = data.data;
				$scope.loading = false;
			});
	    });
	    $('.nhl').on('click', function() {
	    	$scope.loading = true;
	    	$http.get('/api/v1/corsica/fp/skater').then(function(data){
				console.log(data.data);
				$scope.players = data.data;
				$scope.loading = false;
			});
	    })
		//}
	}]);

	angular.bootstrap(document.getElementById('fp-app'), ['fp-app']);
})();