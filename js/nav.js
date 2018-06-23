(function(){
	var navApp = angular.module('nav-app', []);

	navApp.controller('nav-ctrl', ['$scope', '$http', function($scope, $http){
		$http.get('./config/nav.json').then(function(rawNavData){
			$scope.navData = rawNavData.data;
		})
	}])

	angular.bootstrap(document.getElementById("nav-app"), ['nav-app']);
})();


