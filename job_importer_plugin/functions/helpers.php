<?php
if( !function_exists( 'get_plugin_data' ) ) {
	require_once( ABSPATH . 'wp-admin/includes/plugin.php' );
}

if( ! function_exists( 'imji_pri' ) ) :
function imji_pri( $data ) {
	echo '<pre>';
	if( is_object( $data ) || is_array( $data ) ) {
		print_r( $data );
	}
	else {
		var_dump( $data );
	}
	echo '</pre>';
}
endif;

/**
 * @param bool $show_cached either to use a cached list of posts or not. If enabled, make sure to wp_cache_delete() with the `save_post` hook
 */
if( ! function_exists( 'imji_get_posts' ) ) :
function imji_get_posts( $args = [], $show_heading = true, $show_cached = true ) {

	$defaults = [
		'post_type'         => 'post',
		'posts_per_page'    => -1,
		'post_status'		=> 'publish'
	];

	$_args = wp_parse_args( $args, $defaults );

	// use cache
	if( true === $show_cached && ( $cached_posts = wp_cache_get( "imji_{$_args['post_type']}", 'imji' ) ) ) {
		$posts = $cached_posts;
	}

	// don't use cache
	else {
		$queried = new WP_Query( $_args );

		$posts = [];
		foreach( $queried->posts as $post ) :
			$posts[ $post->ID ] = $post->post_title;
		endforeach;
		
		wp_cache_add( "imji_{$_args['post_type']}", $posts, 'imji', 3600 );
	}

	$posts = $show_heading ? [ '' => sprintf( __( '- Choose a %s -', 'imji' ), $_args['post_type'] ) ] + $posts : $posts;

	return apply_filters( 'imji_get_posts', $posts, $_args );
}
endif;

if( ! function_exists( 'imji_get_option' ) ) :
function imji_get_option( $key, $section, $default = '' ) {

	$options = get_option( $key );

	if ( isset( $options[ $section ] ) ) {
		return $options[ $section ];
	}

	return $default;
}
endif;

if( !function_exists( 'imji_get_template' ) ) :
/**
 * Includes a template file resides in /views diretory
 *
 * It'll look into /job-importer directory of your active theme
 * first. if not found, default template will be used.
 * can be overriden with job-importer_template_override_dir hook
 *
 * @param string $slug slug of template. Ex: template-slug.php
 * @param string $sub_dir sub-directory under base directory
 * @param array $fields fields of the form
 */
function imji_get_template( $slug, $base = 'views', $args = null ) {

	// templates can be placed in this directory
	$override_template_dir = apply_filters( 'imji_template_override_dir', get_stylesheet_directory() . '/job-importer/', $slug, $base, $args );
	
	// default template directory
	$plugin_template_dir = dirname( IMJI ) . "/{$base}/";

	// full path of a template file in plugin directory
	$plugin_template_path =  $plugin_template_dir . $slug . '.php';
	
	// full path of a template file in override directory
	$override_template_path =  $override_template_dir . $slug . '.php';

	// if template is found in override directory
	if( file_exists( $override_template_path ) ) {
		ob_start();
		include $override_template_path;
		return ob_get_clean();
	}
	// otherwise use default one
	elseif ( file_exists( $plugin_template_path ) ) {
		ob_start();
		include $plugin_template_path;
		return ob_get_clean();
	}
	else {
		return __( 'Template not found!', 'job-importer' );
	}
}
endif;

/**
 * Generates some action links of a plugin
 *
 * @since 1.0
 */
if( !function_exists( 'imji_action_link' ) ) :
function imji_action_link( $plugin, $action = '' ) {

	$exploded	= explode( '/', $plugin );
	$slug		= $exploded[0];

	$links = [
		'install'		=> wp_nonce_url( admin_url( "update.php?action=install-plugin&plugin={$slug}" ), "install-plugin_{$slug}" ),
		'update'		=> wp_nonce_url( admin_url( "update.php?action=upgrade-plugin&plugin={$plugin}" ), "upgrade-plugin_{$plugin}" ),
		'activate'		=> wp_nonce_url( admin_url( "plugins.php?action=activate&plugin={$plugin}&plugin_status=all&paged=1&s" ), "activate-plugin_{$plugin}" ),
		'deactivate'	=> wp_nonce_url( admin_url( "plugins.php?action=deactivate&plugin={$plugin}&plugin_status=all&paged=1&s" ), "deactivate-plugin_{$plugin}" ),
	];

	if( $action != '' && array_key_exists( $action, $links ) ) return $links[ $action ];

	return $links;
}
endif;