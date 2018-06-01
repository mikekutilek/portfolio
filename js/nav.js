(function(){
	var navApp = angular.module('nav-app', []);
})();
/*
app.controller('nav-ctrl', ['$scope', '$http', '$window', function($scope, $http, $window){
	$http.get('./config/nav.json').then(function(rawNavData){
		var navMap: object = {};

		angular.forEach(rawNavData.data, function(navGroup, index){
			navMap[navGroup.type] = navGroup;
		});

		$scope.navDataMap = navMap;
		$scope.navData = rawNavData.data;
	})
}])
*/
