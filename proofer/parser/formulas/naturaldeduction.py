import sys
from itertools import combinations, groupby
sys.path.insert(0, "../..")

if sys.version_info[0] >= 3:
    raw_input = input


def listOfAtoms(formulaObj):
	result = []
	if not type(formulaObj) is AndFormula:
		result.append(formulaObj)
		return result
	for f in formulaObj.formulas:
		result.extend(listOfAtoms(f))
	return result

class Proof:
	'''
	Constructed with assumptions as a conjunction. Then for each formula line,
	the Proof object will check if it infers the formula from assumption and if
	true, joins it with the previous conjuction to make another conjuction and
	so on
	'''

	def __init__(self, *assumptions, conjunction = [], lineNumber=1):
		self.ass = list(assumptions)
		self.numToForm = {n:f for (n,f) in \
		zip(range(lineNumber, len(self.ass)+1), self.ass)}
		vals = list(self.numToForm.values())
		vals.extend(conjunction)
		self.conjunction = AndFormula(*(vals))
		# print("created proof conjunction")
		# print(self.conjunction.__str__())

	def infers(self, formula):
		# print('infering')
		# print(formula.__str__())
		result = self.conjunction.infers(formula)
		# print("infers 1")
		# print(self.conjunction.__str__())
		if result:
			self.numToForm[list(self.numToForm.keys())[-1]] = formula
			# self.conjunction = AndFormula(*(self.numToForm.values()))
		# print("infered 2")
		# print(self.conjunction.__str__())

		return result




class AndFormula(Proof):
	"""Formula object representing a conjunction which will serve also as a
	proof object for nested assumption proofs. It is also used to create
	one massive formula when each formula is proved. I.e., if A is proved, then
	B is proved, then an next = AndFormula(A, B) would be constructed. If C is
	then proved, then next = AndFormula(next, C).
	"""

	def __init__(self, *formulas):
		self.ass = list(formulas)
		listFormula = []
		for f in list(formulas):
			listFormula.extend(listOfAtoms(f))

		self.formulas = list(set(listFormula))

	def __str__(self):
		return ' * '.join(f.__str__() for f in self.formulas)

	def __hash__(self):
		return sum([form.__hash__() for form in self.formulas])

	def __eq__(self, other):
		try:
			left = list(self.formulas)
			right = list(other.formulas)
			try:
				for rightFormula in right:
					left.remove(rightFormula)
			except ValueError:
				return False
			return not left
		except AttributeError:
			return False

	def infers(self, formula):
		'''
		Validation of a proof. 
		'''
		# append implementations of intro validation here per type of formula
		# E.g, self.infers(A->B), self.infers(A + B), self.infers(~A)
		# if (type(formula) is AndFormula) or (type(formula) is Formula):
		# 	return formula in self.eliminationList()
		# elif type(formula) is ImpFormula:
		# 	e = self.eliminationList()
		# 	return (formula.left in e) and \
		# 	(formula.right in e)
		# if type(formula) is ImpFormula:
			# print([x.__str__() for x in self.eliminationList()])
		return formula in self.eliminationList()
		# if type(formula) is ImpFormula:
		# reurn assumption == formula.left and formula.right in eliminationList
			# write implementation here about assumption

	def eliminationList(self):
		result = self.formulas[:]
		result.append(self)
		max_len = len(self.formulas)
		for L in range(2, max_len):
			for f in combinations(self.formulas, L):
				result.append(AndFormula(*f))

		# might have a problem here when having imp within imp
		# implies elimination here
		for impFormula in result:
			# if type(impFormula) is ImpFormula:
				# print('IMPLIES FORMULA IS')
				# print(impFormula.__str__())
			if type(impFormula) is ImpFormula and impFormula.left in result:
				# print("appending")
				# print(impFormula.right.__str__())
				result.append(impFormula.right)
		return result

class Formula(Proof):
	"""Formula object representing an atom through a character."""

	def __init__(self, formula):
		self.formula = formula

	def __str__(self):
		return self.formula

	def __eq__(self, other):
		return self.__str__() == other.__str__()

	def __hash__(self):
		return ord(self.formula)

	def infers(self, formula):
		return self == formula

class ImpFormula(Proof):

	def __init__(self, left, right):
		self.left = left
		self.right = right

	def __str__(self):
		return ' -> '.join([self.left.__str__(), self.right.__str__()])

	def __hash__(self):
		return self.left.__hash__() + self.right.__hash__()

	def __eq__(self, other):
		# print(self.__str__())
		try:
			return (self.left == other.left) and (self.right == other.right)
		except AttributeError:
			return False

	def infers(self, formula):
		return self == formula
