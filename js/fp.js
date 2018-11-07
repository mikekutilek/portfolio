(function(){
	var app = angular.module('fp-app', []);

	app.controller('fp-ctrl', ['$http', '$scope', function($http, $scope){
		//$scope.getNHL = function(selection){
		$scope.loading = true;
		$http.get('/api/v1/corsica/fp/skater/FPG').then(function(data){
			//console.log(data.data);
			var df = data.data;
			var len = data.data.length;
			//console.log(len);
			var pages = len / 20;
			$scope.players = df.slice(0, 20);
			$scope.loading = false;
		});

	    $('.nfl').on('click', function() {
	    	$scope.loading = true;
	    	var qb = $('.qb').attr('class');
	    	var rb = $('.rb').attr('class');
	    	var wr = $('.wr').attr('class');
	    	var te = $('.te').attr('class');
	    	var flex = $('.flex').attr('class');
    		var qbvalues = qb.split(" ");
    		var rbvalues = rb.split(" ");
    		var wrvalues = wr.split(" ");
    		var tevalues = te.split(" ");
    		var flexvalues = flex.split(" ");
    		if (qbvalues.pop() == 'active'){
    			var pos = 'QB';
    			var sort = 'FPG';
    		}
    		if (rbvalues.pop() == 'active'){
    			var pos = 'RB';
    			var sort = 'WOG';
    		}
    		if (wrvalues.pop() == 'active'){
    			var pos = 'WR';
    			var sort = 'WOPRG';
    		}
    		if (tevalues.pop() == 'active'){
    			var pos = 'TE';
    			var sort = 'WOPRG';
    		}
    		if (flexvalues.pop() == 'active'){
    			var pos = 'flex';
    			var sort = 'WOG';
    		}
	    	$http.get('/api/v1/wopr/fp/' + pos + '/' + sort).then(function(data){
				$scope.players = data.data;
				$('.filters.nhl-options').removeClass('showx');
		    	$('.filters.nhl-options').addClass('hidex');
		    	$('.nhl-stats').removeClass('showx');
		    	$('.nhl-stats').addClass('hidex');
		    	$('.filters.mlb-options').removeClass('showx');
		    	$('.filters.mlb-options').addClass('hidex');
		    	$('.mlb-stats').removeClass('showx');
		    	$('.mlb-stats').addClass('hidex');
		    	$('.filters.nfl-options').removeClass('hidex');
		    	$('.filters.nfl-options').addClass('showx');
		    	$('.nfl-stats').removeClass('hidex');
		    	$('.nfl-stats').addClass('showx');
		    	$('table.showx th.sorted').removeClass('sorted');
	    		$('table.showx th#'+sort.toLowerCase()).addClass('sorted');
		    	$scope.loading = false;
			});

	    });
	    $('.nhl').on('click', function() {
	    	$scope.loading = true;
	    	var skater = $('.skater').attr('class');
    		var skatersplit = skater.split(" ");
    		if (skatersplit.pop() == 'active'){
    			var pos = 'skater';
    		}
    		else{
    			var pos = 'goalie';
    		}
	    	$http.get('/api/v1/corsica/fp/' + pos + '/FPG').then(function(data){
				$scope.players = data.data;
				$('.filters.nfl-options').removeClass('showx');
		    	$('.filters.nfl-options').addClass('hidex');
		    	$('.nfl-stats').removeClass('showx');
		    	$('.nfl-stats').addClass('hidex');
		    	$('.filters.mlb-options').removeClass('showx');
		    	$('.filters.mlb-options').addClass('hidex');
		    	$('.mlb-stats').removeClass('showx');
		    	$('.mlb-stats').addClass('hidex');
		    	$('.filters.nhl-options').removeClass('hidex');
		    	$('.filters.nhl-options').addClass('showx');
		    	$('.nhl-stats').removeClass('hidex');
		    	$('.nhl-stats').addClass('showx');
		    	$('table.showx th.sorted').removeClass('sorted');
	    		$('#fpg').addClass('sorted');
				$scope.loading = false;
			});
	    });
	    $('.mlb').on('click', function() {
	    	$('.filters.nhl-options').removeClass('showx');
	    	$('.filters.nhl-options').addClass('hidex');
	    	$('.nhl-stats').removeClass('showx');
	    	$('.nhl-stats').addClass('hidex');
	    	$('.filters.nfl-options').removeClass('showx');
	    	$('.filters.nfl-options').addClass('hidex');
	    	$('.nfl-stats').removeClass('showx');
	    	$('.nfl-stats').addClass('hidex');
	    	$('.filters.mlb-options').removeClass('hidex');
	    	$('.filters.mlb-options').addClass('showx');
	    	$('.mlb-stats').removeClass('hidex');
	    	$('.mlb-stats').addClass('showx');
	    });

		$('.skater').on('click', function() {
			$scope.loading = true;
			$('.goalie').removeClass('active');
    		$('.skater').addClass('active');
			$http.get('/api/v1/corsica/fp/skater/FPG').then(function(data){
				//console.log(data.data);
				$scope.players = data.data;
				$scope.loading = false;
				$('table.showx th.sorted').removeClass('sorted');
	    		$('#fpg').addClass('sorted');
			});
   		});
	    $('.goalie').on('click', function() {
	    	$scope.loading = true;
	    	$('.skater').removeClass('active');
    		$('.goalie').addClass('active');
	    	$http.get('/api/v1/corsica/fp/goalie/FPG').then(function(data){
				//console.log(data.data);
				$scope.players = data.data;
				$scope.loading = false;
				$('table.showx th.sorted').removeClass('sorted');
	    		$('#fpg').addClass('sorted');
			});
	    });
	    $('.qb').on('click', function() {
	    	$scope.loading = true;
	    	$('.rb').removeClass('active');
	    	$('.wr').removeClass('active');
	    	$('.te').removeClass('active');
	    	$('.flex').removeClass('active');
    		$('.qb').addClass('active');
	    	$http.get('/api/v1/wopr/fp/QB/FPG').then(function(data){
				//console.log(data.data);
				$scope.players = data.data;
				$scope.loading = false;
				$('table.showx th.sorted').removeClass('sorted');
	    		$('#fpg').addClass('sorted');
			});
	    });
	    $('.rb').on('click', function() {
	    	$scope.loading = true;
	    	$('.qb').removeClass('active');
	    	$('.wr').removeClass('active');
	    	$('.te').removeClass('active');
	    	$('.flex').removeClass('active');
    		$('.rb').addClass('active');
	    	$http.get('/api/v1/wopr/fp/RB/WOG').then(function(data){
				//console.log(data.data);
				$scope.players = data.data;
				$scope.loading = false;
				$('table.showx th.sorted').removeClass('sorted');
	    		$('#wog').addClass('sorted');
			});
	    });
	    $('.wr').on('click', function() {
	    	$scope.loading = true;
	    	$('.qb').removeClass('active');
	    	$('.rb').removeClass('active');
	    	$('.te').removeClass('active');
	    	$('.flex').removeClass('active');
    		$('.wr').addClass('active');
	    	$http.get('/api/v1/wopr/fp/WR/WOPRG').then(function(data){
				//console.log(data.data);
				$scope.players = data.data;
				$scope.loading = false;
				$('table.showx th.sorted').removeClass('sorted');
	    		$('#woprg').addClass('sorted');
			});
	    });
	    $('.te').on('click', function() {
	    	$scope.loading = true;
	    	$('.qb').removeClass('active');
	    	$('.rb').removeClass('active');
	    	$('.wr').removeClass('active');
	    	$('.flex').removeClass('active');
    		$('.te').addClass('active');
	    	$http.get('/api/v1/wopr/fp/TE/WOPRG').then(function(data){
				//console.log(data.data);
				$scope.players = data.data;
				$scope.loading = false;
				$('table.showx th.sorted').removeClass('sorted');
	    		$('#woprg').addClass('sorted');
			});
	    });
	    $('.flex').on('click', function() {
	    	$scope.loading = true;
	    	//var newcol = $(this);
	    	$('.qb').removeClass('active');
	    	$('.rb').removeClass('active');
	    	$('.wr').removeClass('active');
	    	$('.te').removeClass('active');
    		$('.flex').addClass('active');
	    	$http.get('/api/v1/wopr/fp/flex/WOG').then(function(data){
				//console.log(data.data);
				$scope.players = data.data;
				$scope.loading = false;
				$('table.showx th.sorted').removeClass('sorted');
	    		$('#wog').addClass('sorted');
			});
	    });

	    $('.sortable').on('click', function() {
	    	$scope.loading = true;
	    	var newcol = $(this);
	    	var sport = $('ul#sport-filters > li.active').text().toLowerCase();
	    	console.log(sport);
	    	if (sport == 'nhl'){
	    		api = 'corsica';
	    	}
	    	if (sport == 'nfl'){
	    		api = 'wopr';
	    	}
	    	if (sport == 'mlb'){
	    		api = 'sabr';
	    	}
	    	var pos = $('div.showx > ul#filters > li.active').text().toLowerCase();
	    	var category = $(this).text();
	    	if (category == 'FP'){
	    		var sort = 'FP';
	    	}
	    	if (category == 'FP/G'){
	    		var sort = 'FPG'
	    	}
	    	if (category == 'WO'){
	    		var sort = 'WO'
	    	}
	    	if (category == 'WO/G'){
	    		var sort = 'WOG'
	    	}
	    	if (category == 'WOPR'){
	    		var sort = 'WOPR'
	    	}
	    	if (category == 'WOPR/G'){
	    		var sort = 'WOPRG'
	    	}
	    	$http.get('/api/v1/' + api + '/fp/' + pos + '/' + sort).then(function(data){
				$scope.players = data.data;
				$scope.loading = false;
				$('table.showx th.sorted').removeClass('sorted');
	    		//console.log($(this));
	    		newcol.addClass('sorted');
			});
			
	    })

		//}
	}]);

	angular.bootstrap(document.getElementById('fp-app'), ['fp-app']);
})();