# -*- coding: utf-8 -*-
"""
"""
from pprint import pprint

class A:
	a = "class A - a"
	
	def __init__(self):
		self._b = "class A - b"
	
	@property
	def b(self):
		return self._b
		
	@property
	def c(self):
		return "class A - c"
		
	def d(self):
		return "class A - d"
		
	def test(self):
		print("A.a =", A.a)
		print("self.a =", self.a)
		print("self.b =", self.b)
		print("self.c =", self.c)
		print("self.d() =", self.d())

class B(A):
	a = "class B - a"
	
	def __init__(self):
		super().__init__()
		self._b = "class B - b"
	
	@property
	def c(self):
		return "class B - c"
		
	def d(self):
		return "class B - d"
		
	def test(self):
		print("B.a =", B.a)
		super().test()

class C(A):
	a = "class C - a"
	
	def __init__(self):
		super().__init__()
		self._b = "class C - b"
	
	@property
	def c(self):
		return "class C - c"
		
	def d(self):
		return "class C - d"
		
	def test(self):
		print("C.a =", C.a)
		super().test()

#~ print()
#~ print("-- A")
#~ insta = A()
#~ insta.test()
#~ pprint(insta.__dict__)

print()
print("-- B")
instb = B()
instb.test()
pprint(instb.__dict__)

print()
print("-- C")
instc = C()
instc.test()
pprint(instc.__dict__)

A.a = "class AA - a"
B.a = "class BB - a"
C.a = "class CC - a"
print()
print("-- B")
instb.test()
print()
print("-- C")
instc.test()

#~ print()
#~ print("-- A")
#~ insta.test()

instb.a = "coucou"
print()
print("-- B")
instb.test()
print()
print("-- C")
instc.test()

