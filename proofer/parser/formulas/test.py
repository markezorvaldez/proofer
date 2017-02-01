import sys
import unittest
import naturaldeduction as nat
from naturaldeduction import Proof, AndFormula, Formula, \
	OrFormula, ImpFormula, NotFormula, FalseFormula, TrueFormula
class TestFormulaObjects(unittest.TestCase):
	"""Test suite for testing formula objects and its derivatives."""
	# might have problems because infers also appends objects
	# meaning self.ab might not just be self.ab

	a = nat.Formula("A")
	b = nat.Formula("B")
	c = nat.Formula("C")
	d = nat.Formula("D")
	ab = nat.AndFormula(a, b)
	ba = nat.AndFormula(b, a)
	ac = nat.AndFormula(a, c)
	ca = nat.AndFormula(c, a)
	ad = nat.AndFormula(a, d)
	bc = nat.AndFormula(b, c)
	cd = nat.AndFormula(c, d)
	abc = nat.AndFormula(a, b, c)
	abcd1 = nat.AndFormula(a, b, c, d)
	abcd2 = nat.AndFormula(ab, cd)
	abcd3 = nat.AndFormula(abc, d)
	abcd4 = nat.AndFormula(ab, c, d)
	dab = nat.AndFormula(d, a, b)

	def test_ab_infers_a(self):
		self.assertTrue(self.ab.infers(self.a))

	def test_abc_infers_ab(self):
		self.assertTrue(self.abc.infers(self.ab))

	def test_abc_infers_ba(self):
		self.assertTrue(self.abc.infers(self.ba))

	def test_ab_not_infers_ac(self):
		self.assertFalse(self.ab.infers(self.ac))

	def test_ac_not_infers_ab(self):
		self.assertFalse(self.ac.infers(self.ab))

	def test_ac_infers_ac(self):
		self.assertTrue(self.ac.infers(self.ac))

	def test_ac_infers_ca(self):
		self.assertTrue(self.ac.infers(self.ca))
		self.assertTrue(self.ca.infers(self.ac))

	def test_abc_not_infers_abcd(self):
		self.assertFalse(self.abc.infers(self.abcd1))

	def test_abcd_andformula_variations_infers_abcd(self):
		self.assertTrue(self.abcd2.infers(self.abcd1))
		self.assertTrue(self.abcd3.infers(self.abcd1))
		self.assertTrue(self.abcd2.infers(self.abcd3))
		self.assertTrue(self.abcd3.infers(self.abcd4))
	 
	def test_dab(self):
		self.assertTrue(self.abcd1.infers(self.dab))

	def test_proof(self):
		proof = nat.Proof(self.abcd1)
		self.assertTrue(proof.infers(self.abc))

	def test_implies(self):
		bIc = nat.ImpFormula(self.b, self.c)
		aIbIc = nat.ImpFormula(self.a, bIc)

		proof1 = nat.Proof(aIbIc)
		
		proof = nat.Proof(self.ab, parent = proof1)
		self.assertTrue(proof.infers(self.a))
		self.assertTrue(proof.infers(bIc))

		self.assertTrue(proof.infers(self.b))

		self.assertTrue(proof.infers(self.c))

		# print(proof.conjunction)
		abIc = nat.ImpFormula(self.ab, self.c)
		aibIc = nat.ImpFormula(self.a, self.bc)
		self.assertTrue(proof.proves(abIc))
		self.assertFalse(proof.proves(aibIc))

		# proof2 = nat.Proof(aIbIc)
		# self.assertTrue(proof2.proves(abIc))

	def test_implies2(self):
		bIc = nat.ImpFormula(self.b, self.c)
		aIbIc = nat.ImpFormula(self.a, bIc)
		abIc = nat.ImpFormula(self.ab, self.c)
		proof1 = nat.Proof(aIbIc, goal = abIc)
		proof2 = nat.Proof(self.ab, parent = proof1, goal = self.c)
		self.assertTrue(proof2.infers(self.a))
		self.assertTrue(proof2.infers(bIc))
		self.assertTrue(proof2.infers(self.b))
		self.assertTrue(proof2.infers(self.c))
		self.assertTrue(proof1.infers(abIc))

	def test_implies3(self):
		bIc = nat.ImpFormula(self.b, self.c)
		aIbIc = nat.ImpFormula(self.a, bIc)
		abIc = nat.ImpFormula(self.ab, self.c)
		proof1 = nat.Proof(aIbIc, goal = abIc)
		proof2 = nat.Proof(self.ab, parent = proof1, goal = self.c)
		# self.assertTrue(proof2.infers(self.ab))
		self.assertTrue(proof2.infers(bIc)) # should be false since a isnt yet
		self.assertFalse(proof2.infers(abIc))
		self.assertTrue(proof2.infers(self.c))
		self.assertTrue(proof1.infers(abIc))

	def test_or_implies(self):
		aIc = nat.ImpFormula(self.a, self.c)
		bIc = nat.ImpFormula(self.b, self.c)
		aOb = nat.OrFormula(self.a, self.b)
		aObIc = nat.ImpFormula(aOb, self.c)
		proof1 = nat.Proof(aIc, bIc, goal = aObIc)
		proof2 = nat.Proof(aOb, parent = proof1, goal = self.c)
		proof3 = nat.Proof(self.a, parent = proof2, goal = self.c)
		proof4 = nat.Proof(self.b, parent = proof2, goal = self.c)
		self.assertTrue(proof3.infers(self.c))
		self.assertTrue(proof4.infers(self.c))
		# print([f.__str__() for f in proof2.conjunction.formulas])
		self.assertTrue(proof2.infers(self.c))

	def test_negate_formula(self):
		Na = nat.NotFormula(self.a)
		self.assertFalse(Na == self.a)
		self.assertFalse(self.a == Na)
		Nab = nat.NotFormula(self.ab)
		Nba = nat.NotFormula(self.ba)
		self.assertTrue(Nba == Nab)

	def test_negate_proof(self):
		s = nat.Formula("s")
		b = nat.Formula('b')
		w = nat.Formula('w')
		sIb = nat.ImpFormula(s, b)
		bIw = nat.ImpFormula(b, w)
		Nw = nat.NotFormula(w)
		Ns = nat.NotFormula(s)
		F = nat.FalseFormula()
		proof1 = nat.Proof(sIb, bIw, Nw, goal = Ns)
		proof2 = nat.Proof(s, parent = proof1, goal = F)
		self.assertTrue(proof2.infers(b))
		self.assertTrue(proof2.infers(w))
		self.assertTrue(proof2.infers(F))
		self.assertTrue(proof1.infers(Ns))

	def test_or_not_proof(self):
		c = nat.Formula("C")
		d = nat.Formula("D")
		cOd = nat.OrFormula(c, d)
		NcOd = nat.NotFormula(cOd)
		Nc = nat.NotFormula(c)
		F = nat.FalseFormula()
		proof1 = nat.Proof(NcOd, goal = Nc)
		proof2 = nat.Proof(c, parent = proof1, goal = F)
		# print(proof2.conjunction.__str__())
		self.assertTrue(proof2.infers(cOd))
		# print(proof2.conjunction.__str__())
		self.assertTrue(proof2.infers(F))
		self.assertTrue(proof1.infers(Nc))

	def test_false_any_proof(self):
		e = nat.Formula("E")
		f = nat.FalseFormula()
		ne = nat.NotFormula(e)
		proof1 = nat.Proof(f, goal = e)
		proof2 = nat.Proof(ne, parent = proof1, \
			goal = f)
		self.assertTrue(proof2.infers(f))
		self.assertTrue(proof1.infers(nat.NotFormula(ne)))

	def test_example_5_11(self):
		A = nat.Formula("A")
		B = nat.Formula("B")
		C = nat.Formula("C")
		F = nat.FalseFormula()
		AOB = nat.OrFormula(A, B)
		NA = nat.NotFormula(A)
		NC = nat.NotFormula(C)
		BANC = nat.AndFormula(B, NC)
		NBANC = nat.NotFormula(BANC)
		proof1 = nat.Proof(AOB, nat.ImpFormula(NC, NA), NBANC, goal = C)
		proof2 = nat.Proof(NC, parent = proof1, goal = F)
		self.assertTrue(proof2.infers(NA))
		proof2_1 = nat.Proof(A, parent = proof2, goal = B)
		self.assertTrue(proof2_1.infers(F))
		self.assertTrue(proof2_1.infers(B))
		proof2_2 = nat.Proof(B, parent = proof2, goal = B)
		self.assertTrue(proof2_2.infers(B))
		self.assertTrue(proof2.infers(B))
		self.assertTrue(proof2.infers(BANC))
		# print(BANC)
		# print(type(BANC))
		# print(proof2.conjunction)
		# print([f.__str__() for f in proof2.conjunction.eliminationList])
		# problem is that conjunction is being broken down which shouldn't be
		#
		self.assertTrue(proof2.infers(F))
		self.assertTrue(proof1.infers(C))
		# infers(C) should work, just implement

	def test_example_lemma(self):
		F = FalseFormula()
		a = self.a
		na = NotFormula(a)
		aOna = OrFormula(a, na)
		NaOna = NotFormula(aOna)
		proof = Proof(TrueFormula(), goal = aOna)
		proof1 = Proof(NaOna, parent = proof,  goal = F)
		proof2 = Proof(a, parent = proof1, goal = F)
		self.assertTrue(proof2.infers(aOna))
		self.assertTrue(proof2.infers(F))
		self.assertTrue(proof1.infers(na))
		self.assertTrue(proof1.infers(aOna))
		self.assertTrue(proof1.infers(F))
		self.assertTrue(proof.infers(NotFormula(NaOna)))
		self.assertTrue(proof.infers(aOna))
		# print(proof.conjunction)

	def test_example_piercelaw(self):
		a = self.a
		b = self.b
		aIb = ImpFormula(a, b)
		aIbIa = ImpFormula(aIb, a)
		aONa = OrFormula(a, NotFormula(a))
		F = FalseFormula()
		proof1 = Proof(TrueFormula(), goal = ImpFormula(aIbIa, a))
		proof2 = Proof(aIbIa, OrFormula(a, NotFormula(a)), parent = proof1, \
			goal = a)
		proof2_1 = Proof(a, parent = proof2, goal = a)
		self.assertTrue(proof2_1.infers(a))
		proof2_2 = Proof(NotFormula(a), parent = proof2, goal = a)
		proof2_2_1 = Proof(a, parent = proof2_2, goal = b)
		self.assertTrue(proof2_2_1.infers(F))
		self.assertTrue(proof2_2_1.infers(b))
		self.assertTrue(proof2_2.infers(aIb))
		self.assertTrue(proof2_2.infers(a))
		self.assertTrue(proof2.infers(a))
		print(proof1.conjunction)
		self.assertTrue(proof1.infers(ImpFormula(aIbIa, a)))
if __name__ == '__main__':
	unittest.main()