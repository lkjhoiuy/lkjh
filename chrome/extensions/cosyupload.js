document.addEventListener('DOMContentLoaded', onDOMloaded, false);

function onDOMloaded() {
	
	setTimeout(function() {
		// window.location.href = 'https://cosyupload.com/uploads/5315030761f65815f0000dbc';
		// $('span[id$="uploaded_net"] a').html();
		var id = $('span[id$="_uploaded_net"]').attr('id');
		// id = 'link_for_upload_5315030761f65815f0000dbc_uploaded_net'
		id = id.replace(/link_for_upload_(.+)_uploaded_net/, '$1');
		
		// var onclick = $('span[id$="_uploaded_net"] a').attr('onclick');
		// KO $('span[id$="_uploaded_net"] a').trigger('click');
		
		// https://cosyupload.com/uploads/open_link/?upload_id=5315030761f65815f0000dbc&server=uploaded_net
		// TODO GET
		$.getJSON('https://cosyupload.com/uploads/open_link/', {upload_id:id, server:'uploaded_net'}, function(data, textStatus, jqXHR) {
			if (jqXHR.status == 200) {  // textStatus == 'success', jqXHR.status == 200
				// alert(data);
				window.location.href = data.link;
			}
			else {
				alert('ERROR ' + jqXHR.status);
			}
		});
	}, 300);
}
