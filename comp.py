from ply import ctokens as tokens
from ply import lex as lex
from ply import yacc as yacc

tokens = [
    # Literals (identifier, integer constant, float constant, string constant, char const)
    # 'ID', 'TYPEID', 'INTEGER', 'FLOAT', 'STRING', 'CHARACTER',
    'NUMBER',
    # Operators (+,-,*,/,%,|,&,~,^,<<,>>, ||, &&, !, <, <=, >, >=, ==, !=)
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MODULO',
    'OR', 'AND', 'NOT', 'XOR', 'LSHIFT', 'RSHIFT',
    'LOR', 'LAND', 'LNOT',
    # 'LT', 'LE', 'GT', 'GE', 'EQ', 'NE',
    
    # # Assignment (=, *=, /=, %=, +=, -=, <<=, >>=, &=, ^=, |=)
    # 'EQUALS', 'TIMESEQUAL', 'DIVEQUAL', 'MODEQUAL', 'PLUSEQUAL', 'MINUSEQUAL',
    # 'LSHIFTEQUAL','RSHIFTEQUAL', 'ANDEQUAL', 'XOREQUAL', 'OREQUAL',

    # # Increment/decrement (++,--)
    # 'INCREMENT', 'DECREMENT',

    # # Ternary operator (?)
    # 'TERNARY',
    
    # Delimeters ( ) [ ] { } , . ; :
    'LPAREN', 'RPAREN',
    # 'LBRACKET', 'RBRACKET',
    # 'LBRACE', 'RBRACE',
    # 'COMMA', 'PERIOD', 'SEMI', 'COLON',

    
]
    
# Operators
t_PLUS             = r'\+'
t_MINUS            = r'-'
t_TIMES            = r'\*'
t_DIVIDE           = r'/'
t_MODULO           = r'%'
t_OR               = r'\|'
t_AND              = r'&'
t_NOT              = r'~'
t_XOR              = r'\^'
t_LSHIFT           = r'<<'
t_RSHIFT           = r'>>'
t_LOR              = r'\|\|'
t_LAND             = r'&&'
t_LNOT             = r'!'
# t_LT               = r'<'
# t_GT               = r'>'
# t_LE               = r'<='
# t_GE               = r'>='
# t_EQ               = r'=='
# t_NE               = r'!='

# # Assignment operators

# t_EQUALS           = r'='
# t_TIMESEQUAL       = r'\*='
# t_DIVEQUAL         = r'/='
# t_MODEQUAL         = r'%='
# t_PLUSEQUAL        = r'\+='
# t_MINUSEQUAL       = r'-='
# t_LSHIFTEQUAL      = r'<<='
# t_RSHIFTEQUAL      = r'>>='
# t_ANDEQUAL         = r'&='
# t_OREQUAL          = r'\|='
# t_XOREQUAL         = r'\^='

# # Increment/decrement
# t_INCREMENT        = r'\+\+'
# t_DECREMENT        = r'--'

# # ?
# t_TERNARY          = r'\?'

# Delimeters
t_LPAREN           = r'\('
t_RPAREN           = r'\)'
# t_LBRACKET         = r'\['
# t_RBRACKET         = r'\]'
# t_LBRACE           = r'\{'
# t_RBRACE           = r'\}'
# t_COMMA            = r','
# t_PERIOD           = r'\.'
# t_SEMI             = r';'
# t_COLON            = r':'


# # Identifiers
# t_ID = r'[A-Za-z_][A-Za-z0-9_]*'

# # Integer literal
# t_INTEGER = r'\d+([uU]|[lL]|[uU][lL]|[lL][uU])?'

# # Floating literal
# t_FLOAT = r'((\d+)(\.\d+)(e(\+|-)?(\d+))? | (\d+)e(\+|-)?(\d+))([lL]|[fF])?'

# # String literal
# t_STRING = r'\"([^\\\n]|(\\.))*?\"'

# # Character constant 'c' or L'c'
# t_CHARACTER = r'(L)?\'([^\\\n]|(\\.))*?\''

# Comment (C-Style)
def t_COMMENT(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')
    return t

# # Comment (C++-Style)
# def t_CPPCOMMENT(t):
#     r'//.*\n'
#     t.lexer.lineno += 1
#     return t

def t_NUMBER( t ) :
    r'[0-9]+'
    t.value = int( t.value )
    return t

def t_newline( t ):
  r'\n+'
  t.lexer.lineno += len( t.value )

def t_error( t ):
  #print("Invalid Token:",t.value[0])
  t.lexer.skip( 1 )

lexer = lex.lex()

precedence = (
    ( 'left', 'PLUS', 'MINUS' ),
    ( 'left', 'TIMES', 'DIVIDE' ),
    ( 'nonassoc', 'UMINUS' )
)

# Addition

def p_add( p ) :
    'expr : expr PLUS expr'
    p[0] = p[1] + p[3]

# Substraction

def p_sub( p ) :
    'expr : expr MINUS expr'
    p[0] = p[1] - p[3]

# conversion of positive to negative

def p_expr2uminus( p ) :
    'expr : MINUS expr %prec UMINUS'
    p[0] = - p[2]

# Multiplication and Division

def p_mult_div( p ) :
    '''expr : expr TIMES expr
            | expr DIVIDE expr'''

    if p[2] == '*' :
        p[0] = p[1] * p[3]
    else :
        if p[3] == 0 :
            print("Can't divide by 0")
            raise ZeroDivisionError('integer division by 0')
        p[0] = p[1] / p[3]

# Modulus

def p_modulus( p ) :
	'expr : expr MODULO expr'
	p[0] = p[1] % p[3]

# Bitwise Operations

# OR
def p_or( p ) :
	'expr : expr OR expr'
	p[0] = p[1] | p[3]

# AND
def p_and( p ) :
	'expr : expr AND expr'
	p[0] = p[1] & p[3]

# NOT
def p_not( p ) :
	'expr : NOT expr'
	p[0] = ~ p[2]

# XOR
def p_xor( p ) :
	'expr : expr XOR expr'
	p[0] = p[1] ^ p[3]

# R Shift
def p_rshift( p ) :
	'expr : expr RSHIFT expr'
	p[0] = p[1] >> p[3]

# L Shift
def p_lshift( p ) :
	'expr : expr LSHIFT expr'
	p[0] = p[1] << p[3]

# Logical Operators

# OR
def p_lor( p ) :
	'expr : expr LOR expr'
	p[0] = p[1] or p[3]

# AND
def p_land( p ) :
	'expr : expr LAND expr'
	p[0] = p[1] and p[3]

# NOT
def p_lnot( p ) :
	'expr : LNOT expr'
	p[0] = not p[2]

########################

def p_expr2NUM( p ) :
    'expr : NUMBER'
    p[0] = p[1]

def p_parens( p ) :
    'expr : LPAREN expr RPAREN'
    p[0] = p[2]

def p_error( p ):
    print("Syntax error in input!")

parser = yacc.yacc()

fname = "fname.c"
with open(fname) as f :
    val = f.read()
res = parser.parse(val)

print(res)