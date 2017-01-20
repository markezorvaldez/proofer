PLY_PATH = "/Users/mark/ply-3.9/"
FORMULAS_PATH = "/Users/mark/proofer/proofer/parser/"
import sys

sys.path.insert(0, "../..")
sys.path.append(PLY_PATH)
sys.path.append(FORMULAS_PATH)

from formulas.naturaldeduction import Formula, AndFormula

if sys.version_info[0] >= 3:
    raw_input = input

tokens = (
    'ATOM',
    'AND',
    'LPAREN','RPAREN',
    )

# Tokens

t_AND     = r'\*'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_ATOM    = r'[a-zA-Z_]'


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
    )

# dictionary of names
atoms = { }
andFormula = None


def p_statement_expr(t):
    'statement : expression'
    global andFormula
    andFormula = t[1]
    print(t[1])

def p_expression_atom(t):
    'expression : ATOM'
    try:
        form = atoms[t[1]]
        t[0] = AndFormula(andFormula, form)
    except LookupError:
        if andFormula is not None:
            print("can not prove")
            t[0] = andFormula
        else:
            atoms[t[1]] = Formula(t[1])
            t[0] = atoms[t[1]]

def p_expression_andformula(t):
    'expression : expression AND expression'
    newAndFormula = AndFormula(t[1], t[3])
    if andFormula is None:
        t[0] = newAndFormula
    elif andFormula.infers(newAndFormula):
        t[0] = AndFormula(andFormula, newAndFormula)
    else:
        print("cannot prove")
        t[0] = andFormula

def p_expression_group(t):
    'expression : LPAREN expression RPAREN'
    t[0] = t[2]

def p_error(t):
    print("Syntax error at '%s'" % t.value)

import ply.yacc as yacc
localparser = yacc.yacc()

def parse_premise(s):
    localparser.parse(s)
    return(andFormula)

# while 1:
#     try:
#         s = raw_input('proof > ')
#     except EOFError:
#         break
#     if not s:
#         continue
#     localparser.parse(s)