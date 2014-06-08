#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Magma.py
#
# Nathan BeDell
# 6/8/2014
#
# This file contains the Magma abstract base class, which allows the user to instantiate a
# derived class representing a magma with a cayley table, order, and set of elements in the
# magma. The + operator is used for the binary magma operation. See readme.md for more 
# usage information.
#

from abc import ABCMeta, abstractproperty, abstractmethod

class abstractstatic(staticmethod):
    __slots__ = ()
    def __init__(self, function):
        super(abstractstatic, self).__init__(function)
        function.__isabstractmethod__ = True
    __isabstractmethod__ = True

class Magma(metaclass=ABCMeta):

	## options ##
	usegreek = False
	greek = ['α','β','γ','δ','ε','ζ','η','θ','ι','κ','λ','μ','ν','ξ','ο','π','ρ','σ','τ','υ','φ','χ','ψ','ω']
	usecustomcharset = False
	customcharset = []
	identity = [] # [] if none, populated by one number if has inverse. Maybe monad?


	@abstractstatic
	def cayley_table(self):
		""" """
		return []

	@abstractstatic
	def order(self):
		""" """
		return 0

	@abstractstatic
	def magma_set(self):
		""" """
		return set([])

	def __init__(self,n):
		if(n in self.magma_set()):
			self.n = n
		else:
			raise Exception("Invalid argument.")

	def __add__(x,y):
		new = x.__class__(x.cayley_table()[x.n][y.n])
		if(x.usegreek == True or y.usegreek == True):
			new.usegreek = True
		return new

	def __eq__(x,y): # ==
		if x.n == y.n:
			return True
		else:
			return False

	def __repr__(self):
		if not self.usegreek:
			return str(self.n)
		elif self.usegreek:
			return self.greek[self.n]
			if self.n == 0:
				return "α"
			if self.n == 1:
				return "β"
			if self.n == 2:
				return "γ"
		else:
			return "error"
	def is_commut(self):
		""" Checks to see if x + y = y + x for all x and y in the magma. """
		for x in range(self.order()):
			for y in range(self.order()):
				if(self.__class__(x) + self.__class__(y) == self.__class__(y) + self.__class__(x)):
					pass
				else:
					return False
		return True

	def is_assoc(self):
		""" """
		for x in range(self.order()):
			for y in range(self.order()):
				for z in range(self.order()):
					if( (self.__class__(x) + self.__class__(y)) + self.__class__(z) == self.__class__(x) + (self.__class__(y) + self.__class__(z)) ):
						pass
					else:
						return False
		return True

	def hasIdentity(self):
		""" """
		for x in range(self.order()):
			if(self.isIdentity(self.__class__(x))):
				if(len(self.identity) == 0):
					self.identity.append(x)
				return True
		return False

	def isIdentity(self,e):
		""" """
		for x in range(self.order()):
			if(not self.__class__(x) + e == self.__class__(x)):
				return False
		return True

	def hasInverse(self,x):
		""" """
		if(not len(self.identity) == 1):
			return False
		else:
			for y in range(self.order()):
				if(x + self.__class__(y) == self.__class__(self.identity[0])):
					return True
			return False

	def isInvertable(self):
		""" """
		for x in range(self.order()):
			if(not self.hasInverse(self.__class__(x))):
				return False
		return True

	def isMonoid(self):
		""" """
		if(self.hasIdentity() and self.is_assoc()):
			return True
		else:
			return False

	def isGroup(self):
		""" """
		if(self.isMonoid() and self.isInvertable()):
			return True
		else:
			return False

	def isAbeleanGroup(self):
		""" """
		if(self.isGroup() and self.is_commut()):
			return True
		else:
			return False

	def isLoop(self):
		""" """
		if(self.hasIdentity() and self.isInvertable()):
			return True
		else:
			return False

	def isMoufangLoop():
		""" """
		pass

	def isSelfDistributive(self):
		""" Returns true if all of the elements of the magma satisfy the self distributive property. """
		for x in range(self.order()):
			for y in range(self.order()):
				for z in range(self.order()):
					if(not self.__class__(x) + (self.__class__(y) + self.__class__(z)) == (self.__class__(x) + self.__class__(y)) + (self.__class__(x) + self.__class__(z)) ):
						return False
		return True

	def __rackProperty__(self):
		""" for all a, b, there exists exactly one c such that a * c = b """		
		count = 0 # number of c
		for a in range(self.order()):
			for b in range(self.order()):
				for c in range(self.order()):
					if (self.__class__(a) + self.__class__(c) == self.__class__(b)):
						count = count + 1
					if (count > 1):
						return False
		if(count == 1):
			return True
		else:
			return False

	def isRack(self):
		""" """
		if(self.isSelfDistributive() and self.__rackProperty__()):
			return True
		else:
			return False

	def isQuandle(self):
		""" """
		if(self.isRack() and self.isIdempotent()):
			return True
		else:
			return False

	def isBiRack(self):
		""" """
		pass

	def isBiQuandle(self):
		""" """
		print("test")

	def isIdempotent(self): # Could I use functional programming to make this simpler?
		""" Tests to see if mag obeys the indepotent property for all x.
		∀xϵmag(x * x = x) """
		for row in self.cayley_table():
			for x in row:
				if((self.__class__(x) + self.__class__(x)) == self.__class__(x)):
					pass
				else:
					return False
		return True 
	
	def isSzasz(self):
		""" """
		pass

	def isParamedial(self):
		""" """
		for _x in range(self.order()):
			for _y in range(self.order()):
				for _a in range(self.order()):
					for _b in range(self.order()):
						x = self.__class_(_x)
						y =	self.__class_(_y)
						a = self.__class_(_a)
						b = self.__class_(_b)
						if(not (a+x)+(y+b) == (b+x)+(y+a)):
							return False
		return True

	def isFlexible(self):
		""" X*(Y*X) = (X*Y)*X """
		for _x in range(self.order()):
			for _y in range(self.order()):
				x = self.__class__(_x)
				y = self.__class__(_y)
				if(not x+(y+x) == (x+y)+x):
					return False
		return True

	def isJordan(self):
		""" ((XX)Y)X = (XX)(YX) """
		for _x in range(self.order()):
			for _y in range(self.order()):
				x = self.class(_x)
				y = self.class(_y)
				if(not ((x+x)+y)+x == (x+x)+(y+x))):
					return False
		return True

	def isAntiCommutative(self):
		""" """
		pass

	def isAlternative(self):
		""" (X*X)*Y = X*(X*Y) and X*(Y*Y) = (X*Y)*Y """
		pass

	def isExtra(self):
		""" ((XY)Z)X = X(Y(ZX)) """
		pass

	def isLeftBol(self):
		""" Y(Z(YX)) = (Y(ZY))X """
		for _x in range(self.order()):
			for _y in range(self.order()):
				for _z in range(self.order()):
					x = self.__class__(_x)
					y = self.__class__(_y)
					z = self.__class__(_z)
					if(not y+(z+(y+x) == (y+(z+y))+x):
						return False
		return True

	def isBand(self):
		""" """
		if(self.is_assoc() and self.isIdempotent()):
			return True
		else:
			return False

	def isRightInvoulntary():
		""" (XY)Y = X """
		for _x in range(self.order()):
			for _y in range(self.order()):
				x = self.__class__(_x)
				y = self.__class__(_y)
				if(not (x+y)+y == x):
					return False

	def isKei(self):
		""" """
		if(self.isQuandle() and self.isRightInvoulntary()):
			return True
		else:
			return False

	def isSteiner(self):
		""" """
		for _x in range(self.order()):
			for _y in range(self.order()):
				x = self.__class__(_x)
				y = self.__class__(_x)
				if(not (x+(x+y) == y && self.is_commut())):
					return False
		return True

	def isSquag(self):
		""" A squag is an idempotent Steiner magma. """
		if(self.isSteiner() and self.isIdempotent()):
			return True
		else:
			return False

	def isDiassociative(self):
		""" Returns true if each submagma of the magma m generated by two elements is associative. """
		pass

	def isMedial(self):
		""" Returns true if the agma satisfies the medial law (x*y)*(u*v) = (x*u)*(y*v). """
		for _x in range(self.order()):
			for _y in range(self.order()):
				for _u in range(self.order()):
					for _v in range(self.order()):
						x = self.__class__(_x)
						y = self.__class__(_y)
						u = self.__class__(_u)
						v = self.__class__(_v)
						if(not (x+y)+(u+v) == (x+u)+(y+v)):
							return False
		return True
		
	def IsSubMagma(self,magma):
		""" Determines if magma is a submagma of the magma object """
		pass

	def isZeropotent(self):
		""" (X*X)*Y = (Y*Y)*X = X*X """
		pass

	def evaluate(self,expr):
		""" Evaluates a string of symbols and letters or numbers representing the operator and symbols of the magma. """
		if(self.usegreek):
			# Tokenize with () first?
			pass # Tokenize with ' ' and '*' or '+'.
			# make into list
		elif(self.usecustomcharset):
			pass #tokenize
		else:
			pass

def applyToAllOfOrder(f,n):
	""" Applies f to all magmas of order n and returns a list of the results. """
	array = []
	results = []

	# O(n^n) complexity?

	# Possiblity -- Make permutations of an array and rearrange into matrices for function application
	# logic?

	# Populate array with first permutation
	for i in range(n):
		array.append([])
	for i in range(n):
		for j in range(n):
			array[i].append(0)

	
	
# Idea: create a text interface for using this, so that things like alternate binary operators can be defined e.a. ▷ and ◁ ...
# α, β, γ, δ, ζ, η, θ, etc...
# ◇, ◆, ◊, ○, ◾, ◽ ...
