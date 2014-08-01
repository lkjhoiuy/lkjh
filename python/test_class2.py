# -*- coding: utf-8 -*-
"""
"""
from pprint import pprint

class A:
	a = "class A - a"
	def __init__(self):
		pass
	@property
	def b(self):
		return "class A - b"
	def test(self):
		print("  A.a =", A.a)
		print("  B.a =", B.a)
		print("  self.a =", self.a)
		print("  self.b =", self.b)

class B:
	a = "class B - a"
	def __init__(self):
		pass
	@property
	def b(self):
		return "class B - b"
	def test(self):
		print("  A.a =", A.a)
		print("  B.a =", B.a)
		print("  self.a =", self.a)
		print("  self.b =", self.b)

class AA(A):
	a = "class AA - a"
	def __init__(self):
		super().__init__()
	@property
	def b(self):
		return "class AA - b"
	def test(self):
		print("AA.a =", AA.a)
		super().test()

class BB(B):
	a = "class BB - a"
	def __init__(self):
		super().__init__()
	@property
	def b(self):
		return "class BB - b"
	def test(self):
		print("BB.a =", BB.a)
		super().test()

print("-- AA")
aa = AA()
aa.test()
pprint(aa.__dict__)

print()
print("-- BB")
bb = BB()
bb.test()
pprint(bb.__dict__)

A.a = "class A - NEW a"
B.a = "class B - NEW a"
AA.a = "class AA - NEW a"
BB.a = "class BB - NEW a"

print()
print("-- AA")
aa.test()

print()
print("-- BB")
bb.test()
