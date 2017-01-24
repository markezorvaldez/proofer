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
	so on.
	'''

	def __init__(self, *assumptions, parent = None, goal = None, lineNum = 1):
		'''
		Initialises a proof object with a list of assumptions and a goal.
		If the proof is within some proof, then the conjunction of the outside
		proof is used with the line number.
		'''

		self.ass = list(assumptions)
		self.parent = parent
		self.numToForm = {n:f for (n,f) in \
			zip(range(lineNum, len(self.ass)+1), self.ass)}
		try:
			self.conjunction = AndFormula(*self.ass, parent.conjunction)
		except AttributeError:
			self.conjunction = AndFormula(*self.ass)
		self.lineNum = len(self.ass)
		self.goal = goal

	def infers(self, formula):
		result = self.conjunction.infers(formula)
		if result:
			self.numToForm[list(self.numToForm.keys())[-1]] = formula
			if result == self.goal:
				parent.conjunction.append(\
					ImpFormula(AndFormula(*self.ass), self.goal))
		return result

	def proves(self, formula):
		# only works for implies formula
		return formula.left in self.ass and formula.right in \
			self.conjunction.eliminationList

	# think of an architecture of nesting proofs
	# can do observer 
	# def assumption(self, proof):
		

class AndFormula(Proof):
	'''
	Formula object representing a conjunction which serves as a aggregate for
	a proof by joining formulas as one conjunction.
	'''

	def __init__(self, *formulas, lineNumber = 1):
		'''
		Constructs an AndFormula object. If formulas contain an AndFormula,
		it will be broken apart into elements until it is not an AndFormula so
		that the original object is a conjunction not consisting of 
		AndFormulas. 
		I.e., (A * B) * (A * C) * (D -> (E * F)) = A * B * C * (D -> (E * F))
		'''

		listFormula = []
		self.lineNumber = lineNumber
		# self.formNumDict = { }
		for f in list(formulas):
			l = listOfAtoms(f)
			listFormula.extend(l)
			# for a in l:
				# self.formNumDict[a] = lineNumber
			self.lineNumber += 1

		self.formulas = list(set(listFormula))
		self.eliminationList = list(set(listFormula))

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

	def append(self, formula):
		'''
		Appends a formula to the conjunction. If formula is AndFormula,
		it is broken down into non conjunctions and appended.
		'''

		f = listOfAtoms(formula)

		self.formulas.extend(x for x in f if x not in self.formulas)

	def appendElim(self, formula):
		'''
		Appends a formula to the eliminationList. If the formula is AndFormula,
		it is broken down into non conjunctions and appended.
		'''

		f = listOfAtoms(formula)
		self.eliminationList.extend(x for x in f if x not in self.formulas)

	def infers(self, formula):
		'''
		Validation of a proof. 
		'''
		# starts by finding if each element alone can infer formula, else
		# combinations of formulas will be made into a conjunction to see if
		# they can infer formula and so on
		# eliminationList will be appended 
		# result = formula in self.


		result = formula in self.eliminationList
		if result:
			self.append(formula)
			return result

		for f in self.eliminationList:
			if type(f) is ImpFormula and f.left in self.eliminationList:
				self.appendElim(f.right)
				if formula is f.right:
					self.append(formula)
					return True
				# check now if formula in elimList
		if type(formula) is AndFormula:
			numConjs = len(formula.formulas)
			for f in combinations(self.formulas, numConjs):
				# f is a numConjs-tuple that needs to be AndFormula
				x = AndFormula(*f)
				self.appendElim(x)
				if formula == x:
					self.append(formula)
					return True
		return False


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
		return '('+' -> '.join([self.left.__str__(), self.right.__str__()])+')'

	def __hash__(self):
		return self.left.__hash__() + self.right.__hash__()

	def __eq__(self, other):
		try:
			return (self.left == other.left) and (self.right == other.right)
		except AttributeError:
			return False

	def infers(self, formula):
		return self == formula
