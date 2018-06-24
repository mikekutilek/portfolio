(function(){
	var videoApp = angular.module('video-app', []).filter('trustAsResourceUrl', ['$sce', function($sce) {
    	return function(val) {
        	return $sce.trustAsResourceUrl(val);
    	};
	}]);

	videoApp.config(function($sceDelegateProvider){
		$sceDelegateProvider.resourceUrlWhitelist([
			'self',
			'*://www.youtube.com/**',
			'*://www.player.vimeo.com/video/**']);
	});

	videoApp.controller('video-ctrl', ['$scope', '$http', '$sce', function($scope, $http, $sce){
		$http.get('/config/videos.json').then(function(rawData){
			$scope.$watch(function() {
			    $('.selectpicker').selectpicker('refresh');
			});
			var arr = rawData.data;
			var urls = [];
			var links = [];
			var years = [];
			var teams = [];
			for (var i = 0; i < arr.length; i++){
				var url = "";
				var link = "";
				var year = arr[i].year;
				var team = arr[i].team;
				if (arr[i].site == "youtube"){
					link = "https://www." + arr[i].site + ".com/watch?v=" + arr[i].id;
					url = "https://www." + arr[i].site + ".com/embed/" + arr[i].id;
				}
				else {
					link = "https://www." + arr[i].site + ".com/" + arr[i].id;
					url = "https://player." + arr[i].site + ".com/video/" + arr[i].id;
				}
				if (years.indexOf(year) == -1){
					years.push(year);
				}
				if (teams.indexOf(team) == -1){
					teams.push(team);
				}
				links.push(link);
				urls.push(url);
			}
			$scope.teams = teams;
			$scope.years = years;
			$scope.links = links;
			$scope.urls = urls;
			$scope.videos = arr;
			$scope.limit = 10;
			$scope.loadMore = function() {
				$scope.limit += 10;
			};
			$scope.resetLimit = function() {
				$scope.limit = 10;
			}
		});
	}]);
	angular.bootstrap(document.getElementById("video-app"), ['video-app']);
})();