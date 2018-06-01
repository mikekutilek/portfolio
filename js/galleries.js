(function(){
	var galleryApp = angular.module('gallery-app', []);

	galleryApp.controller('gallery-ctrl', function($scope, $http){
		$http.get('/config/galleries.json').then(function(rawData){
			var arr = rawData.data;
			var newArr = [];
			for (var i = 0; i < arr.length; i += 3){
				newArr.push(arr.slice(i, i+3));
			}
			$scope.galleries = newArr;
		});
	});
	angular.bootstrap(document.getElementById("gallery-app"), ['gallery-app']);
})();