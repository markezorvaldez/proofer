import sys
import unittest
import naturaldeduction as nat

class TestFormulaObjects(unittest.TestCase):
	"""Test suite for testing formula objects and its derivatives."""

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

		proof = nat.Proof(self.ab, conjunction = [aIbIc])
		self.assertTrue(proof.infers(self.a))
		self.assertTrue(proof.infers(bIc))
		self.assertTrue(proof.infers(self.b))
		self.assertTrue(proof.infers(self.c))
		print(proof.conjunction)
		abIc = nat.ImpFormula(self.ab, self.c)
		aibIc = nat.ImpFormula(self.a, self.bc)
		self.assertTrue(proof.proves(abIc))
		self.assertFalse(proof.proves(aibIc))

		print("ADKJFAL;SDKFJA;SDFLASDFJ")
		proof2 = nat.Proof(aIbIc)
		self.assertTrue(proof2.proves(abIc))

if __name__ == '__main__':
	unittest.main()