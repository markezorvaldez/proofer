import sys
import naturaldeduction as nat

sys.path.insert(0, "../..")

if sys.version_info[0] >= 3:
    raw_input = input


def testAndFormulaInfers1():
	formulaA = nat.Formula("A")
	formulaB = nat.Formula("B")
	ab = nat.AndFormula(formulaA, formulaB)

	print("A * B infers A?")
	print(ab.infers(formulaA))

def testAndFormulaInfers2():
	a = nat.Formula("A")
	b = nat.Formula("B")
	c = nat.Formula("C")
	ab = nat.AndFormula(a, b)
	abc = nat.AndFormula(a, b, c)

	print("ABC infers AB?")
	print(abc.infers(ab))

def testAndFormulaInfers3():
	a = nat.Formula("A")
	b = nat.Formula("B")
	c = nat.Formula("C")
	ba = nat.AndFormula(b, a)
	abc = nat.AndFormula(a, b, c)

	print("ABC infers BA?")
	print(abc.infers(ba))

def testAndFormulaInfers4():
	a = nat.Formula("A")
	b = nat.Formula("B")
	c = nat.Formula("C")
	ab = nat.AndFormula(a, b)
	ac = nat.AndFormula(a, c)
	ca = nat.AndFormula(c, a)

	print("AB infers AC?")
	print(ab.infers(ac))
	print("AC infers AB?")
	print(ac.infers(ab))
	print("AC infers AC?")
	print(ac.infers(ac))
	print("AC infers CA?")
	print(ac.infers(ca))


def testAndFormula():
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

	print("AB infers A?")
	print(ab.infers(a))

	print("ABC infers AB?")
	print(abc.infers(ab))

	print("ABC infers BA?")
	print(abc.infers(ba))

	print("AB infers AC?")
	print(ab.infers(ac))

	print("AC infers AB?")
	print(ac.infers(ab))

	print("AC infers AC?")
	print(ac.infers(ac))

	print("AC infers CA?")
	print(ac.infers(ca))

	print("ABC infers ABCD?")
	print(abc.infers(abcd1))

	print("AB * CD infers ABCD?")
	print(abcd2.infers(abcd1))

	print("ABC * D infers ABCD?")
	print(abcd3.infers(abcd1))

	print("AB * CD infers ABC * D?")
	print(abcd2.infers(abcd3))



print("---------------------------     TEST     ------------------------")
# testAndFormulaInfers1()
# testAndFormulaInfers2()
# testAndFormulaInfers3()
# testAndFormulaInfers4()
testAndFormula()