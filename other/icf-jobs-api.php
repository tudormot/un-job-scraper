<?php

/*
Plugin Name: Jobs API endpoints.
Plugin URI:  https://www.fiverr.com/ketion/
Description: Add API endpoints to bulk create/delete jobs.
Version:     1.0.0
Author:      Ketion
Author URI:  https://www.fiverr.com/ketion/
License:     GPL-2.0+
License URI: http://www.gnu.org/licenses/gpl-2.0.txt
Text Domain: icf-jobs-api

TUDOR: this code not used in this projet per-se, just kept here for referece
*/

defined('ABSPATH') || exit;

if ( ! defined('ICF_Jobs_API_FILE')) {
    define('ICF_Jobs_API_FILE', __FILE__);
}

/**
 * Class ICF_Jobs_API_Main
 *
 * @property string $namespace
 * @property mixed $instance
 */
class ICF_Jobs_API_Main
{
    
    /**
     * Class instance.
     *
     * @var ICF_Jobs_API_Main instance
     */
    protected static $instance = false;
    /**
     * @var string $namespace Rest route namespace
     */
    private $namespace = 'icf-jobs';
    
    /**
     * Define the core functionality of the plugin.
     */
    public function __construct()
    {
        $this->run();
    }
    
    /**
     * Run all hooks within WordPress.
     *
     * @since    1.0.0
     */
    public function run()
    {
        /**
         * Register rest routes
         */
        add_action('rest_api_init', array($this, 'register_routes'));
    }
    
    /**
     * Get class instance
     */
    public static function get_instance()
    {
        if ( ! self::$instance) {
            self::$instance = new self();
        }
        
        return self::$instance;
    }
    
    /**
     * Register api routes.
     */
    public function register_routes()
    {
        register_rest_route('wp/v2', $this->namespace, array(
            [
                'methods'             => WP_REST_Server::CREATABLE,
                'callback'            => array($this, 'create'),
                'permission_callback' => array($this, 'check_permission'),
                'args'                => [
                    'jobs' => [
                        'required'    => true,
                        'description' => __('List of jobs.', 'icf-jobs-api'),
                        'type'        => 'array',
                        'items' => [
                            'type' => 'object',
                            'properties' => array(
                                'id' => array(
                                    'type'   => 'integer',
                                    'required' => true,
                                ),
                                'title' => array(
                                    'type'   => 'string',
                                    'required' => true,
                                ),
                                'extra_information' => array(
                                    'type'   => 'string',
                                    'required' => true,
                                ),
                                'closing_date' => array(
                                    'type'   => 'string',
                                    'required' => true,
                                ),
                            ),
                        ]
                    ],
                ]
            ],
            [
                'methods'             => WP_REST_Server::DELETABLE,
                'callback'            => array($this, 'delete'),
                'permission_callback' => array($this, 'check_permission'),
                'args'                => [
                    'jobs' => [
                        'required'    => true,
                        'description' => __('List of jobs.', 'icf-jobs-api'),
                        'type'       => 'array',
                        'items' => [
                            'type' => 'object',
                            'properties' => array(
                                'id' => array(
                                    'type'   => 'integer',
                                    'required' => true,
                                ),
                            ),
                        ]
                    ],
                ]
            ],
        ));
    }
    
    /**
     * Add list of jobs.
     *
     * @param  WP_REST_Request  $request
     *
     * @return array
     */
    public function create(WP_REST_Request $request)
    {
        $jobs = $request->get_param('jobs');
        
        if ( ! is_array($jobs) || empty($jobs)) {
            return new WP_REST_Response([
                'error' => __('Provide list of jobs.', 'icf-jobs-api')
            ], 403);
        }
        
        foreach ($jobs as $job) {

            $args = array(
                'post_type'   => 'noo_job',
                'post_status' => 'publish',
                'fields'      => 'ids',
                'meta_query'  => array(
                    array(
                        'key' => 'icf_job_id',
                        'value' => $job['id'],
                        'compare' => '=',
                    )
                )
            );
            
            $exists = new WP_Query($args);

            if ($exists->post_count > 0) {
                $data[] = [
                    'id'      => $job['id'],
                    'error'   => true,
                    'type'    => 'exists',
                    'message' => sprintf(__('Job with id:%d exists', 'icf-jobs-api'), $job['id'])
                ];
            } else {
                $post_id = wp_insert_post(
                    array(
                        'post_title'   => $job['title'],
                        'post_type'    => 'noo_job',
                        'post_status'  => 'publish',
                        'post_content' => $job['extra_information']
                    )
                );
                
                if (is_wp_error($post_id)) {
                    $data[] = [
                        'id'      => $job['id'],
                        'error'   => true,
                        'type'    => 'failed',
                        'message' => sprintf(__('Failed to add job with id:%d.', 'icf-jobs-api'), $job['id'])
                    ];
                    
                    continue;
                }

                $organisation_args = array(
                    'post_type'   => 'noo_company',
                    'post_status' => 'publish',
                    'title'       => $job['organisation'],
                    'fields'      => 'ids',
                );
                
                $organisation_exists = new WP_Query($organisation_args);
                
                if ($organisation_exists->post_count > 0) {
                    $organization = $organisation_exists->posts[0];
                } else {
                    $organization = wp_insert_post([
                        'post_title'  => $job['organisation'],
                        'post_status' => 'publish',
                        'post_type'   => 'noo_company'
                    ]);
                }
                
                // set id
                update_post_meta($post_id, 'icf_job_id', $job['id']);
                // set organisation
                update_post_meta($post_id, '_company_id', $organization);
                // set original_job_link
                update_post_meta($post_id, '_custom_application_url', $job['original_job_link']);
                // set grade
                update_post_meta($post_id, '_noo_job_field__grade', $job['grade']);
                // set office
                update_post_meta($post_id, '_noo_job_field__office', $job['office']);
                // set closing_date
                $datetime = DateTime::createFromFormat('d.m.Y', $job['closing_date']);
                update_post_meta($post_id, '_expires', $datetime->getTimestamp());
                
                // set job_type
                wp_set_object_terms($post_id, array($job['job_type']), 'job_type');
                
                // set tags
                wp_set_post_terms($post_id, $job['tags'], 'job_tag');

                // set categories
                $parent_cat = term_exists('All', 'job_category', 0);
                if ( ! $parent_cat) {
                    $parent_cat = wp_insert_term('All', 'job_category', array('parent' => 0));
                }
                $parent_cat = is_array($parent_cat) ? $parent_cat['term_id'] : $parent_cat;
                $parent_cat = intval($parent_cat);

                $categories = array();
                foreach($job['tags'] as $tag) {
                    $cat = term_exists($tag, 'job_category', $parent_cat);
                    if ( ! $cat) {
                        $cat = wp_insert_term($tag, 'job_category', array('parent' => $parent_cat));
                    }
                    $cat = is_array($cat) ? $cat['term_id'] : $cat;
                    $categories[] = $cat;
                }
                $categories = array_map( 'intval', $categories );
                $categories = array_unique( $categories );
                wp_set_post_terms($post_id, $categories, 'job_category');
                
                // set location
                $country = get_terms([
                    'name'     => $job['country'],
                    'taxonomy' => 'job_location',
                    'fields'   => 'ids',
                    'parent'   => 0,
                ]);
                
                $country = term_exists($job['country'], 'job_location', 0);
                if ( ! $country) {
                    $country = wp_insert_term($job['country'], 'job_location', array('parent' => 0));
                }
                $country = is_array($country) ? $country['term_id'] : $country;
                $country = intval($country);
                
                $city = term_exists($job['city'], 'job_location', $country);
                if ( ! $city) {
                    $city = wp_insert_term($job['city'], 'job_location', array('parent' => $country));
                }
                $city = is_array($city) ? $city['term_id'] : $city;
                $city = intval($city);
                
                wp_set_post_terms($post_id, array($city), 'job_location');

                $data[] = [
                    'id'      => $job['id'],
                    'success' => true,
                    'message' => sprintf(__('Job with id:%d added successfully.', 'icf-jobs-api'), $job['id'])
                ];
            }
        }
        
        return new WP_REST_Response($data, 200);
    }
    
    /**
     * Delete list of jobs.
     *
     * @param  WP_REST_Request  $request
     *
     * @return array
     */
    public function delete(WP_REST_Request $request)
    {
        $jobs = $request->get_param('jobs');
        
        if ( ! is_array($jobs) || empty($jobs)) {
            return new WP_REST_Response([
                'error' => __('Provide list of jobs ids to delete.', 'icf-jobs-api')
            ], 403);
        }

        foreach ($jobs as $job) {

            $args = array(
                'post_type'   => 'noo_job',
                'post_status' => 'publish',
                'fields'      => 'ids',
                'meta_query'  => array(
                    array(
                        'key' => 'icf_job_id',
                        'value' => $job['id'],
                        'compare' => '=',
                    )
                )
            );
            
            $exists = new WP_Query($args);

            if ($exists->post_count > 0) {
                foreach($exists->posts as $jobId) {
                    $deleted = wp_delete_post($jobId, true);
                    if($deleted) {
                        $data[] = [
                            'id'      => $job['id'],
                            'success' => true,
                            'message' => sprintf(__('Job with id:%d deleted successfully.', 'icf-jobs-api'), $job['id'])
                        ];
                    } else {
                        $data[] = [
                            'id'      => $job['id'],
                            'error'   => true,
                            'type'    => 'failed',
                            'message' => sprintf(__('Failed to delete job with id:%d.', 'icf-jobs-api'), $job['id'])
                        ];
                    }
                }
            } else {
                $data[] = [
                    'id'      => $job['id'],
                    'error'   => true,
                    'type'    => 'not_exists',
                    'message' => sprintf(__('Job with id:%d doesn\'t exist.', 'icf-jobs-api'), $job['id'])
                ];
            }
        }

        return new WP_REST_Response($data, 200);
    }
    
    /**
     * Check if a given request has access.
     *
     * @param  WP_REST_Request  $request  Full data about the request.
     *
     * @return WP_Error|boolean
     */
    public function check_permission($request)
    {
        if ( ! current_user_can('manage_options')) {
            return false;
        }
        
        return true;
    }
    
}

ICF_Jobs_API_Main::get_instance();
