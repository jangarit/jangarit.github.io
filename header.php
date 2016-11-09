<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="utf-8" />
	<title><?php wp_title('&laquo;', true, 'right'); ?> <?php bloginfo('name'); ?></title> 
	<?php wp_head(); ?>
	<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1" />
	<link href='http://fonts.googleapis.com/css?family=Source+Sans+Pro:400,300,200' rel='stylesheet' type='text/css' />
	<link href='http://fonts.googleapis.com/css?family=Open+Sans' rel='stylesheet' type='text/css' />
	<link href='http://fonts.googleapis.com/css?family=Lato:300,400,500,700,900' rel='stylesheet' type='text/css'>
	<!--[if lt IE 9]>
	<script src="http://css3-mediaqueries-js.googlecode.com/svn/trunk/css3-mediaqueries.js"></script>
	<![endif]-->              		
	<link rel="stylesheet" href="<?php bloginfo('stylesheet_url'); ?>" type="text/css" media="screen" title="no title" charset="utf-8"/>
	<!--[if IE]>
		<script src="http://html5shiv.googlecode.com/svn/trunk/html5.js"></script>
	<![endif]-->
	<link rel="stylesheet" href="<?php bloginfo('stylesheet_directory'); ?>/css/mobile.css" type="text/css" media="screen" title="no title" charset="utf-8"/>
	<link rel="stylesheet" href="<?php bloginfo('stylesheet_directory'); ?>/css/slicknav.css" />
	<script src="http://code.jquery.com/jquery-1.10.2.min.js"></script>
<!--	<script src="http://cdnjs.cloudflare.com/ajax/libs/modernizr/2.6.2/modernizr.min.js"></script>-->
	<script src="<?php bloginfo('stylesheet_directory'); ?>/js/jquery.infinitescroll.js"></script>
	<script src="<?php bloginfo('stylesheet_directory'); ?>/js/jquery.slicknav.js"></script>
	<script src="<?php bloginfo('stylesheet_directory'); ?>/js/retina-1.1.0.min.js"></script>
	<script src="<?php bloginfo('stylesheet_directory'); ?>/js/imagesloaded.js"></script>
<!--	<script src="<?php bloginfo('stylesheet_directory'); ?>/js/jquery.film_roll.min.js"></script>-->
	<script src="<?php bloginfo('stylesheet_directory'); ?>/js/jquery.carouFredSel-6.2.1.js"></script>
	<script src="<?php bloginfo('stylesheet_directory'); ?>/js/masonry.js"></script>
	
	<script src="<?php bloginfo('stylesheet_directory'); ?>/js/scripts.js"></script>
	<?php $shortname = "bordergrid"; ?>
	<?php  
		$color = stripslashes(stripslashes(get_option($shortname.'_border_color',''))); 
				
		if (!$color)		
			{
				$color = '#efefef';
			}
			 ?>
	<style type="text/css">
	body{
		border: 30px solid <?php echo $color; ?>;
		min-height: 94vh;
	}
	.header_bottom { border-top: 30px solid <?php echo $color; ?>; border-left: 30px solid <?php echo $color; ?>; border-right: 30px solid <?php echo $color; ?>; }
	@media only screen and (min-width: 768px) and (max-width: 959px) {
		.header_bottom { border-top: none; }
	}
	@media only screen and ( max-width: 767px ){
		.header_bottom { border: none; }
		body { border: none;}
	}
	</style>
			
</head>
<body <?php body_class($class); ?>>
<header id="header">
	<div class="header_bottom">
	
		<div class="container">
			<div class="header_social">
				<?php if(get_option($shortname.'_twitter_link','') != '') { ?>
					<a href="<?php echo get_option($shortname.'_twitter_link',''); ?>"target="_blank"><img src="<?php bloginfo('stylesheet_directory'); ?>/images/twitter-icon.png" alt="twitter" /></a>
				<?php } ?>
				<?php if(get_option($shortname.'_facebook_link','') != '') { ?>
					<a href="<?php echo get_option($shortname.'_facebook_link',''); ?>"target="_blank"><img src="<?php bloginfo('stylesheet_directory'); ?>/images/facebook-icon.png" alt="facebook" /></a>
				<?php } ?>
				<?php if(get_option($shortname.'_google_plus_link','') != '') { ?>
					<a href="<?php echo get_option($shortname.'_google_plus_link',''); ?>"target="_blank"><img src="<?php bloginfo('stylesheet_directory'); ?>/images/google-plus-icon.png" alt="google plus" /></a>
				<?php } ?>
				<?php if(get_option($shortname.'_picasa_link','') != '') { ?>
					<a href="<?php echo get_option($shortname.'_picasa_link',''); ?>"target="_blank"><img src="<?php bloginfo('stylesheet_directory'); ?>/images/picasa-icon.png" alt="instagram" /></a>
				<?php } ?>
				<?php if(get_option($shortname.'_pinterest_link','') != '') { ?>
					<a href="<?php echo get_option($shortname.'_pinterest_link',''); ?>"target="_blank"><img src="<?php bloginfo('stylesheet_directory'); ?>/images/pinterest-icon.png" alt="pinterest" /></a>
				<?php } ?>
				<?php if(get_option($shortname.'_vimeo_link','') != '') { ?>
					<a href="<?php echo get_option($shortname.'_vimeo_link',''); ?>"target="_blank"><img src="<?php bloginfo('stylesheet_directory'); ?>/images/vimeo-icon.png" alt="vimeo" /></a>
				<?php } ?>
				<?php if(get_option($shortname.'_youtube_link','') != '') { ?>
					<a href="<?php echo get_option($shortname.'_youtube_link',''); ?>"target="_blank"><img src="<?php bloginfo('stylesheet_directory'); ?>/images/youtube-icon.png" alt="youtube" /></a>
				<?php } ?>
				<?php if(get_option($shortname.'_flickr_link','') != '') { ?>
					<a href="<?php echo get_option($shortname.'_flickr_link',''); ?>"target="_blank"><img src="<?php bloginfo('stylesheet_directory'); ?>/images/flickr-icon.png" alt="youtube" /></a>
				<?php } ?>				
				<div class="clear"></div>
			</div><!--//header_social-->
			<div class="clear"></div>
			<div class="header_mid">
			<div class="full_logo_cont">
				<?php if(get_option($shortname.'_custom_logo_url','') != "") { ?>
					<a href="<?php bloginfo('url'); ?>"><img src="<?php echo get_option($shortname.'_custom_logo_url',''); ?>" class="logo" alt="logo" /></a>
				<?php } else { ?>
					<a href="<?php bloginfo('url'); ?>"><img src="<?php bloginfo('stylesheet_directory'); ?>/images/logo.png" class="logo" alt="logo" /></a>
				<?php } ?>					
			</div><!--//logo_cont-->		
			
			<div class="header_menu">
				<?php wp_nav_menu('theme_location=header-menu&container=false&menu_id=main_header_menu'); ?>
			</div><!--//header_menu-->	
			<div class="clear"></div>
			</div><!--//header_mid-->
		</div><!--//container-->
		
	</div><!--//header_bottom-->	
</header><!--//header-->
<div class="header_spacing"></div>