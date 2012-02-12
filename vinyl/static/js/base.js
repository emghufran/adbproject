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
	
	//star rating functionality
	$(document).ready(function() {
        
        $('.rate_widget').each(function(i) {
            var widget = this;
            var out_data = {
                widget_id : $(widget).attr('id'),
                fetch: 1,
                csrfmiddlewaretoken : $('input[name="csrfmiddlewaretoken"]').first().val()
            };
            $.post(
                '/vinyl/handle_rating/',
                out_data,
                function(INFO) {
                    $(widget).data( 'fsr', INFO );
                    set_votes(widget);
                },
                'json'
            );
        });
    

        $('.ratings_stars').hover(
            // Handles the mouseover
            function() {
                $(this).prevAll().andSelf().addClass('ratings_over');
                $(this).nextAll().removeClass('ratings_vote'); 
            },
            // Handles the mouseout
            function() {
                $(this).prevAll().andSelf().removeClass('ratings_over');
                // can't use 'this' because it wont contain the updated data
                set_votes($(this).parent());
            }
        );
        
        
        // This actually records the vote
        $('.ratings_stars').bind('click', function() {
            var star = this;
            var widget = $(this).parent();
            
            var clicked_data = {
                clicked_on : $(star).attr('class'),
                widget_id : $(star).parent().attr('id'),
                csrfmiddlewaretoken : $('input[name="csrfmiddlewaretoken"]').first().val()
            };
            $.post(
                '/vinyl/handle_rating/',
                clicked_data,
                function(INFO) {
                    widget.data( 'fsr', INFO );
                    set_votes(widget);
                },
                'json'
            ); 
        });
        
        
        
    });

    function set_votes(widget) {

        var avg = $(widget).data('fsr').whole_avg;
        var votes = $(widget).data('fsr').number_votes;
        var exact = $(widget).data('fsr').dec_avg;
    
        window.console && console.log('and now in set_votes, it thinks the fsr is ' + $(widget).data('fsr').number_votes);
        
        $(widget).find('.star_' + avg).prevAll().andSelf().addClass('ratings_vote');
        $(widget).find('.star_' + avg).nextAll().removeClass('ratings_vote'); 
        $(widget).find('.total_votes').text( votes + ' votes recorded (' + exact + ' rating)' );
    }