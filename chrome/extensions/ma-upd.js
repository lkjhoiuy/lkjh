// http://met-art.com/updates?date=2014-02

function getUrlParams() {
	var match,
		pl = /\+/g,  // Regex for replacing addition symbol with a space
		search = /([^&=]+)=?([^&]*)/g,
		decode = function(s) { return decodeURIComponent(s.replace(pl, ' ')); },
		query  = window.location.search.substring(1),
		ret = {};

    while (match = search.exec(query)) {
       ret[decode(match[1])] = decode(match[2]);
	}
	return ret;
}

function Doc() {
	this.link = '';
	this.month = '';
}

Doc.prototype = {
	
	clean: function() {
		$('html').empty();
		$('html').append( $('<head>'), '\n', $('<body>'), '\n' );
	},
	
	addLink: function(month) {
		this.month = month;
		this.link = 'http://guests.met-art.com/archive/' + this.month.split('-').join('/') + '/';
		var _this = this;
		
		$('body').append(
			'\n',
			$('<p>').append(
				$('<a>', { 'href': this.link }).text('ma ' + this.month)
			),
			'\n',
			$('<button>', { 'id': 'btn-' + this.month }).prop('disabled', true).text("click").click( function(evt) {
				$('div#data-' + _this.month).toggle();
			}),
			'\n',
			$('<div>', { 'id': 'data-' + this.month })
		);
	},
	
	getLink: function() {
		var _this = this;
		
		// $.get(this.link, function(data, textStatus, jqXHR) {
		//    if (jqXHR.status == 200)
		
		$.get(this.link)
		.done(function(data) {
			var $result = $('table.gallery_table', $(data));
			_this.addTable($result);
			
			var data = $('table.gallery_table tr td ul').map(function() {
				return doScrap($(this));
			});
		})
		.fail(function(jqxhr, textStatus, error) {
			var $result = $('<span>').text(textStatus);
			_this.addTable($result);
		});
	},
	
	addTable: function($e) {
		// Remove some <li>
		$e.find('li:contains("Rated:")').remove();
		$e.find('li:contains(" photos")').remove();
		$e.find('li:nth-child(8)').remove();
		$e.find('li:nth-child(8)').remove();
		// Remove last <td>
		$e.find('td a.append_pa_long').parent().remove();
		
		$('div#data-' + this.month).toggle().append('\n', $e);
		$('button#btn-' + this.month).prop('disabled', false);
	}
}

function doScrap($upd) {
	console.log("doScrap");
	console.log("%o", $upd[0]);
	
	var s = new Update(ma);
	
	var d = $('li:nth-child(2)', $upd).text();  // 27.01.2014
	var dmy = d.match(/(\d{2})\.(\d{2})\.(\d{4})/);
	s.date = new Date(dmy[3], dmy[2]-1, dmy[1]);
	
	s.id = $('li:nth-child(1) a img', $upd).attr('src').match(/\/media\/(.+)\//)[1];
	s.model = $('li:nth-child(3)', $upd).text();
	s.modelId = $('li:nth-child(7) a', $upd).attr('href').match(/\?Model_UUID=(.+)/)[1];
	s.title = $('li:nth-child(4)', $upd).text();
	s.artist = $('li:nth-child(5) a', $upd).text();
	
	if ($('li:nth-child(6)', $upd).text() == 'MOVIE') s.type = 'vid';
	
	console.log("%O", s);
	return s;
}

window.stop();

var urlParams = getUrlParams();
var doc = new Doc();

doc.clean();
doc.addLink(urlParams['date']);
doc.getLink();

function BdSitePattern() {
	this.id = '';
	this.home = '';
	this.upd = '';
	this.cover = '';
	this.tcover = '';
	this.wcover = '';
	this.twcover = '';
}

BdSitePattern.prototype = {
}

// mélange dans le patterns site et set !!!!!!!!!!
var ma = new BdSitePattern();

ma.id = 'ma';
ma.name = 'Met Art';
ma.website = 'http://guests.met-art.com/';
ma.logo = 'http://static.met-art.com/favicon.ico';
ma.bandeau = 'http://static.met-art.com/view/images/new-logo-top.png';
ma.siteRoot = 'http://guests.met-art.com/';
ma.imgRoot = 'http://static.met-art.com/media/'
ma.upd = '$(imgRoot)model/$(modelFmt)/gallery/$(dateYear)$(dateMonth)$(dateDay)/$(TITLE)/';
ma.model = '';
ma.cover = '$(imgRoot)$(id)/cover_$(id).jpg';
ma.tcover = '$(imgRoot)$(id)/t_cover_$(id).jpg';
ma.wcover = '$(imgRoot)$(id)/wide_$(id).jpg';
ma.twcover = '$(imgRoot)$(id)/t_wide_$(id).jpg';

function Update(patterns) {
	this.patterns = patterns;
	this.date = '';  // upd-date "2014-01-27"
	this.id = '';  // upd-id
	this.model = '';  // upd-model-name "Milena D"
	this.modelId = '';  // upd-model-id
	this.title = '';  // upd-title
	this.artist = '';  // upd-artist
	this.type = 'img';  // 
	
	this.__defineGetter__('cover', function() { return this._getCover(); });
	this.__defineGetter__('tcover', function() { return this._getTCover(); });
	this.__defineGetter__('wcover', function() { return this._getWCover(); });
	this.__defineGetter__('twcover', function() { return this._getTWCover(); });
	
	this.__defineGetter__('dateYear', function() { return this._getDateYear(); });
	this.__defineGetter__('dateMonth', function() { return this._getDateMonth(); });
	this.__defineGetter__('dateDay', function() { return this._getDateDay(); });
	this.__defineGetter__('dateFmt', function() { return this._getDateFmt(); });
	
	this.__defineGetter__('modelFmt', function() { return this._getModelFmt(); });
	this.__defineGetter__('titleFmt', function() { return this._getTitleFmt(); });
	this.__defineGetter__('artistFmt', function() { return this._getArtistFmt(); });
	
	this.__defineGetter__('searchPattern', function() { return this._getSearchPattern(); });
}
Update.prototype = {
	
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
	_getSearchPattern: function() {
		if (this._search) return this._search;
		if (!this.title) return '';
		return this._search = this.model.split(' ').concat(this.title.split(' ')).join('+');
	}
}
