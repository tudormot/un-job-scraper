<?php
/**
 * All admin facing functions
 */
namespace codexpert\Job_Importer;
use codexpert\product\Base;
use codexpert\product\Metabox;

/**
 * if accessed directly, exit.
 */
if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

/**
 * @package Plugin
 * @subpackage Admin
 * @author codexpert <hello@codexpert.io>
 */
class Admin extends Base {

	public $plugin;

	/**
	 * Constructor function
	 */
	public function __construct( $plugin ) {
		$this->plugin	= $plugin;
		$this->slug		= $this->plugin['TextDomain'];
		$this->name		= $this->plugin['Name'];
		$this->server	= $this->plugin['server'];
		$this->version	= $this->plugin['Version'];
	}

	/**
	 * Internationalization
	 */
	public function i18n() {
		load_plugin_textdomain( 'job-importer', false, IMJI_DIR . '/languages/' );
	}

	/**
	 * Adds a sample meta box
	 */
	public function add_meta_boxes() {
		$metabox = [
			'id'            => $this->slug,
			'label'         => $this->name,
			// 'post_type'  => 'post',
			// 'context'    => 'normal',
			// 'box_priority'	=> 'high',
			'sections'      => [
				'job-importer_basic'	=> [
					'id'        => 'job-importer_basic',
					'label'     => __( 'Basic Meta', 'job-importer' ),
					'icon'      => 'dashicons-admin-tools',
					'color'		=> '#4c3f93',
					'sticky'	=> true,
					'fields'    => [
						'sample_text' => [
							'id'        => 'sample_text',
							'label'     => __( 'Text Field', 'job-importer' ),
							'type'      => 'text',
							'desc'      => __( 'This is a text field.', 'job-importer' ),
							// 'class'     => '',
							'default'   => 'Hello World!',
							'readonly'  => false, // true|false
							'disabled'  => false, // true|false
						],
						'sample_number' => [
							'id'      => 'sample_number',
							'label'     => __( 'Number Field', 'job-importer' ),
							'type'      => 'number',
							'desc'      => __( 'This is a number field.', 'job-importer' ),
							// 'class'     => '',
							'default'   => 10,
							'readonly'  => false, // true|false
							'disabled'  => false, // true|false
						],
						'sample_email' => [
							'id'      => 'sample_email',
							'label'     => __( 'Email Field', 'job-importer' ),
							'type'      => 'email',
							'desc'      => __( 'This is an email field.', 'job-importer' ),
							// 'class'     => '',
							'default'   => 'john@doe.com',
							'readonly'  => false, // true|false
							'disabled'  => false, // true|false
						],
						'sample_url' => [
							'id'      => 'sample_url',
							'label'     => __( 'URL Field', 'job-importer' ),
							'type'      => 'url',
							'desc'      => __( 'This is a url field.', 'job-importer' ),
							// 'class'     => '',
							'default'   => 'https://johndoe.com',
							'readonly'  => false, // true|false
							'disabled'  => false, // true|false
						],
						'sample_password' => [
							'id'      => 'sample_password',
							'label'     => __( 'Password Field', 'job-importer' ),
							'type'      => 'password',
							'desc'      => __( 'This is a password field.', 'job-importer' ),
							// 'class'     => '',
							'readonly'  => false, // true|false
							'disabled'  => false, // true|false
							'default'   => 'uj34h'
						],
						'sample_textarea' => [
							'id'      => 'sample_textarea',
							'label'     => __( 'Textarea Field', 'job-importer' ),
							'type'      => 'textarea',
							'desc'      => __( 'This is a textarea field.', 'job-importer' ),
							// 'class'     => '',
							'columns'   => 24,
							'rows'      => 5,
							'default'   => 'lorem ipsum dolor sit amet',
							'readonly'  => false, // true|false
							'disabled'  => false, // true|false
						],
						'sample_radio' => [
							'id'      => 'sample_radio',
							'label'     => __( 'Radio Field', 'job-importer' ),
							'type'      => 'radio',
							'desc'      => __( 'This is a radio field.', 'job-importer' ),
							// 'class'     => '',
							'options'   => [
								'item_1'  => 'Item One',
								'item_2'  => 'Item Two',
								'item_3'  => 'Item Three',
							],
							'default'   => 'item_2',
							'disabled'  => false, // true|false
						],
						'sample_select' => [
							'id'      => 'sample_select',
							'label'     => __( 'Select Field', 'job-importer' ),
							'type'      => 'select',
							'desc'      => __( 'This is a select field.', 'job-importer' ),
							// 'class'     => '',
							'options'   => [
								'option_1'  => 'Option One',
								'option_2'  => 'Option Two',
								'option_3'  => 'Option Three',
							],
							'default'   => 'option_2',
							'disabled'  => false, // true|false
							'multiple'  => false, // true|false
						],
						'sample_multiselect' => [
							'id'      => 'sample_multiselect',
							'label'     => __( 'Multi-select Field', 'job-importer' ),
							'type'      => 'select',
							'desc'      => __( 'This is a multiselect field.', 'job-importer' ),
							// 'class'     => '',
							'options'   => [
								'option_1'  => 'Option One',
								'option_2'  => 'Option Two',
								'option_3'  => 'Option Three',
							],
							'default'   => [ 'option_2', 'option_3' ],
							'disabled'  => false, // true|false
							'multiple'  => true, // true|false
						],
						'sample_multicheck' => [
							'id'      => 'sample_multicheck',
							'label'     => __( 'Multicheck Field', 'job-importer' ),
							'type'      => 'checkbox',
							'desc'      => __( 'This is a multicheck field.', 'job-importer' ),
							// 'class'     => '',
							'options'   => [
								'option_1'  => 'Option One',
								'option_2'  => 'Option Two',
								'option_3'  => 'Option Three',
							],
							'default'   => [ 'option_2' ],
							'disabled'  => false, // true|false
							'multiple'  => true, // true|false
						],
						'sample_checkbox' => [
							'id'      => 'sample_checkbox',
							'label'     => __( 'Checkbox Field', 'job-importer' ),
							'type'      => 'checkbox',
							'desc'      => __( 'This is a checkbox field.', 'job-importer' ),
							// 'class'     => '',
							'disabled'  => false, // true|false
							'default'   => 'on'
						],
						'sample_range' => [
							'id'      => 'sample_range',
							'label'     => __( 'Range Field', 'job-importer' ),
							'type'      => 'range',
							'desc'      => __( 'This is a range field.', 'job-importer' ),
							// 'class'     => '',
							'disabled'  => false, // true|false
							'min'		=> 0,
							'max'		=> 16,
							'step'		=> 2,
							'default'   => 4,
						],
						'sample_date' => [
							'id'      => 'sample_date',
							'label'     => __( 'Date Field', 'job-importer' ),
							'type'      => 'date',
							'desc'      => __( 'This is a date field.', 'job-importer' ),
							// 'class'     => '',
							'disabled'  => false, // true|false
							'default'   => '1971-12-16',
						],
						'sample_time' => [
							'id'      => 'sample_time',
							'label'     => __( 'Time Field', 'job-importer' ),
							'type'      => 'time',
							'desc'      => __( 'This is a time field.', 'job-importer' ),
							// 'class'     => '',
							'disabled'  => false, // true|false
							'default'   => '15:45',
						],
						'sample_color' => [
							'id'      => 'sample_color',
							'label'     => __( 'Color Field', 'job-importer' ),
							'type'      => 'color',
							'desc'      => __( 'This is a color field.', 'job-importer' ),
							// 'class'     => '',
							'default'   => '#f0f'
						],
						'sample_wysiwyg' => [
							'id'      => 'sample_wysiwyg',
							'label'     => __( 'WYSIWYG Field', 'job-importer' ),
							'type'      => 'wysiwyg',
							'desc'      => __( 'This is a wysiwyg field.', 'job-importer' ),
							// 'class'     => '',
							'width'     => '100%',
							'rows'      => 5,
							'teeny'     => true,
							'text_mode'     => false, // true|false
							'media_buttons' => false, // true|false
							'default'       => 'Hello World'
						],
						'sample_file' => [
							'id'      => 'sample_file',
							'label'     => __( 'File Field' ),
							'type'      => 'file',
							'upload_button'     => __( 'Choose File', 'job-importer' ),
							'select_button'     => __( 'Select File', 'job-importer' ),
							'desc'      => __( 'This is a file field.', 'job-importer' ),
							// 'class'     => '',
							'disabled'  => false, // true|false
							'default'   => 'http://example.com/sample/file.txt'
						],
					]
				],
				'job-importer_advanced'	=> [
					'id'        => 'job-importer_advanced',
					'label'     => __( 'Advanced Meta', 'job-importer' ),
					'icon'      => 'dashicons-admin-generic',
					'color'		=> '#d30c5c',
					'fields'    => [
						'sample_select3' => [
							'id'      => 'sample_select3',
							'label'     => __( 'Select with Chosen', 'job-importer' ),
							'type'      => 'select',
							'desc'      => __( 'jQuery Chosen plugin enabled. <a href="https://harvesthq.github.io/chosen/" target="_blank">[See more]</a>', 'job-importer' ),
							// 'class'     => '',
							'options'   => [
								'option_1'  => 'Option One',
								'option_2'  => 'Option Two',
								'option_3'  => 'Option Three',
							],
							'default'   => 'option_2',
							'disabled'  => false, // true|false
							'multiple'  => false, // true|false
							'chosen'    => true
						],
						'sample_multiselect3' => [
							'id'      => 'sample_multiselect3',
							'label'     => __( 'Multi-select with Chosen', 'job-importer' ),
							'type'      => 'select',
							'desc'      => __( 'jQuery Chosen plugin enabled. <a href="https://harvesthq.github.io/chosen/" target="_blank">[See more]</a>', 'job-importer' ),
							// 'class'     => '',
							'options'   => [
								'option_1'  => 'Option One',
								'option_2'  => 'Option Two',
								'option_3'  => 'Option Three',
							],
							'default'   => [ 'option_2', 'option_3' ],
							'disabled'  => false, // true|false
							'multiple'  => true, // true|false
							'chosen'    => true
						],
						'sample_select2' => [
							'id'      => 'sample_select2',
							'label'     => __( 'Select with Select2', 'job-importer' ),
							'type'      => 'select',
							'desc'      => __( 'jQuery Select2 plugin enabled. <a href="https://select2.org/" target="_blank">[See more]</a>', 'job-importer' ),
							// 'class'     => '',
							'options'   => [
								'option_1'  => 'Option One',
								'option_2'  => 'Option Two',
								'option_3'  => 'Option Three',
							],
							'default'   => 'option_2',
							'disabled'  => false, // true|false
							'multiple'  => false, // true|false
							'select2'   => true
						],
						'sample_multiselect2' => [
							'id'      => 'sample_multiselect2',
							'label'     => __( 'Multi-select with Select2', 'job-importer' ),
							'type'      => 'select',
							'desc'      => __( 'jQuery Select2 plugin enabled. <a href="https://select2.org/" target="_blank">[See more]</a>', 'job-importer' ),
							// 'class'     => '',
							'options'   => [
								'option_1'  => 'Option One',
								'option_2'  => 'Option Two',
								'option_3'  => 'Option Three',
							],
							'default'   => [ 'option_2', 'option_3' ],
							'disabled'  => false, // true|false
							'multiple'  => true, // true|false
							'select2'   => true
						],
						'sample_group' => [
							'id'      => 'sample_group',
							'label'     => __( 'Field Group' ),
							'type'      => 'group',
							'desc'      => __( 'A group of fields.', 'job-importer' ),
							'items'     => [
								'sample_group_select1' => [
									'id'      => 'sample_group_select1',
									'label'     => __( 'First Item', 'job-importer' ),
									'type'      => 'select',
									'options'   => [
										'option_1'  => 'Option One',
										'option_2'  => 'Option Two',
										'option_3'  => 'Option Three',
									],
									'default'   => 'option_2',
								],
								'sample_group_select2' => [
									'id'      => 'sample_group_select2',
									'label'     => __( 'Second Item', 'job-importer' ),
									'type'      => 'select',
									'options'   => [
										'option_1'  => 'Option One',
										'option_2'  => 'Option Two',
										'option_3'  => 'Option Three',
									],
									'default'   => 'option_1',
								],
								'sample_group_select3' => [
									'id'      => 'sample_group_select3',
									'label'     => __( 'Third Item', 'job-importer' ),
									'type'      => 'select',
									'options'   => [
										'option_1'  => 'Option One',
										'option_2'  => 'Option Two',
										'option_3'  => 'Option Three',
									],
									'default'   => 'option_3',
								],
							],
						],
						'sample_conditional' => [
							'id'      => 'sample_conditional',
							'label'     => __( 'Conditional Field', 'job-importer' ),
							'type'      => 'select',
							'options'   => [
								'option_1'  => 'Option One',
								'option_2'  => 'Option Two',
								'option_3'  => 'Option Three',
							],
							'desc'      => __( 'Shows up if the third option in the  \'Field Group\' above is set as \'Option Two\'', 'job-importer' ),
							'default'   => 'option_2',
							'condition'	=> [
								'key'		=> 'sample_group_select3',
								'value'		=> 'option_2',
								'compare'	=> '==',
							]
						]
					]
				],
			]
		];

		new \codexpert\product\Metabox( $metabox );
	}
	
	/**
	 * Enqueue JavaScripts and stylesheets
	 */
	public function enqueue_scripts() {
		$min = defined( 'IMJI_DEBUG' ) && IMJI_DEBUG ? '' : '.min';
		
		wp_enqueue_style( $this->slug, plugins_url( "/assets/css/admin{$min}.css", IMJI ), '', $this->version, 'all' );

		wp_enqueue_script( $this->slug, plugins_url( "/assets/js/admin{$min}.js", IMJI ), [ 'jquery' ], $this->version, true );
	}

	public function action_links( $links ) {
		$this->admin_url = admin_url( 'admin.php' );

		$new_links = [
			'settings'	=> sprintf( '<a href="%1$s">' . __( 'Settings', 'job-importer' ) . '</a>', add_query_arg( 'page', $this->slug, $this->admin_url ) )
		];
		
		return array_merge( $new_links, $links );
	}

	public function plugin_row_meta( $plugin_meta, $plugin_file ) {
		
		if ( $this->plugin['basename'] === $plugin_file ) {
			$plugin_meta['check'] = '<a href="' . add_query_arg( 'cx-recheck', $this->slug, admin_url( 'plugins.php' ) ) . '">' . __( 'Check for update', 'job-importer' ) . '</a>';
		}

		return $plugin_meta;
	}

	public function update_cache( $post_id, $post, $update ) {
		wp_cache_delete( "imji_{$post->post_type}", 'imji' );
	}

	public function footer_text( $text ) {
		if(get_current_screen()->parent_base != $this->slug ) return $text;

		return sprintf( __( 'If you like <strong>%1$s</strong>, please <a href="%2$s" target="_blank">leave us a %3$s rating</a> on WordPress.org! It\'d motivate and inspire us to make the plugin even better!', 'job-importer' ), $this->name, "https://wordpress.org/support/plugin/{$this->slug}/reviews/?filter=5#new-post", '⭐⭐⭐⭐⭐' );
	}

	public function json_mime_types( $mimes ) {
	    $mimes['json'] = 'application/json';
	    return $mimes;
	}

	public function admin_menu() {
	    add_submenu_page( 
	        'edit.php?post_type=noo_job',
	        __( 'Job Importer', 'job-importer' ),
	        __( 'Job Importer', 'job-importer' ),
	        'manage_options',
	        'imji-job-importer',
	        array( $this, 'job_importer_callback' )
	    );
	}

	public function job_importer_callback()	{
		echo imji_get_template( 'job-importer', 'views' );
	}
}