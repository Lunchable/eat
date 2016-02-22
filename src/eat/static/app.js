var $headernav = $("#header-nav");
var $navmenu = $(".nav-menu");
var $signin = $("#signin");
var $signup = $("#signup");

// need to differentiate between the mobile and desktop version

$(document).ready(function(){
				$("input:radio[value='yes']").change(function(){
    				$("#child_Income").removeClass('hidden');
  				});
  				$("input:radio[value='no']").change(function(){
  					$("#child_Income").addClass('hidden');
  				});
			$('.cancel').click(function() {
				$("input").removeAttr('required');
				window.location='/';
				});
			})