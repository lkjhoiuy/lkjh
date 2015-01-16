# -*- coding: utf-8 -*-
"""
"""

if __name__ == "__main__":
	s = b'\x96'
	# KO d = s.decode('utf-8')
	#~ d = s.decode('iso-8859-1')
	d = s.decode('cp1252')
	#~ print(s)
	#~ print(d)
	print(b'\x96'.decode('cp1252'))
	
	with open('toto.txt', 'wb') as fp:
		# fp.write(b"toto " + b'\x96' + b" toto")
		fp.write(b"toto \x96 toto")
		fp.write("éè".encode('utf-8'))

	with open('toto.txt', 'r') as fp:
		r = fp.read()
	
	print(r)
	r = r.encode('cp1252')
	print(r)
	
	#~ r = b"toto \x96 toto"
	#~ print(r)
	
	#~ r = r.decode('cp1252')
	
	#~ r = str(r)
	#~ print(r)
	# KO r.encode('iso-8859-1')
	# r = r.encode('utf-8')  # b'toto \xe2\x80\x93 toto'
	
	#~ r = r.encode('cp1252')  # b'toto \x96 toto'
	#~ print(r)
	
	print(r.find(b'\x96'))  # 5
	r = r.replace(b'\x96', b'-')
	
	#~ r = r.decode('cp1252')
	r = r.decode('utf-8')
	print(r)  # b'toto - toto'
