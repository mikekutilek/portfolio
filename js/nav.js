(function(){
	var navApp = angular.module('nav-app', []);

	navApp.controller('nav-ctrl', ['$scope', '$http', function($scope, $http){
		$http.get('./config/nav.json').then(function(rawNavData){
			/*
			var navMap: object = {};

			angular.forEach(rawNavData.data, function(navGroup, index){
				navMap[navGroup.type] = navGroup;
			});

			$scope.navDataMap = navMap;
			*/
			$scope.navData = rawNavData.data;
		})
	}])

	angular.bootstrap(document.getElementById("nav-app"), ['nav-app']);
})();


