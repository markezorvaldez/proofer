import sys
from itertools import combinations
sys.path.insert(0, "../..")

if sys.version_info[0] >= 3:
    raw_input = input


class Formula:
	"""Formula object representing an atom through a character."""

	def __init__(self, formula):
		self.formula = formula

	def __str__(self):
		return self.formula

	def __eq__(self, other):
		return self.__str__() == other.__str__()

	def infers(self, formula):
		return self.__str__() == formula.__str__()

class AndFormula(Formula):
	"""Formula object representing a conjunction. It is also used to create
	one massive formula when each formula is proved. I.e., when A is proved
	and B is proved, a AndFormula object is constructed which will be used
	to prove the next line in the proof.
	"""

	def __init__(self, *formulas):
		self.formulas = list(formulas)

	def __str__(self):
		return ' * '.join(f.__str__() for f in self.formulas)

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
		return formula in self.eliminationList()

	def eliminationList(self):
		result = self.formulas[:]
		result.append(self)
		max_len = len(self.formulas)
		for L in range(2, max_len):
			for f in combinations(self.formulas, L):
				result.append(AndFormula(*f))

		return result
