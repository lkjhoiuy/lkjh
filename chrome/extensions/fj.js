document.addEventListener('DOMContentLoaded', onload, false);

function Set() {
	this.date = '';  // 2014-01-27
	this.id = '';  // C05817BD3798F7645158B1D7B1E49710
	this.model = '';  // Milena D
	this.modelId = '';  // 22EA835B150BD8B234567D90E1290D81
	this.title = '';  // Maituse
	this.artist = '';  // Erik Latika
	this.type = 'img';
	
	this.__defineGetter__('cover', function() { return this._getCover(); });
	this.__defineGetter__('tcover', function() { return this._getTCover(); });
	this.__defineGetter__('wcover', function() { return this._getWCover(); });
	this.__defineGetter__('twcover', function() { return this._getTWCover(); });
	this.__defineGetter__('sample', function() { return this._getSample(); });
	
	this.__defineGetter__('dateYear', function() { return this._getDateYear(); });
	this.__defineGetter__('dateMonth', function() { return this._getDateMonth(); });
	this.__defineGetter__('dateDay', function() { return this._getDateDay(); });
	this.__defineGetter__('dateFmt', function() { return this._getDateFmt(); });
	
	this.__defineGetter__('modelFmt', function() { return this._getModelFmt(); });
	this.__defineGetter__('titleFmt', function() { return this._getTitleFmt(); });
	this.__defineGetter__('artistFmt', function() { return this._getArtistFmt(); });
	
	this.__defineGetter__('searchPattern', function() { return this._getSearchPattern(); });
}
Set.prototype = {
	_getDateYear: function () {
		if (!this.date) return '';
		alert(this.date);
		return this.date.getFullYear();
	},
	_getDateMonth: function () {
		if (!this.date) return '';
		var m = this.date.getMonth()+1;
		if (m < 10) return '0'+m;
		return m;
	},
	_getDateDay: function () {
		if (!this.date) return '';
		var d = this.date.getDate();
		if (d < 10) return '0'+d;
		return d;
	},
	_getDateFmt: function () {
		if (!this.date) return '';
		return this.dateYear + '-' + this.dateMonth + '-' + this.dateDay;
	},
	_getModelFmt: function () {
		if (!this.model) return '';
		return this.model.toLowerCase().replace(/ /g, '-');
	},
	_getTitleFmt: function () {
		if (!this.title) return '';
		return this.title.toLowerCase().replace(/ /g, '-');
	},
	_getArtistFmt: function () {
		if (!this.artist) return '';
		var a = this.artist.toLowerCase().split(' ');
		if (a.length < 2) return a;
		return a.shift()[0] + '-' + a.join('-');
	},
	_getCover: function () {
		if (this._cover) return this._cover;
		if (!this.id) return '';
		return this._cover = 'http://m1.femjoy.com/u/updates/' + this.id + '/cover2_642x642.jpg';
	},
	_getTCover: function () {
		if (this._tcover) return this._tcover;
		if (!this.id) return '';
		return this._tcover = 'http://m1.femjoy.com/u/updates/' + this.id + '/cover2_150x150.jpg';
	},
	_getWCover: function () {
		if (this._wcover) return this._wcover;
		if (!this.id) return '';
		return this._wcover = 'http://m1.femjoy.com/u/updates/' + this.id + '/cover2_970x463.jpg';
	},
	_getTWCover: function () {
		if (this._twcover) return this._twcover;
		if (!this.id) return '';
		return this._twcover = 'http://m1.femjoy.com/u/updates/' + this.id + '/cover2_314x150.jpg';
	},
	_getSample: function () {
		if (this._sample) return this._sample;
		if (!this.id) return '';
		return this._sample = '';
	},
	_getSearchPattern: function () {
		if (this._search) return this._search;
		if (!this.title) return '';
		return this._search = this.model.split(' ').concat(this.title.split(' ')).join('+');
	}
}

function onload() {
	removeAllButTheMost();
	removeMore();
	
	// var urls = window.location.href.split('/');
	// var dateurl = urls[urls.length-3] + '-' + urls[urls.length-2];
	var dateurl = "";
	$('head').empty().append(
		$('<title>').text('FJ ' + dateurl)
	);
	
	var data = $('div.span-1').map(function() {
		return doScrap($(this), 'img');
	});
	$.merge(data, $('div.span-2').map(function() {
		return doScrap($(this), 'vid');
	}));
	
	$('body').empty();
	$('body').append(
		data.map(function() {
			return newPres(this);
		}).get()
	);
	$('body').css( {'display': 'block'} );
}

function doScrap($set, type) {
	var s = new Set();
	
	var d = $('h6', $set).text();  // January 26, 2014
	s.date = new Date(d);
	
	s.id = $('a[href^="/sets"]', $set).attr('href').match(/\/sets\/(.+)/)[1];
	s.model = $('a[href^="/models"]', $set).text();
	s.title = $('a[href^="/sets"] img', $set).attr('alt');
	s.artist = $('a[href^="/artists"]', $set).text();
	s.type = type;
	
	return s;
}

function newPres(s) {
	return $('<ul>').append(
		s.type == 'img' ?
			$('<a>', {'href': s.cover, 'target': '_blank'}).append($('<img>', {'src': s.tcover, 'title': s.model + ' - ' + s.title}) ) :
			$('<a>', {'href': s.wcover, 'target': '_blank'}).append($('<img>', {'src': s.twcover, 'title': s.model + ' - ' + s.title}) ),
		$('<li>', {'class': 'set-date'}).text(s.dateFmt),
		$('<li>').text(s.model),
		$('<li>').text(s.title),
		$('<li>').append($('<a>', {'href': 'http://www.metxx.com/search?q=' + s.searchPattern, 'target': '_blank'}).text('metxx') )
	);
}

function removeAllButTheMost(theMost) {
}

function removeMore() {
}

/*
serie, gallery, set, update
date: 2014-01-27
model: Ivy
modelId: 
set: Premiere
setId: 117169_rrw277
artist: 
*/

/*
<div class="span-1 last">
	<div class="set data">
		<div class="addon">
			<a class="button" data-action="add-to-top" data-setcode="117169_rrw277">T<span class="loader"></span></a>
		</div>
		<div class="cover">
			<a href="/sets/117169_rrw277">
				<i class="banderole banderole-today"></i>
				<img src="http://m1.femjoy.com/u/updates/117169_rrw277/cover2_150x150.jpg" width="150" height="150" alt="Premiere">
			</a>
		</div>
		<h6 style="color:#E0C1E4">January 29, 2014</h6>
		<p style="height:75px;">Premiere<br>
			<a href="/models/ivy">Ivy</a><br>
			by <a href="/artists/FEMJOY exclusive">FEMJOY exclusive</a>
		</p>
	</div>
</div>

<div class="span-2 last">
	<div class="set data">
		<div class="addon">
			<a class="button" data-action="add-to-top" data-setcode="116967_tts348">T<span class="loader"></span></a>
		</div>
		<div class="cover">
			<a href="/sets/116967_tts348">
				<i class="banderole banderole-new"></i>
				<img src="http://m1.femjoy.com/u/updates/116967_tts348/cover2_314x150.jpg" width="314" height="150" alt="Timber Place">
			</a>
		</div>
		<h6 style="color:#31C5F6">January 26, 2014</h6>
		<p style="height:75px;">Timber Place<br>
			<a href="/models/lauren">Lauren</a><br>
			by <a href="/artists/FEMJOY Exclusive">FEMJOY Exclusive</a>
		</p>
	</div>
</div>
*/