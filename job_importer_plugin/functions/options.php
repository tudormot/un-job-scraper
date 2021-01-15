<?php
/**
 * Usually functions that return settings values
 */

if( ! function_exists( 'imji_site_url' ) ) :
function imji_site_url() {
	return get_bloginfo( 'url' );
}
endif;