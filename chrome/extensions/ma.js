// window.onload fires after all images, frames etc have been loaded.
// window.addEventListener('load', onload, false);
document.addEventListener('DOMContentLoaded', onload, false);

// $('link[rel="stylesheet"]').each(function () {

function onDOMloaded() {
	// document.removeEventListener('DOMContentLoaded', arguments.callee, false);
}

function Set(patterns) {
	this.patterns = patterns;
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
	
	_fromPatterns: function(str) {
		console.info(str);
		vars = str.match(/\$\(.+?\)/g);
		for (var i=0; i<vars.length; i++) {
			str = str.replace(vars[i], this.patterns[vars[i].replace('$(', '').replace(')', '')]);
		}
		console.info(str);
	},
	
	_getDateYear: function() {
		if (!this.date) return '';
		return this.date.getFullYear();
	},
	_getDateMonth: function() {
		if (!this.date) return '';
		var m = this.date.getMonth()+1;
		if (m < 10) return '0'+m;
		return m;
	},
	_getDateDay: function() {
		if (!this.date) return '';
		var d = this.date.getDate();
		if (d < 10) return '0'+d;
		return d;
	},
	_getDateFmt: function() {
		if (!this.date) return '';
		return this.dateYear + '-' + this.dateMonth + '-' + this.dateDay;
	},
	_getModelFmt: function() {
		if (!this.model) return '';
		return this.model.toLowerCase().replace(/ /g, '-');
	},
	_getTitleFmt: function() {
		if (!this.title) return '';
		return this.title.toLowerCase().replace(/ /g, '-');
	},
	_getArtistFmt: function() {
		if (!this.artist) return '';
		var a = this.artist.toLowerCase().split(' ');
		if (a.length < 2) return a;
		return a.shift()[0] + '-' + a.join('-');
	},
	_getCover: function() {
		if (this._cover) return this._cover;
		// patterns.tcover = '$(imgRoot)$(id)/t_cover_$(id).jpg'
		this._fromPatterns(this.patterns.tcover);
		return this._cover = 'http://static.met-art.com/media/' + this.id + '/cover_' + this.id + '.jpg';
	},
	_getTCover: function() {
		if (this._tcover) return this._tcover;
		if (!this.id) return '';
		return this._tcover = 'http://static.met-art.com/media/' + this.id + '/t_cover_' + this.id + '.jpg';
	},
	_getWCover: function() {
		if (this._wcover) return this._wcover;
		if (!this.id) return '';
		return this._wcover = 'http://static.met-art.com/media/' + this.id + '/wide_' + this.id + '.jpg';
	},
	_getTWCover: function() {
		if (this._twcover) return this._twcover;
		if (!this.id) return '';
		return this._twcover = 'http://static.met-art.com/media/' + this.id + '/t_wide_' + this.id + '.jpg';
	},
	_getSample: function() {
		if (this._sample) return this._sample;
		if (!this.id) return '';
		return this._sample = 'http://buceta.com/galleries/' + this.dateYear + '/' + this.dateMonth + '/metart-' + this.modelFmt + '-in-' + this.titleFmt + '-by-' + this.artistFmt + '/';
	},
	_getSearchPattern: function() {
		if (this._search) return this._search;
		if (!this.title) return '';
		return this._search = this.model.split(' ').concat(this.title.split(' ')).join('+');
	}
}

var sitedata = linkPatterns['ma'];

function onload() {
	removeAllButTheMost('div.gallery_display');
	removeMore();
	
	var urls = window.location.href.split('/');
	var dateurl = urls[urls.length-3] + '-' + urls[urls.length-2];
	$('head').empty().append(
		$('<title>').text(sitedata.id.toUpperCase() + ' ' + dateurl)
	);
	
	// $('body').prepend('<button id="_GO_"> transf </button>');
	// $('#_GO_').on('click', function() {
	
	var data = $('table.gallery_table tr td ul').map(function() {
		return doScrap($(this));
	});
	
	$('body').empty();
	$('body').append(
		data.map(function() {
			return newPres(this);
		}).get()
	);
	$('body').css( {'display': 'block'} );
}

function doScrap($set) {
	var s = new Set(sitedata);
	
	var d = $('li:nth-child(2)', $set).text();  // 27.01.2014
	var dmy = d.match(/(\d{2})\.(\d{2})\.(\d{4})/);
	s.date = new Date(dmy[3], dmy[2]-1, dmy[1]);
	
	s.id = $('li:nth-child(1) a img', $set).attr('src').match(/\/media\/(.+)\//)[1];
	s.model = $('li:nth-child(3)', $set).text();
	s.modelId = $('li:nth-child(7) a', $set).attr('href').match(/\?Model_UUID=(.+)/)[1];
	s.title = $('li:nth-child(4)', $set).text();
	s.artist = $('li:nth-child(5) a', $set).text();
	
	if ($('li:nth-child(6)', $set).text() == 'MOVIE') s.type = 'vid';
	
	return s;
}

function newPres(s) {
	return $('<ul>').append(
		$('<a>', {'href': s.cover, 'target': '_blank'}).append($('<img>', {'src': s.tcover, 'title': s.model + ' - ' + s.title}) ),
		s.type == 'img' ?
			'' : $('<a>', {'href': s.wcover, 'target': '_blank'}).append($('<img>', {'src': s.twcover, 'title': s.model + ' - ' + s.title}) ),
		$('<li>', {'class': 'set-date'}).text(s.dateFmt),
		$('<li>').text(s.model),
		$('<li>').text(s.title),
		$('<li>').append($('<a>', {'href': s.sample, 'target': '_blank'}).text('sample') ),
		$('<li>').append($('<a>', {'href': 'http://www.metxx.com/search?q=' + s.searchPattern, 'target': '_blank'}).text('metxx') )
		// $('<li>').append($('<a>', {'href': 'http://www.hornywhores.net/search/' + s.searchPattern, 'target': '_blank'}).text('hornywhores') )
	);
}

function removeAllButTheMost(theMost) {
	$('body').after($(theMost));
	$('body').empty();
	$('body').append($(theMost));
}

function removeMore() {
	$('li:contains("Rated:")').remove();
	$('li:contains(" photos")').remove();
	$('li:nth-child(8)').remove();
	$('li:nth-child(8)').remove();
	
	$('a.append_pa_long').remove();
}

/*
serie, gallery, set, update
date: 2014-01-27
model: Milena D
modelId: 22EA835B150BD8B234567D90E1290D81
set: Maituse
setId: C05817BD3798F7645158B1D7B1E49710
artist: Erik Latika
*/

/*
<div class="gallery_display" style="position:relative;left:-16px;">
	<table class="gallery_table">
	<tbody>
	<tr>
		<td>
		<ul class="table_list">
		1	<li style="position:relative;">
				<a href="http://guests.met-art.com/model/mia-sollis/gallery/20140126/ROSELLE/">
					<img src="http://static.met-art.com/media/9EB2C3EBF7488514C5126017531BDCF9/t_cover_9EB2C3EBF7488514C5126017531BDCF9.jpg" alt="">
				</a>
			</li>
		2	<li>26.01.2014</li>
			<!-- <li>Rated: 8.84</li> REMOVED -->
		3	<li class="highlight">
				<a style="text-decoration:none;" href="http://guests.met-art.com/model/mia-sollis/">Mia Sollis</a>
			</li>
		4	<li>Roselle</li>
		5	<li>By 
				<a style="text-decoration:none;" href="http://guests.met-art.com/photographer/dave-lee/">Dave Lee</a>
			</li>
			<!-- <li>135 photos</li> REMOVED -->
		6	<li class="resolution">
				<a href="javascript:popGuestCover('9EB2C3EBF7488514C5126017531BDCF9');">Full Cover</a>
			</li>
		7	<li class="resolution spaced">
				<a class="jTip" href="http://guests.met-art.com/view/ajax/modelInfoj.php?Model_UUID=5D822CAFA9556454D921A47B4ED5D16F" id="bbl_0_740_top_5D822CAFA9556454D921A47B4ED5D16F">Biography</a>
			</li>
		</ul>
		</td>
		
		<td>
		<ul class="table_list">
		1	<li style="position:relative;">
				<a href="javascript:popMovieCover('9DE0A6ADAB55ED3421863D0032A850C7');">
					<img src="http://static.met-art.com/media/9DE0A6ADAB55ED3421863D0032A850C7/t_cover_9DE0A6ADAB55ED3421863D0032A850C7.jpg" alt="">
				</a>
			</li>
		2	<li>22.01.2014</li>
		3	<li class="highlight">
				<a style="text-decoration:none;" href="http://guests.met-art.com/model/mira-d/">Mira D</a>
			</li>
		4	<li>Tiffisa</li>
		5	<li>By 
				<a style="text-decoration:none;" href="http://guests.met-art.com/photographer/balius/">Balius</a>
			</li>
		6	<li class="resolution">
				<a href="javascript:popMovieCover('9DE0A6ADAB55ED3421863D0032A850C7');">MOVIE</a>
			</li>
		7	<li class="resolution spaced">
				<a class="jTip" href="http://guests.met-art.com/view/ajax/modelInfoj.php?Model_UUID=6B641B781E9746C445B8DDD23C97510A" id="bbl_4_196_top_6B641B781E9746C445B8DDD23C97510A">Biography</a>
			</li>
			<!-- <li>&nbsp;</li> REMOVED -->
			<!-- <li>&nbsp;</li> REMOVED -->
		</ul>
		</td>
*/

// http://www.met-art.com/webmasters/rss/
/*
<item>
	<title>Maituse</title>
	<link>
		http://guests.met-art.com/model/milena-d/gallery/20140127/MAITUSE/
	</link>
	<guid>
		http://guests.met-art.com/media/C05817BD3798F7645158B1D7B1E49710/t_cover_C05817BD3798F7645158B1D7B1E49710.jpg
	</guid>
	<description>
		<![CDATA[
		<a href="http://guests.met-art.com/model/milena-d/gallery/20140127/MAITUSE/">
			<img src="http://guests.met-art.com/media/C05817BD3798F7645158B1D7B1E49710/t_cover_C05817BD3798F7645158B1D7B1E49710.jpg">
		</a>
		<br/>
		Milena D: "Maituse" by Erik Latika
		]]>
	</description>
	<pubDate>Mon, 27 Jan 2014 12:00:00 MST</pubDate>
	<enclosure url="http://guests.met-art.com/media/C05817BD3798F7645158B1D7B1E49710/t_cover_C05817BD3798F7645158B1D7B1E49710.jpg" length="7899" type="image/jpg"/>
</item>
*/
