var fessmodule = angular.module('myModule', ['ngResource']);

fessmodule.controller('fessCntrl', function ($scope, ScoreDataService) {
    
    $scope.scores = [{name:'Bukit Batok Street 1', URL:'http://maps.googleapis.com/maps/api/geocode/json?address=Singapore, SG, Singapore, 153 Bukit Batok Street 1&sensor=true'},
                    {name:'London 8', URL:'http://maps.googleapis.com/maps/api/geocode/json?address=Singapore, SG, Singapore, London 8&sensor=true'}];
    
    $scope.getScoreData = function(score){
        ScoreDataService.getScoreData(score).then(function (result) {
            $scope.ScoreData = result;          
        }, function (result) {
            alert("Error: No data returned");
        });
    };   
    
});

fessmodule.$inject = ['$scope', 'ScoreDataService'];

fessmodule.factory('ScoreDataService', ['$http','$q',  function($http) {
    
   var factory = {
        getScoreData: function (score) {  
            console.log(score);
            var data = $http({method: 'GET', url: score.URL});
            
        
            return data;
        }
   }       
    return factory;
}]);