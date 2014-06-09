
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

from pymonad import Maybe, Just, Nothing

class MagmaMeta(type):
    """ A metaclass used to control how the instantiation of Magma subclasses behaves. This essentially
		makes the Magma class an abstract base class, but I need more control than the abc library provides,
		so I created this custom metaclass. """
    def __new__(cls, name, parents, dct):
        # Check that Magma instances are valid.
        if name is not 'Magma':
            if 'CAYLEY_TABLE' not in dct:
                raise Exception("Cannot create Magma instance without CAYLEY_TABLE")
            else:
                # Check for square CAYLEY_TABLE
                for row in dct['CAYLEY_TABLE']:
                    if not len(row) == len(dct['CAYLEY_TABLE']):
                        raise Exception("CAYLEY_TABLE must be a square array")
                # Create SET and ORDER from CAYLEY_TABLE
                dct['SET'] = set([])
                for rows in dct['CAYLEY_TABLE']:
                    for x in rows:
                        dct['SET'].add(x)
                dct['ORDER'] = len(dct['SET'])
        return super(MagmaMeta, cls).__new__(cls, name, parents, dct)

class Magma(metaclass=MagmaMeta):
	"""
Magma is an abstract base class used to represent the algebraic structure known as a magma,
which is simply a set, and a binary operator (+) that maps two values in the set to another
value in the set. 

The Magma class used the static constant CAYLEY_TABLE to define how the binary operator works,
CAYLEY_TABLE is a two dimensional array that represents the result of the binary operator.

By convention, the row number corresponds to the value on the left side of the binary operator,
and the column number corresponds to the value on the right. e.a. for a+b=c, a is the row number,
c is the column number, and c is the result of the operation.

The row and column numbers are also 0-indexed, e.a. the 1st column is actually, the 0th column,
the 2nd column is actually the 1st column... 
		
*****BASIC USAGE*****:

To create a new magma class with a Cayley table, use the following syntax:
 
class DihedralD3(magpy.Magma):
	CAYLEY_TABLE == [[0,1,2,3,4,5],
			[1,0,4,5,2,3],
			[2,5,0,4,3,1],
			[3,4,5,0,1,2],
			[4,3,1,2,5,0],
			[5,2,3,1,0,4]]

To instantiate a magma class, use this syntax:

d = DihedralD3(2) 

Finally, to use the binary operator of the magma, simply use "+"

d + d
	"""

	## options ##
	usegreek = False
	use_eabc = False
	usecustomcharset = False

	## Charsets ##
    #
	# Used in the display of individual values of magmas, and the display of a
	# magma's CAYLEY_TABLE. Customizable with the charset options.
    #

	customcharset = []
	greek = ['α','β','γ','δ','ε','ζ','η','θ','ι','κ','λ','μ','ν','ξ','ο','π','ρ','σ','τ','υ','φ','χ','ψ','ω']
	eabc = ['e','a','b','c','d','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

	### Constant Static Variables ###
    #
    # These must be given values (other than the default) in subclasses of Magma in order
    # for those subclasses to be valid. These values are CONSTANTS for subclasses of Magma,
    # and should not be modified after the class has been instantiated.
    #

	CAYLEY_TABLE = []
	SET = set([])
	ORDER = 0 

	# 
	__identity = Nothing

	def __init__(self,n):
		if self.__class__.__name__ == 'Magma':
			raise NotImplementedError("Magma is an abstract base class, it must be instantiated before use. See help(Magma) for more information.")
		if(n in self.SET):
			self.n = n
		else:
			raise Exception("Invalid argument.")

	def __add__(x,y):
		new = x.__class__(x.CAYLEY_TABLE[x.n][y.n])
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
		for x in range(self.ORDER):
			for y in range(self.ORDER):
				if(self.__class__(x) + self.__class__(y) == self.__class__(y) + self.__class__(x)):
					pass
				else:
					return False
		return True

	def is_assoc(self):
		""" """
		for x in range(self.ORDER):
			for y in range(self.ORDER):
				for z in range(self.ORDER):
					if( (self.__class__(x) + self.__class__(y)) + self.__class__(z) == self.__class__(x) + (self.__class__(y) + self.__class__(z)) ):
						pass
					else:
						return False
		return True

	def hasIdentity(self):
		""" """
		for x in range(self.ORDER):
			if(self.isIdentity(self.__class__(x))):
				if(self.identity == Nothing):
					self.identity = Just(x)
				return True
		return False

	def isIdentity(self,e):
		""" """
		for x in range(self.ORDER):
			if(not self.__class__(x) + e == self.__class__(x)):
				return False
		return True

	def hasInverse(self,x):
		""" """
		if(self.identity == Nothing):
			return False
		else:
			for y in range(self.ORDER):
				if(x + self.__class__(y) == self.__class__(self.identity.getValue())):
					return True
			return False

	def isInvertable(self):
		""" """
		for x in range(self.ORDER):
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
		for x in range(self.ORDER):
			for y in range(self.ORDER):
				for z in range(self.ORDER):
					if(not self.__class__(x) + (self.__class__(y) + self.__class__(z)) == (self.__class__(x) + self.__class__(y)) + (self.__class__(x) + self.__class__(z)) ):
						return False
		return True

	def __rackProperty__(self):
		""" for all a, b, there exists exactly one c such that a * c = b """		
		count = 0 # number of c
		for a in range(self.ORDER):
			for b in range(self.ORDER):
				for c in range(self.ORDER):
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
		for row in self.CAYLEY_TABLE:
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
		for _x in range(self.ORDER):
			for _y in range(self.ORDER):
				for _a in range(self.ORDER):
					for _b in range(self.ORDER):
						x = self.__class_(_x)
						y =	self.__class_(_y)
						a = self.__class_(_a)
						b = self.__class_(_b)
						if(not (a+x)+(y+b) == (b+x)+(y+a)):
							return False
		return True

	def isFlexible(self):
		""" X*(Y*X) = (X*Y)*X """
		for _x in range(self.ORDER):
			for _y in range(self.ORDER):
				x = self.__class__(_x)
				y = self.__class__(_y)
				if(not x+(y+x) == (x+y)+x):
					return False
		return True

	def isJordan(self):
		""" ((XX)Y)X = (XX)(YX) """
		for _x in range(self.ORDER):
			for _y in range(self.ORDER):
				x = self.__class__(_x)
				y = self.__class__(_y)
				if(not ((x+x)+y)+x == (x+x)+(y+x) ):
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
		for _x in range(self.ORDER):
			for _y in range(self.ORDER):
				for _z in range(self.ORDER):
					x = self.__class__(_x)
					y = self.__class__(_y)
					z = self.__class__(_z)
					if(not y+(z+(y+x)) == (y+(z+y))+x):
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
		for _x in range(self.ORDER):
			for _y in range(self.ORDER):
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
		for _x in range(self.ORDER):
			for _y in range(self.ORDER):
				x = self.__class__(_x)
				y = self.__class__(_x)
				if(not (x+(x+y) == y and self.is_commut())):
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
		for _x in range(self.ORDER):
			for _y in range(self.ORDER):
				for _u in range(self.ORDER):
					for _v in range(self.ORDER):
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
