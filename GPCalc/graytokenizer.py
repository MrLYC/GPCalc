# coding: UTF-8
# Name:Gray表达式的Tokenizer
# Author: LYC
# Created: 2014-03-28

from collections import deque
from tokenize import generate_tokens
import token
from StringIO import StringIO
from re import compile
from expelement import ElementTypeEnum, Element

def pretokens(exp):
    return (tk[1] for tk in generate_tokens(StringIO(exp).readline))

class GrayStateException(Exception):
    def __init__(self, msg = "tokens state error because of error expression."):
        super(GrayStateException, self).__init__(msg)

class GrayStateInitException(Exception):
    def __init__(self, msg = "tokens init error because of error expression."):
        super(GrayStateInitException, self).__init__(msg)

class GrayStateEndException(Exception):
    def __init__(self, msg = "tokens finished error because of error expression."):
        super(GrayStateEndException, self).__init__(msg)

class GrayToken(object):
    def __init__(self, exp):

        self.context = deque(pretokens(exp))
        self.tokens = []
        self.state = self.init_state
        self.done = None

    def _try_append(self, tokentype, tk):
        val = tokentype(tk)
        if val != None:
            self.tokens.append(Element(val, tokentype))
            return True
        return False

    def init_state(self, tk):
        if self._try_append(ElementTypeEnum.UOP, tk):
            pass

        elif self._try_append(ElementTypeEnum.LBK, tk):
            pass

        elif self._try_append(ElementTypeEnum.NUM, tk):
            self.state = self.next_state

        elif self._try_append(ElementTypeEnum.VAR, tk):
            self.state = self.next_state

        else:
            raise GrayStateException()

    def next_state(self, tk):
        if self._try_append(ElementTypeEnum.CMM, tk):
            self.state = self.init_state

        elif self._try_append(ElementTypeEnum.RBK, tk):
            pass

        elif self._try_append(ElementTypeEnum.BOP, tk):
            self.state = self.init_state

        elif self._try_append(ElementTypeEnum.NON, tk):
            self.end_state()

        else:
            raise GrayStateException()

    def end_state(self):
        self.tokens = tuple(self.tokens)
        self.done = True

    def __call__(self):
        if self.done == None:
            self.done = False
            while self.context:
                tk = self.context.popleft()
                self.state(tk)
                if self.done:break
            else:
                raise GrayStateEndException()
        return self.tokens