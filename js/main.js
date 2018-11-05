(function($) {
	"use strict";

	//On Click Open Menu Items
	$('.menu-block, .menu-item').on('click', function() {
	    $('.name').addClass('reverse');
	    $('.name-container').addClass('reverse');
	    $('.menu-blocks').addClass('hidex');
	    $('.inline-nav-container').addClass('showx');
	    $('.inline-nav-container.style2').addClass('dark');
	});
	//On Click Open About/Resume Block
	$('.about-block, .menu-item.about').on('click', function() {
	    $('.content-blocks').removeClass('showx');
	    $('.content-blocks.about').addClass('showx');
	    $('.menu-item').removeClass('active');
	    $('.menu-item.about').addClass('active');
	});
	$(document).on('click', '.open-about', function() {
	    var projectUrl = $(this).attr("href");
	    $('.content-blocks.about section').load(projectUrl);
	    return false;
	});
	//On Click Open Projects Block
	$('.projects-block, .menu-item.projects').on('click', function() {
	    $('.content-blocks').removeClass('showx');
	    $('.content-blocks.projects').addClass('showx');
	    $('.menu-item').removeClass('active');
	    $('.menu-item.projects').addClass('active');
	});
	$(document).on('click', '.open-projects', function() {
	    var projectUrl = $(this).attr("href");
	    $('.content-blocks.projects section').load(projectUrl);
	    return false;
	});
	//On Click Open Photography Block
	$('.photography-block, .menu-item.photography').on('click', function() {
	    $('.content-blocks').removeClass('showx');
	    $('.content-blocks.photography').addClass('showx');
	    $('.menu-item').removeClass('active');
	    $('.menu-item.photography').addClass('active');
	});
	$(document).on('click', '.open-photography', function() {
	    var projectUrl = $(this).attr("href");
	    $('.content-blocks.photography section').load(projectUrl);
	    return false;
	});
	//On Click Open Videography Block
	$('.videography-block, .menu-item.videography').on('click', function() {
	    $('.content-blocks').removeClass('showx');
	    $('.content-blocks.videography').addClass('showx');
	    $('.menu-item').removeClass('active');
	    $('.menu-item.videography').addClass('active');
	});
	$(document).on('click', '.open-videography', function() {
	    var projectUrl = $(this).attr("href");
	    $('.content-blocks.videography section').load(projectUrl);
	    return false;
	});
	//On Click Close Blocks
	$('#close').on('click', function() {
	    $('.name').removeClass('reverse');
	    $('.name-container').removeClass('reverse');
	    $('.content-blocks').removeClass('showx');
	    $('.menu-blocks').removeClass('hidex');
	    $('.inline-nav-container').removeClass('showx');
	    $('.menu-item').removeClass('active');
	});
	//On Click Close Blog Post And Project Details
	$('#close-pop').on('click', function() {
	    $('.content-blocks.pop').removeClass('showx');
	    $('.sidebar-menu').removeClass('hidex');
	    $('.inline-nav-container').addClass('showx');
	    $('.content-blocks.pop section').empty();
	});

	$('.menu-block, .menu-item, #close').on('click', function() {
	    $('.content-blocks').animate({ scrollTop: 0 }, 800);
	});	

	//Portfolio Modal
	$(document).on('click', '.open-project', function() {
	    var projectUrl = $(this).attr("href");
	    $('.inline-nav-container').removeClass('showx');
	    $('.sidebar-menu').addClass('hidex');
	    $('.content-blocks.pop').addClass('showx');
	    $('.content-blocks.pop section').load(projectUrl);
	    //+' .load-data > *'
	    return false;
	});

})(jQuery);