<div class="wrap imji-wrap">
	<div class="imji-job-importer-wrap">
		
		<div class="imji-button-wrap">
			<form action="" id="imji-job-importer-form" method="post" enctype="multipart/form-data">
				<input type="hidden" name="action" value="job-importer">

				<input type="file" name="job" id="imji-job" class="imji-job-file-input">

				<p class="imji-job-importer-submit">
					<input type="submit" value="<?php _e( 'Upload File', 'job-importer' ); ?>" class="button imji-submit-button" />
				</p>
			</form>

			<div class="imji-message" style="display: none;">
				<p></p>
			</div>
		</div>
		
	</div>
</div>
