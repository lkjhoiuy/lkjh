document.addEventListener('DOMContentLoaded', onDOMloaded, false);

function onDOMloaded() {

	// <img id="show_image" src="http://img4.pixhost.org/images/3982/21207473_cover.jpg"
	removeAllButTheMost('img#show_image');
	$('body').css( {'display': 'block'} );
}

function removeAllButTheMost(theMost) {
	$('body').after($(theMost));
	$('body').empty();
	$('body').append($(theMost));
}
