<?php
/**
 * All AJAX related functions
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
 * @subpackage AJAX
 * @author codexpert <hello@codexpert.io>
 */
class AJAX extends Base {

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

	public function job_importer() {

		$response = array();

		$file 		= $_FILES;
		$job 		= $file['job'];
		$type 		= $job['type'];
		$tmp_file 	= $job['tmp_name'];
		
		if( $type != 'application/json' ) {
			$response['message'] = __( 'Please choose a json file.', 'json-importer' );
			wp_send_json( $response );
		}

		$data 		= json_decode( file_get_contents( $tmp_file ) );
		$updated 	= 0;
		foreach ( $data->jobs as $job ) {

		 	$post_data = array(
			  	'post_title'	=> $job->title,
			  	'post_status'   => 'publish',
			  	'post_type'	  	=> 'noo_job',
			  	'post_content' 	=> $job->extra_information,
			  	'meta_input' 	=> [
					'_closing' 	=> strtotime( $job->closing_date ),
					'_custom_application_url' => $job->original_job_link,
				],
			);

			// Insert the post
			$post_id = wp_insert_post( $post_data );

			wp_set_post_terms( $post_id, $job->tags, 'job_tag' );

			$updated++;
		}

		$response['status']     = 1;
        $response['message']    = sprintf( __( '%d Posts Created.', 'badbugs' ), $updated );

        wp_send_json( $response );
	}

}