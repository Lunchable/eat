var $headernav = $("#header-nav");
var $navmenu = $(".nav-menu");
var $signin = $("#signin");
var $signup = $("#signup");
$(document).ready(function(){
	$navmenu.hide();
});

// need to differentiate between the mobile and desktop version
$headernav.click(function(){
	$navmenu.slideToggle();
});

$signin.click(function(){
	window.load('signin');
});

// $(".overlay-class").click(function(){
// 	$('modal').removeClass('hide');
// })