$('body').css( {'display': 'none'} );

document.addEventListener('DOMContentLoaded', onDOMloaded, false);

function onDOMloaded() {
	// document.removeEventListener('DOMContentLoaded', arguments.callee, false);
	removeAllButTheMost('table#thumbTable');
	removeAllButTheMost('img#fullImage');
	$('td.arylia_bannerCell').css( {'display': 'none'} );
	$('body').css( {'display': 'block'} );
}

function removeAllButTheMost(theMost) {
	// $('head').remove();
	if ($(theMost).length == 0) return;
	
	$('body').after($(theMost));
	$('body').empty();
	$('body').append($(theMost));
}
