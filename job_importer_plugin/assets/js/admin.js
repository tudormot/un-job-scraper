jQuery(function($){
	$('#imji-job-importer-form').submit(function(e){
		e.preventDefault()

		var $dis = $(this)
		var $btn_text = $('.imji-submit-button').val()
		$('.imji-submit-button').val('Uploading..').attr('disabled',true)
		$('.imji-message').hide()
		$('.imji-progress-outline').show()
		var csv_data = $('#imji-job').prop('files')[0];
	    var formData = new FormData();                 
	    formData.append( 'job', csv_data );
	    formData.append( 'action', 'job-importer' );

		$.ajax({
			url: ajaxurl,
			data: formData,
			type: 'POST',
			dataType : "json",
			processData: false,
			contentType: false,
			cache: false,
			success: function( resp ) {
				console.log(resp);
				$('.imji-submit-button').val($btn_text).attr('disabled',false)
				$('.imji-message > p').html(resp.message)
				$('.imji-message').show()
			}
		})
	})
})