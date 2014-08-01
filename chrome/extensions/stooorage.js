document.addEventListener('DOMContentLoaded', onDOMloaded, false);

function onDOMloaded() {
	
	// <div id="page_body">
	// <img onload="scale(this);" onclick="scale(this);" src="http://img2.stooorage.com/images/2771/11309139_btra12884_3000_hw.jpg"
	removeAllButTheMost('div#page_body img');
	$('body').css( {'display': 'block'} );
}

function removeAllButTheMost(theMost) {
	$('head').empty();
	$('body').after($(theMost));
	$('body').empty();
	$('body').append($(theMost));
}
