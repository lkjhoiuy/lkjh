function LinkPattern() {
	this.id = '';
	this.home = '';
	this.set = '';
	this.cover = '';
	this.tcover = '';
	this.wcover = '';
	this.twcover = '';
	this.sample = '';
}

LinkPattern.prototype = {
}


// mélange dans le patterns site et set !!!!!!!!!!
var ma = new LinkPattern();
ma.id = 'ma';
ma.name = 'Met Art';
ma.website = 'http://guests.met-art.com/';
ma.logo = 'http://static.met-art.com/favicon.ico';
ma.bandeau = 'http://static.met-art.com/view/images/new-logo-top.png';
ma.siteRoot = 'http://guests.met-art.com/';
ma.imgRoot = 'http://static.met-art.com/media/'
ma.set = '$(imgRoot)model/$(modelFmt)/gallery/$(dateYear)$(dateMonth)$(dateDay)/$(TITLE)/';
ma.model = '';
ma.cover = '$(imgRoot)$(id)/cover_$(id).jpg';
ma.tcover = '$(imgRoot)$(id)/t_cover_$(id).jpg';
ma.wcover = '$(imgRoot)$(id)/wide_$(id).jpg';
ma.twcover = '$(imgRoot)$(id)/t_wide_$(id).jpg';
ma.sample = '$(imgRoot)$(id)/cover_$(id).jpg';
ma.rss = '';


// http://m1.femjoy.com/u/img/femjoy/logo_footer.png

var linkPatterns = {};
linkPatterns['ma'] = ma;

// http://guests.met-art.com/archive/2014/01/
// Text version:
// http://www.met-art.com/guests/
// http://www.met-arti.com/model/metart/?F=0&C=M&O=D&V=0&P=*&X=Go

/*
Cover:
http://www.metartnetwork.com/helper/thumb.php?width=229&thumb=http://static.met-art.com/media/C05817BD3798F7645158B1D7B1E49710/cover_C05817BD3798F7645158B1D7B1E49710.jpg

http://static.met-art.com/media/C05817BD3798F7645158B1D7B1E49710/t_cover_C05817BD3798F7645158B1D7B1E49710.jpg (113x170)
http://static.met-art.com/media/C05817BD3798F7645158B1D7B1E49710/cover_C05817BD3798F7645158B1D7B1E49710.jpg (525x790)
http://static.met-art.com/media/C05817BD3798F7645158B1D7B1E49710/t_clean_C05817BD3798F7645158B1D7B1E49710.jpg (113x170)
http://static.met-art.com/media/C05817BD3798F7645158B1D7B1E49710/clean_C05817BD3798F7645158B1D7B1E49710.jpg (525x790)
For vid only:
http://static.met-art.com/media/396E0CB856798534897E488A9777869A/t_wide_396E0CB856798534897E488A9777869A.jpg (194x140)
http://static.met-art.com/media/396E0CB856798534897E488A9777869A/wide_396E0CB856798534897E488A9777869A.jpg (1097x790)

Set / img:
http://guests.met-art.com/model/milena-d/gallery/20140127/MAITUSE/
http://www.met-art.com/guests/model/milena-a/gallery/20140127/METUSE/ (text version)
14 images
http://www.metartnetwork.com/model/milena-d/gallery/20140127/MAITUSE/
15 images
http://static.met-art.com/media/C05817BD3798F7645158B1D7B1E49710/t_0D907ADC369DA9A46989145FACD055F5.jpg (86x..)

http://buceta.com/galleries/2014/01/metart-milena-d-in-maituse-by-e-latika/
16 images, index selon
http://buceta.com/galleries/2014/01/metart-milena-d-in-maituse-by-e-latika/thumbs/metart-milena-d-in-maituse-by-e-latika-1.jpg (245x365)
http://buceta.com/galleries/2014/01/metart-milena-d-in-maituse-by-e-latika/metart-milena-d-in-maituse-by-e-latika-1.jpg (1000x1500)

http://buceta.com/wordpress/wp-content/uploads/2014/01/metart-milena-d-in-maituse-by-e-latika-16.jpg

Available 11 days later:
http://www.met-arti.com/model/metart/milena_d/metuse.html
http://fhg.met-art.com/2014-01-27/METUSE/ 
http://static-fhg.met-art.com/media/C05817BD3798F7645158B1D7B1E49710/cover.jpg (250x376)
18 images:

Example:
DEB752CB3F5BC4B481131FEFBB1FCA5C
http://guests.met-art.com/model/katherine-a/gallery/20140116/PANEMO/
http://fhg.met-art.com/2014-01-16/PANEMO/
http://static-fhg.met-art.com/media/DEB752CB3F5BC4B481131FEFBB1FCA5C/cover.jpg (250x376)
18 images:
http://static-fhg.met-art.com/media/DEB752CB3F5BC4B481131FEFBB1FCA5C/wt_76372B18A7896754C12A1B40BEBC68BC.jpg (111x167)
http://static-fhg.met-art.com/media/DEB752CB3F5BC4B481131FEFBB1FCA5C/w_76372B18A7896754C12A1B40BEBC68BC.jpg (682x1024)

Model:
http://guests.met-art.com/view/ajax/modelInfoj.php?Model_UUID=22EA835B150BD8B234567D90E1290D81
http://static.met-art.com/media/headshots/milena-d.jpg (113x170)

All sets:
http://guests.met-art.com/model/milena-d/
http://www.met-art.com/guests/model/milena-d/ (text version)
http://www.met-arti.com/model/metart/milena_d/

http://buceta.com/tag/milena-d/
3 images, index selon
http://buceta.com/wordpress/wp-content/uploads/2014/01/metart-milena-d-in-maituse-by-e-latika-16.jpg (210x314)

http://blog.met-art.com/nude-erotic-art/presenting-hannah-tilt-tempting
*/
