document.addEventListener('DOMContentLoaded', onDOMloaded, false);

// TODO par jour
// http://www.metxx.com/2014_05_08_archive.html

var db = {};
var entry = {};

var regsites = [
	"1000giri",
	"10musume",
	"1pondo",
	"4K-STAR",
	"BeautyLeg",
	"Bomb.tv",
	"C0930",
	"Caribbeancom",
	"Climax Shodo",
	"DGC",
	"DISI",
	"Fetibox",
	"Fetishkorea",
	"G-area",
	"Gachinco",
	"Graphis",
	"H-Paradise",
	"H0930",
	"H4610",
	"HEYZO",
	"Himemix",
	"image.tv",
	"kinpatu86",
	"kin8tengoku",
	"Legs Japan",
	"Ligui",
	"Maxi-247",
	"misty Idol Gravure",
	"Mywife.cc",
	"NAKED-ART",
	"Pacific Girls",
	"pacopacomama",
	"PANS",
	"Pantyhose Life",
	"Pornograph",
	"QWQSHOW",
	"Real Street Angels",
	"ROSI",
	"RQ-STAR",
	"RU1MM",
	"S-Cute",
	"Syukou-Club",
	"The Black Alley",
	"Tokyo Face Fuck",
	"TOKYO-HOT",
	"TopQueen",
	"TPimage",
	"TuiGirl",
	"Ugirls",
	"VgirlMM",
	"Wanibooks",
	"WPB-net",
	"X-City",
	"XiuRen",
	"YS-Web"
];

function onDOMloaded() {
	/* search
	if ($('div.jump-link a').length > 0) {
		window.location.href = $('div.jump-link a').attr('href');
		return;
	}
	*/
	
	scrap1();
	scrap2();
	//~ console.log("%o", db);
	
	$('body').append(
		$('<textarea>', { 'id': 'tocopy' })
	)
}

function scrap1() {
	$('div.hentry').each(function() {
		entry = {};
		entry.$ui = $(this);
		entry.id = $('a', $(this)).attr('name');
		entry.url = $('h3.post-title a', $(this)).attr('href');
		entry.title = $(this).find('h3.post-title a').text().trim().replace(/(\r\n|\r|\n)/gm, '');
			
		db[entry.id] = entry;
	});
}

function scrap2() {
	$.each(db, function(id, entry) {
		var nothanks = false;
		var r = $.each(regsites, function(idx, val) {
			var pat = new RegExp('^' + val.replace('.', '\.') + ' ', 'i')
			if (pat.test(entry.title)) {
				nothanks = true;
				return false;  // break each()
			}
		});
		if (nothanks) {
			entry.$ui.remove();
			return;  // continue each()
		}
		
		scrapTitle(entry.id);
		
		$.get(entry.url)
		.done(function(data) {
			// extract post content
			var $e = $('div.blog-posts', $(data));
			scrap3(entry, $e);
		})
		.fail(function(jqxhr, textStatus, error) {
			console.log("Failed: " + error);
		});
	});
}

function scrap3(entry, $e) {
	console.log("%o", $e);
	entry.$links = $e.find('a[href^="http://uploaded.net/"]');
	
	// no link uploaded / cosyupload: no display
	if (entry.$links.length == 0) {
		// console.log("Remove %s - %s", entry.id, entry.url);
		entry.$ui.remove();
		return;
	}

	scrap4(entry.$ui, entry);
}

function scrap4($ui, entry) {
	// Main image
	var $main = $('a:has(img)', $ui);
	var href = $main.attr('href');
	
	// Add new tab
	$('a:has(img)', $ui).each(function() {
		$(this).attr('target', '_blank');
	});
	
	$anchor = $('<div>', { 'class': 'links-ul' });
	$ui.prepend(
		'\n',
		$('<p>').text(entry.id),
		$anchor
	);
	
	entry.$links.each(function() {
		var link = $(this).attr('href');
		$anchor.append(
			'\n',
			$('<p>').append(
				$('<a>', { 'href': link }).text(link),
				$('<span>').text('ok').on('click', function(e) {
					e.stopPropagation();
					$(this).toggleClass('selected');
					if ($(this).hasClass('selected')) {
						//~ $('#tocopy').append( $('<li>').text(link) );
						$('#tocopy').append(link, '\n');
					}
					else {
						//~ $('#tocopy').find($('li:contains('+link+')')).remove();
						//~ var i = 
						$('#tocopy').text($('#tocopy').text().replace(link+'\n', ''));
					}
				}).trigger('click')
			).on('click', function() {
				$(this).parent().find($('span')).trigger('click');
			})
		)
	});
}

function scrapTitle(id) {
	var entry = db[id];
	
	var pat = /^(.+?) (20\d\d-\d\d-\d\d) (.+?) - (.+?)( \(HD Video\))?$/;
	var re = new RegExp(pat);
	//~ matchs = re.exec(entry.title);
	matchs = entry.title.match(re);
	if (matchs) {
		entry.setStudio = matchs[1].trim();
		entry.setDate = matchs[2].trim();
		entry.setModel = matchs[3].trim();
		entry.setTitle = matchs[4].trim();
		if (matchs[5])
			entry.setType = 'vid';
	}
	console.log("%o", entry);

}