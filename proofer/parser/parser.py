# -----------------------------------------------------------------------------
# calc.py
#
# A simple calculator with variables.   This is from O'Reilly's
# "Lex and Yacc", p. 63.
# -----------------------------------------------------------------------------

PLY_PATH = "/Users/mark/ply-3.9/"

import sys
sys.path.insert(0, "../..")
sys.path.append(PLY_PATH)

if sys.version_info[0] >= 3:
    raw_input = input

tokens = (
    'NAME','NUMBER',
    'OR','AND', 'IMPLIES', 'NEG','EQUALS',
    'LPAREN','RPAREN',
    )

# Tokens

t_OR      = r'\+'
t_AND     = r'\*'
t_IMPLIES = r'->'
t_NEG     = r'~'
t_EQUALS  = r'='
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_NAME    = r'[a-zA-Z_][a-zA-Z0-9_]*'

def t_NUMBER(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

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
    ('right', 'IMPLIES'),
    ('left','OR'),
    ('left','AND'),
    ('right', 'NEG'),
    )

# dictionary of names
names = { }
output = { }

def p_statement_assign(t):
    'statement : NAME EQUALS expression'
    names[t[1]] = t[3]

def p_statement_expr(t):
    'statement : expression'
    print(t[1])
    output[0] = t[1]

def p_expression_binop(t):
    '''expression : expression OR expression
                  | expression AND expression
                  | expression IMPLIES expression'''
    if t[2] == '+'   : t[0] = t[1] | t[3]
    elif t[2] == '*' : t[0] = t[1] & t[3]
    elif t[2] == '->': t[0] = (~t[1] & 1) | t[3]

def p_expression_uneg(p):
    "expression : NEG expression %prec NEG"
    p[0] = ~p[2] & 1

def p_expression_group(t):
    'expression : LPAREN expression RPAREN'
    t[0] = t[2]

def p_expression_number(t):
    'expression : NUMBER'
    t[0] = t[1]

def p_expression_name(t):
    'expression : NAME'
    try:
        t[0] = names[t[1]]
    except LookupError:
        print("Undefined name '%s'" % t[1])
        t[0] = 0

def p_error(t):
    print("Syntax error at '%s'" % t.value)

import ply.yacc as yacc
localparser = yacc.yacc()

while 1:
    try:
        s = raw_input('calc > ')
    except EOFError:
        break
    if not s:
        continue
    localparser.parse(s)
    print(output[0])

