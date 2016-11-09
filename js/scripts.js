function zoomcorrect(){
	$('#posts_cont').imagesLoaded( function() {
		$('.feat').each( function() {
			var h = $(this).children().children().height();
			console.log(h);
		$(this).css('height', h + 'px');
	});
});
	}
$(document).ready(function() {
	zoomcorrect();
    $('.header_menu li').hover(
        function () {
            $('ul:first', this).css('display','block');
        }, 
        function () {
            $('ul:first', this).css('display','none');         
        }
    );  
	$('.header_spacing').css('height', $('#header').outerHeight() + 'px');
	    
	$('#main_header_menu').slicknav();
	    
	if($('#header').css('position') == 'absolute')
		$('#header').css('top', $('.slicknav_menu').outerHeight()+50 + 'px');
	else
		$('#header').css('top', '0px');                 				
	$("#home_cont").on("mouseenter", "#stalac_cont .stalac_box", function(event){
		$(this).find('.stalac_box_hover').css('display','block');
	}).on("mouseleave", "#stalac_cont .stalac_box", function(event){
		$(this).find('.stalac_box_hover').css('display','none');
	});  
	    
	$('.archive_box_media').hover(
		function() {
			$(this).find('.archive_box_hover').css('display','block');
		},
		function() {
			$(this).find('.archive_box_hover').css('display','none');
		}
	);
	var $container = $('.home_posts_cont');
	$container.imagesLoaded( function() {
		$container.masonry({
			itemSelector: '.home_box',
		    columnWidth: '.home_box'
		});
	});
	    
});
$(window).load(function() {
	$('.header_spacing').css('height', $('#header').outerHeight()-10 + 'px');
	var $container = $('.home_posts_cont');
	$container.imagesLoaded( function() {
		$container.masonry({
			itemSelector: '.home_box',
		    columnWidth: '.home_box'
		});
	});
});
$(window).scroll(function() {
	$('.header_spacing').css('height', $('#header').outerHeight()-10 + 'px');
	if($('#header').css('position') == 'absolute')
		$('#header').css('top', $('.slicknav_menu').outerHeight() +50 + 'px');
	else
		$('#header').css('top', '0px');
	zoomcorrect();
	
});
$(window).resize(function() {
	$('.header_spacing').css('height', $('#header').outerHeight()-10 + 'px');
	if($('#header').css('position') == 'absolute')
		$('#header').css('top', $('.slicknav_menu').outerHeight()+50 + 'px');
	else
		$('#header').css('top', '0px');
	$('.feat').css('height', $('.feat img').height() + 'px');
	zoomcorrect();	
});