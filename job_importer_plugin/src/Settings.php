<?php
/**
 * All settings related functions
 */
namespace codexpert\Job_Importer;
use codexpert\product\Base;

/**
 * @package Plugin
 * @subpackage Settings
 * @author codexpert <hello@codexpert.io>
 */
class Settings extends Base {

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
	
	public function init_menu() {
		
		$settings = [
			'id'            => $this->slug,
			'label'         => $this->name,
			'title'         => $this->name,
			'header'        => $this->name,
			// 'parent'     => 'woocommerce',
			// 'priority'   => 10,
			// 'capability' => 'manage_options',
			// 'icon'       => 'dashicons-wordpress',
			// 'position'   => 25,
			'sections'      => [
				'job-importer_basic'	=> [
					'id'        => 'job-importer_basic',
					'label'     => __( 'Basic Settings', 'job-importer' ),
					'icon'      => 'dashicons-admin-tools',
					'color'		=> '#4c3f93',
					// 'sticky'	=> false,
					'fields'    => [
						'upload_json_file' => [
							'id'      	=> 'upload_json_file',
							'label'     => __( 'Upload File' ),
							'type'      => 'file',
							'upload_button'     => __( 'Choose File', 'job-importer' ),
							'select_button'     => __( 'Select File', 'job-importer' ),
							'desc'      => __( 'Please upload json file.', 'job-importer' ),
							// 'class'     => '',
							'disabled'  => false, // true|false
							'default'   => ''
						],
					]
				],
			],
		];

		new \codexpert\product\Settings( $settings );
	}
	
	public function tab_content( $section ) {
		if( 'job-importer_help' == $section['id'] ) {
			// printf( __( 'If you need further assistance, please <a href="%s" target="_blank">reach out to us</a>!', 'job-importer' ), 'https://codexpert.io' );
		}
	}
}