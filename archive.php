<?php get_header(); ?>	
<div class="container">
	
	<div class="archive_title">
		<?php printf( __( '%s', 'twentyten' ), '<span>' . single_cat_title( '', false ) . '</span>' ); ?>
		<div class="clear"></div>
	</div><!--//archive_title-->
	<div id="posts_cont" class="home_posts_cont">
		<?php
		$args = array_merge( $wp_query->query, array( 'posts_per_page' => 6 ) );
		query_posts($args);		
		while (have_posts()) : the_post(); ?>
			<div class="home_box">
				<div class="feat">
					<?php if(get_post_meta( get_the_ID(), 'page_featured_type', true ) == 'youtube') { ?>
						<iframe width="560" height="240" src="http://www.youtube.com/embed/<?php echo get_post_meta( get_the_ID(), 'page_video_id', true ); ?>?wmode=transparent" frameborder="0" allowfullscreen></iframe>
					<?php } elseif(get_post_meta( get_the_ID(), 'page_featured_type', true ) == 'vimeo') { ?>
						<iframe src="http://player.vimeo.com/video/<?php echo get_post_meta( get_the_ID(), 'page_video_id', true ); ?>?title=0&amp;byline=0&amp;portrait=0&amp;color=03b3fc" width="500" height="240" frameborder="0" webkitAllowFullScreen mozallowfullscreen allowFullScreen></iframe>
					<?php } else { ?>
						<a href="<?php the_permalink(); ?>"><?php the_post_thumbnail('home-listing-bordergrid'); ?></a>
					<?php } ?>
				</div>
				<div class="home_box_info">
				<h3><a href="<?php the_permalink(); ?>"><?php echo substr( get_the_title(), 0, 40 ); ?></a></h3>
				
				</div><!--//home_box_info-->
			</div> <!-- //home_box -->
		<?php endwhile; ?>
	</div> <!-- //posts_cont -->
	<div class="clear"></div>
	<div class="load_more_cont">
		<div align="center"><div class="load_more_text">
		<?php
		ob_start();
		next_posts_link('<img src="' . get_bloginfo('stylesheet_directory') . '/images/loading-button.png" />');
		$buffer = ob_get_contents();
		ob_end_clean();
		if(!empty($buffer)) echo $buffer;
		?>
		</div></div>
	</div><!--//load_more_cont-->     					
	<?php wp_reset_query(); ?>                                    		
	
	<div class="clear"></div>	
</div> <!-- //container -->	
<div class="clear"></div>
<script type="text/javascript">
$(document).ready(function($){
//jQuery(window).load(function($) {
	var $container = $('.home_posts_cont');
  $('#posts_cont').infinitescroll({
 
    navSelector  : "div.load_more_text",            
		   // selector for the paged navigation (it will be hidden)
    nextSelector : "div.load_more_text a:first",    
		   // selector for the NEXT link (to page 2)
    itemSelector : "#posts_cont .home_box"
		   // selector for all items you'll retrieve
  },function(arrayOfNewElems){
  
	    var $newElems = $( arrayOfNewElems );
	    $container.imagesLoaded( function() {
		    $container.masonry( 'appended', $newElems );	  
		});
   
  });  
});
</script>	
<?php get_footer(); ?> 		