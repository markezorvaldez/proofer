import sys
from itertools import combinations
sys.path.insert(0, "../..")

if sys.version_info[0] >= 3:
    raw_input = input


class Formula:


	def __init__(self, formula):
		self.formula = formula

	def __str__(self):
		return self.formula

	def __eq__(self, other):
		return self.canProve(other)

	def canProve(self, formula):
		# print("canProve")
		# print(self)
		# print(formula)
		# print("self: " + self.__str__())
		# print("other: " + formula.__str__())
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

	def canProve(self, formula):
		result = False
		for f in self.formulas:
			result = result or f.canProve(formula)
		return result

	def infers(self, formula):
		return formula in self.eliminationList()

	def eliminationList(self):
		# A*B*C*D -> (A, B, C, A*B, A*C, A*D, B*C, B*D, C*D, A*B*C, A*B*D,
		#             A*C*D, B*C*D)
		# print("eliminating " + self.__str__())
		result = self.formulas[:]
		max_len = len(self.formulas)
		# print([s.__str__() for s in result])
		for L in range(2, max_len):
			# print("length at the moment is " + str(L))
			for f in combinations(self.formulas, L):
				# print("length of formulas is " + str(len(self.formulas)))
				# print("value of maxlen is " + str(max_len))
				result.append(AndFormula(*f))
			# print([s.__str__() for s in result])
		# print("hello")
		return result


# formulaA = Formula("A")
# formulaB = Formula("B")
# formulaC = Formula("C")
# formulaD = Formula("D")
# formulaE = Formula("E")
# abcd = AndFormula(formulaA, formulaB, formulaC, formulaD)
# abc = AndFormula(formulaA, formulaB, formulaC)
# ab = AndFormula(formulaA, formulaB)
# ba = AndFormula(formulaB, formulaA)
# bca = AndFormula(formulaB, formulaC, formulaA)
# ae = AndFormula(formulaA, formulaE)
# print(abcd.canProve(formulaA))
# # print(abcd)
# # print(ab)
# # print(abcd.canProve(ab))
# # elim = abcd.eliminationList()
# # print(len(elim))
# # print(ab in elim)
# # print(ba in elim)
# # print(bca in elim)
# # print(abcd in elim)
# # print(ae in elim) # should be false but true
# # print(formulaE in elim)
# # print([f.__str__() for f in elim])
# # print(elim)
# print(ae == formulaA)
# print(formulaA == ae)