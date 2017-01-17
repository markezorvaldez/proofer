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

	print("A * B * C infers A * B?")
	print(abc.infers(ab))

def testAndFormulaInfers3():
	a = nat.Formula("A")
	b = nat.Formula("B")
	c = nat.Formula("C")
	ba = nat.AndFormula(b, a)
	abc = nat.AndFormula(a, b, c)

	print("A * B * C infers B * A?")
	print(abc.infers(ba))

def testAndFormulaInfers4():
	a = nat.Formula("A")
	b = nat.Formula("B")
	c = nat.Formula("C")
	ab = nat.AndFormula(a, b)
	ac = nat.AndFormula(a, c)

	print("AB infers AC?")
	print(ab.infers(ac))
	# print(ac.infers(ab))
	print([f.__str__() for f in ab.eliminationList()])
	print([f.__str__() for f in ac.eliminationList()])

print("---------------------------     TEST     ------------------------")
testAndFormulaInfers1()
testAndFormulaInfers2()
testAndFormulaInfers3()
testAndFormulaInfers4()