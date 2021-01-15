<?php
/**
 * All public facing functions
 */
namespace codexpert\Job_Importer;
use codexpert\product\Base;

/**
 * if accessed directly, exit.
 */
if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

/**
 * @package Plugin
 * @subpackage Front
 * @author codexpert <hello@codexpert.io>
 */
class Front extends Base {

	public $plugin;

	/**
	 * Constructor function
	 */
	public function __construct( $plugin ) {
		$this->plugin	= $plugin;
		$this->slug		= $this->plugin['TextDomain'];
		$this->name		= $this->plugin['Name'];
		$this->version	= $this->plugin['Version'];
	}

	public function add_admin_bar( $admin_bar ) {
		if( !current_user_can( 'manage_options' ) ) return;

		$admin_bar->add_menu( [
			'id'    => $this->slug,
			'title' => $this->name,
			'href'  => add_query_arg( 'page', $this->slug, admin_url( 'admin.php' ) ),
			'meta'  => [
				'title' => $this->name,            
			],
		] );
	}
	
	/**
	 * Enqueue JavaScripts and stylesheets
	 */
	public function enqueue_scripts() {
		$min = defined( 'IMJI_DEBUG' ) && IMJI_DEBUG ? '' : '.min';

		wp_enqueue_style( $this->slug, plugins_url( "/assets/css/front{$min}.css", IMJI ), '', $this->version, 'all' );

		wp_enqueue_script( $this->slug, plugins_url( "/assets/js/front{$min}.js", IMJI ), [ 'jquery' ], $this->version, true );
		
		$localized = [
			'ajaxurl'	=> admin_url( 'admin-ajax.php' )
		];
		wp_localize_script( $this->slug, 'IMJI', apply_filters( "{$this->slug}-localized", $localized ) );
	}

	public function head() {
		$url 		= imji_get_option( 'job-importer_basic', 'upload_json_file' );
		$request 	= wp_remote_get( $url );
		$body 		= wp_remote_retrieve_body( $request );
    	$data 		= json_decode( $body );

    	$data = '';
		// imji_pri($data);
	}
}