import sys
from itertools import combinations, groupby
from functools import reduce
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
			if formula == self.goal:
				newForm = ImpFormula(AndFormula(*self.ass), self.goal)
				try:
					self.parent.conjunction.append(newForm)
					self.parent.conjunction.appendElim(newForm)
				except AttributeError:
					pass
		return result

	def proves(self, formula):
		# only works for implies formula
		return formula.left in self.ass and formula.right in \
			self.conjunction.eliminationList

	def end(self):
		imp = ImpFormula(AndFormula(*self.ass), self.conjunction.formulas[-1])
		try:
			self.parent.conjunction.append(imp)
			self.parent.conjunction.appendElim(imp)
		except AttributeError:
			print('attribute error')
			pass

	def provable(self):

		return False

	# think of an architecture of nesting proofs
	# can do observer 
	# def assumption(self, proof):
		

class AndFormula:
	'''
	Formula object representing a conjunction which serves as a aggregate for
	a proof by joining formulas as one conjunction.
	'''
	
	#problem with assumption being an AndFormula
	# def __new__(cls, *formulas, lineNumber = 1):
	# 	if len(list(formulas)) == 1:
	# 		return list(formulas)[0]
	# 	else:
	# 		return super(AndFormula, cls).__new__(cls)

	def __init__(self, *formulas, lineNumber = 1):
		'''
		Constructs an AndFormula object. If formulas contain an AndFormula,
		it will be broken apart into elements until it is not an AndFormula so
		that the original object is a conjunction not consisting of 
		AndFormulas. 
		I.e., (A * B) * (A * C) * (D -> (E * F)) = A * B * C * (D -> (E * F))
		'''
		# conjunction should not be broken down 

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
		return reduce(lambda x,y: x*y, [z.__hash__() for z in self.formulas])

	def __eq__(self, other):
		if len(self.formulas) == 1:
			return self.formulas[0] == other
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
		self.eliminationList.extend(x for x in f \
			if x not in self.eliminationList)

	def infers(self, formula):
		'''
		Validates a proof.
		Finds if formula is contained in the elimination list.
		If conjunction is A -> (B -> C) * (A * B), then B -> C infers
		because the code will eliminate formulas (E.g., A) to see if B -> C
		can be infered or not.
		'''
		# starts by finding if each element alone can infer formula, else
		# combinations of formulas will be made into a conjunction to see if
		# they can infer formula and so on
		# eliminationList will be appended 
		# result = formula in self.
		# PROBLEM - if ~~E == ~(~E) and (~E) is an AndFormula, wrote temp sol

		result = formula in self.eliminationList
		if result:
			self.append(formula)
			return result

		# might need to refactor all of these
		for f in self.eliminationList:
			if type(f) is ImpFormula and f.left in self.eliminationList:
				self.appendElim(f.right)
				if formula == f.right:
					self.append(formula)
					return True
				# check now if formula in elimList
			elif type(f) is ImpFormula and f.right == FalseFormula():
				x = NotFormula(f.left)
				self.appendElim(x)
				if x == formula:
					self.append(x)
					return True
			elif type(f) is OrFormula:
				conclusion = []
				for fo in f.formulas:
					conclusion.extend([x.right for x in self.eliminationList \
						if type(x) is ImpFormula and x.left == fo \
						and x.right not in conclusion])
				for fo in conclusion:
					self.appendElim(fo)
					self.append(fo)
				try:
					if formula == conclusion[0]:
						return reduce(lambda x,y: x and y, conclusion)
				except IndexError:
					pass
			elif type(f) is NotFormula and f.formula in self.eliminationList:
				x = FalseFormula()
				self.appendElim(x)
				if formula == x:
					self.append(x)
					return True
			elif type(f) is NotFormula and type(f.formula) is NotFormula:
				x = f.formula.formula
				self.appendElim(x)
				if formula == x:
					self.append(x)
					return True
			elif type(f) is NotFormula and type(f.formula) is AndFormula:
				a = f.formula
				l = len(a.formulas)
				if l == 1 and type(a.formulas[0]) is NotFormula:
					z = a.formulas[0].formula
					self.appendElim(z)
					if formula == z:
						self.append(z)
						return True
				x = [a==AndFormula(*b) for b in combinations(self.formulas, l)]
				y = reduce(lambda g,h: g or h, x)
				if y:
					self.appendElim(FalseFormula())
					self.append(FalseFormula())
					return True
			elif type(f) is FalseFormula:
				self.appendElim(formula)
				self.append(formula)
				return True

		if type(formula) is AndFormula:
			numConjs = len(formula.formulas)
			for f in combinations(self.formulas, numConjs):
				# f is a numConjs-tuple that needs to be AndFormula
				x = AndFormula(*f)
				self.appendElim(x)
				if formula == x:
					self.append(formula)
					return True

		if type(formula) is OrFormula:
			for f in formula.formulas:
				if f in self.eliminationList:
					self.appendElim(formula)
					self.append(formula)
					return True
		return False

		# also implement falsity implies everything

class OrFormula:
	'''
	Object representing a disjunction.
	'''

	def __init__(self, *formulas):
		'''
		Constructs an OrFormula object. Since the or operator is commutative,
		it can be initialised like an AndFormula object as above.
		'''

		listFormula = []
		for f in list(formulas):
			l = listOfAtoms(f)
			listFormula.extend(l)
		self.formulas = list(set(listFormula))

	def __str__(self):
		return '(' + ' + '.join(f.__str__() for f in self.formulas) + ')'

	def truthTable(self):
		listOfForms = list(self.formulas)
		

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

	def __hash__(self):
		return sum([form.__hash__() for form in self.formulas])

	def infers(self, formula):
		return self == formula

class Formula:
	"""Formula object representing an atom through a character."""

	def __init__(self, formula):
		self.formula = formula

	def truthTable(self):
		return [1, 0]

	def __str__(self):
		return self.formula

	def __eq__(self, other):
		return self.__str__() == other.__str__()

	def __hash__(self):
		return ord(self.formula)

	def infers(self, formula):
		return self == formula

class ImpFormula:

	def __init__(self, left, right):
		self.left = left
		self.right = right

	def truthTable(self):
		lt = self.left.truthTable
		rt = self.right.truthTable
		r = []
		for t in lt:
			r.extend([(not t) or ts for ts in rt])

		return r

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

class NotFormula:

	def __init__(self, formula):
		self.formula = formula

	# def __new__(cls, formula):
	# 	if type(formula) is NotFormula:
	# 		print("HERER")
	# 		C = type(formula.formula)
	# 		return C.C(formula)
	# 	else:
	# 		return cls.__init__(cls, formula)
	def truthTable(self):
		return [not x for x in self.formula.truthTable]

	def __str__(self):
		return '~' + self.formula.__str__()

	def __hash__(self):
		return -1*self.formula.__hash__()

	def __eq__(self, other):
		if type(other) is AndFormula:
			return other.__eq__(self)
		return type(other) is NotFormula and self.formula == other.formula

	def infers(self, formula):
		return self == formula

class FalseFormula:
	# def __init__(self):
		# self.formula = self

	def truthTable(self):
		return [0]

	def __str__(self):
		return "FALSITY"


	def __hash__(self):
		return -1

	def __eq__(self, other):
		return type(other) is FalseFormula

	def infers(self, formula):
		return self == formula

class TrueFormula:

	def truthTable(self):
		return [1]

	def __str__(self):
		return 'TRUTH'

	def __hash__(self):
		return 1

	def __eq__(self, other):
		return type(other) is TrueFormula

	def infers(self, formula):
		return self == formula