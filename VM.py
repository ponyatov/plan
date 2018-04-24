import sys

try: SRC = sys.argv[1]
except IndexError: SRC = 'init.4th'

class Object:
    def __init__(self,V):
        self.tag = self.__class__.__name__.lower()
        self.val = V
        self.nest = []
        self.attr = {}
    def __repr__(self): return self.dump()
    def dump(self,depth=0):
        S = self.pad(depth) + self.head()
        return S
    def head(self,prefix=''):
        return '%s<%s:%s>'%(prefix,self.tag,self.val)
    def pad(self,N):
        return '\n'+'\t'*N
    def pop(self):
        return self.nest.pop()
    def __getitem__(self,K):
        try: return self.attr[K]
        except KeyError: return self.attr[K.val]
    def __setitem__(self,K,V):
        self.attr[K] = V ; return self
    
class Token(Object): pass

class Stack(Object):
    def __lshift__(self,o): self.nest.append(o); return self
    
class Voc(Object):
    def __lshift__(self,o): self.attr[o.val] = o ; return self
    
class Fn(Object):
    def __init__(self,F):
        Object.__init__(self, F.__name__)
        self.fn = F

D = Stack('DATA')
W = Voc('FORTH')

def q(): print D
W['?'] = Fn(q)

def qq(): print W ; q() ; BYE()
W['??'] = Fn(qq)

def BYE(): sys.exit(0)

import ply.lex as lex

tokens = ['WORD']

t_ignore = ' \t\r'

t_ignore_COMMENT = '[\\\#].*'

def t_newline(t):
    r'\n'
    t.lexer.lineno += 1
    
def t_WORD(t):
    r'[a-zA-Z0-9_\?]+'
    t.value = Token(t.value) ; return t

def t_error(t): raise SyntaxError(t)

def t_eof(t): BYE()

lexer = []

def WORD():
    D << lexer[-1].token().value
    
def FIND():
    WN = D.pop()
    try: D << W[WN]
    except KeyError: raise SyntaxError(WN)

def INTERPRET(SRC):
    global lexer ; lexer += [lex.lex()]
    lexer[-1].input(SRC)
    while True:
        WORD()
        print D
        FIND()
        print D
INTERPRET(open(SRC).read())
