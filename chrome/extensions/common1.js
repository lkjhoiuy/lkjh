//  Extends String

String.prototype.startsWith = function(pattern) {
	return this.indexOf(pattern) == 0;
};

String.prototype.endsWith = function(pattern) {
	var d = this.length - pattern.length;
	return d >= 0 && this.lastIndexOf(pattern) === d;
};

