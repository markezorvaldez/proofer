PLY_PATH = "/Users/mark/ply-3.9/"
FORMULAS_PATH = "/Users/mark/proofer/proofer/parser/"
import sys

sys.path.insert(0, "../..")
sys.path.append(PLY_PATH)
sys.path.append(FORMULAS_PATH)

from formulas.naturaldeduction import Formula, AndFormula, Proof, ImpFormula,OrFormula, NotFormula


tokens = (
    'PROVE',
    'ASS',
    'END',
    'ATOM',
    'AND',
    'IMP',
    'OR',
    'NOT',
    'LPAREN','RPAREN',
    )

# Tokens
t_PROVE   = r'=>'
t_ASS     = r'ASS'
t_END     = r'END'
t_AND     = r'\*'
t_IMP     = r'->'
t_OR      = r'\|'
t_NOT     = r'\~'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_ATOM    = r'[a-z]'


# Ignored characters
t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
    
# Build the lexer
import ply.lex as lex
lexer = lex.lex()

# Parsing rules

precedence = (
    ('left','AND'),
    ('left', 'IMP'),
    ('left', 'OR'),
    ('right', 'NOT')
    )

# dictionary of names
atoms = { }
andFormula = None
proof = None

def p_statement_proof(t):
    'statement : expression PROVE expression'
    global proof
    proof = Proof(t[1], goal = t[3])

def p_statement_ass(t):
    'statement : expression ASS'
    global proof
    global andFormula
    andFormula = True
    proof = Proof(t[1], parent = proof)


def p_statement_expr(t):
    # here we will do infer checks
    'statement : expression'
    global andFormula
    global proof
    res = proof.infers(t[1])
    andFormula = res

def p_statement_end(t):
    'statement : END'
    global proof
    global andFormula
    andFormula = True
    proof.end()
    proof = proof.parent

def p_expression_andformula(t):
    'expression : expression AND expression'
    t[0] = AndFormula(t[1], t[3])

def p_expression_impformula(t):
    'expression : expression IMP expression'
    t[0] = ImpFormula(t[1], t[3])

def p_expression_orformula(t):
    'expression : expression OR expression'
    t[0] = OrFormula(t[1], t[3])

def p_expression_notformula(t):
    'expression : NOT expression'
    t[0] = NotFormula(t[2])

def p_expression_group(t):
    'expression : LPAREN expression RPAREN'
    t[0] = t[2]

def p_expression_atom(t):
    'expression : ATOM'
    try:
        t[0] = atoms[t[1]]
    except LookupError:
        atoms[t[1]] = Formula(t[1])
        t[0] = atoms[t[1]]

def p_error(t):
    print("Syntax error at '%s'" % t.value)

import ply.yacc as yacc
localparser = yacc.yacc()


def parse_premise(s):
    localparser.parse(s)
    return(andFormula)
