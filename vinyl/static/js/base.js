$(document).ready(function() {
	$('.lang_select').change(function() {
		var lang_url = '/vinyl/lang/' + $(this).val();
		jQuery.ajax({
			url: lang_url,
			success: function(){
				location.reload();
		  	}
		});
	});
	
	$('#addtolist').click(function(){
		ids = getCheckedIDArr();
		if(!ids) {
			alert("Please select some records."); 
			return false;
		}
		$.ajax({
			url: '/vinyl/list/add/' + $('#listtype').val() + "/" + ids.join("_"),
			success: function(response) {
				alert(response);
			},
			error: function() {
				alert('Error');
			}
			
		});
	});
	
	$('#addtoplaylist').click(function(){
		ids = getCheckedIDArr();
		if(!ids) {
			alert("Please select some tracks."); 
			return false;
		}
		
		$.ajax({
			url: '/vinyl/playlist/add/' + $('#playlists').val() + "/" + ids.join("__"),
			success: function(response) {
				alert(response);
			},
			error: function() {
				alert('Error');
			}
			
		});
	});
	
	getCheckedIDArr = function(ids) {
		var ids = []
		var idchk = $('input:checked');
		if(idchk.length == 0) {return false;}
		idchk.each(function(){ ids.push($(this).attr("id")); });
		
		return ids;
	};
	
	$('#createplaylist').click(function(){
		ids = getCheckedIDArr();
		if(!ids) {
			alert("Please select some tracks."); 
			return false;
		}
		var listname = prompt('Enter playlist name');
		
		$.ajax({
			url: '/vinyl/playlist/new/' + encodeURI(listname) + "/" + ids.join("__"),
			success: function() {
				alert('Created');
			},
			error: function() {
				alert('Error');
			}
			
		});
	});
	
	$('#rm-rec-lib').click(function(){
		ids = getCheckedIDArr();
		if(!ids) {
			alert("Please select some records.");
			return false;
		}
		$.ajax({
			url: '/vinyl/library/delete/' + ids.join("_"),
			success: function() {
				alert('Deleted');
				document.location.reload();
			},
			error: function() {
				alert('Error');
			}
			
		});
	});
	
	$('#promote-owned').click(function(){
		ids = getCheckedIDArr();
		if(!ids) {
			alert("Please select some records.");
			return false;
		}
		$.ajax({
			url: '/vinyl/library/promote/' + ids.join("_"),
			success: function() {
				document.location.reload();
			},
			error: function() {
				alert('Error');
			}
			
		});
	});
	
	$('#publish-now').click(function(){
		$.ajax({
			url: '/vinyl/playlist/publish/' + $(this).attr("pid"),
			success: function(response) {
				alert(response);
				document.location.reload();
			},
			error: function(response) {
				alert(response)
			}
		});
		return false;
	});
	
	$('#lightbox').ajaxStart(function(){
		$(this).show();
	});

	$('#lightbox').ajaxStop(function(){
		$(this).hide();
	});
		
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