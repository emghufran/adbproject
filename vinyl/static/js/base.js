$(document).ready(function() {
		$('#add_track_to_record_form').submit(function(e) {
			jQuery("#add_track_submit").attr('disabled', true);
          	jQuery("#add_track_error_div").prepend('<span>Adding track, please wait... </span>');
          	jQuery("#add_track_error_div").html("");
          	jQuery.post("/vinyl/record/associate_track_to_record/", 
          		$("#add_track_to_record_form").serialize(),
          		function(data) {
          			resp_obj = jQuery.parseJSON(data);
          			if(typeof(resp_obj.success) == 'undefined') {
          				if (typeof(resp_obj.track) != 'undefined') {
          					jQuery("#add_track_error_div").prepend("<div>" + resp_obj.track[0].replace("This", "Soundtrack") + "</div>");
          				}
          				if (typeof(resp_obj.order) != 'undefined') {
          					jQuery("#add_track_error_div").prepend("<div>" + resp_obj.order[0].replace("This", "Order") + "</div>");
          				}
          				if (typeof(resp_obj.disc_number) != 'undefined') {
          					jQuery("#add_track_error_div").prepend("<div>" + resp_obj.disc_number[0].replace("This", "Disc number") + "</div>");
          				}
          				if (typeof(resp_obj.general_error) != 'undefined') {
          					jQuery("#add_track_error_div").prepend("<div>" + resp_obj.general_error[0] + "</div>");
          				}
          			} else {
          				document.location.reload();
          			
          			}
          		}
          	);
          	
          	jQuery("#add_track_submit").attr('disabled', false);
          	
          	e.preventDefault(); 
		});
	});