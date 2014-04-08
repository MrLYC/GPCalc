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
from gpcalccfg import Configuration

def pretokens(exp):
    """利用generate_tokens进行预处理"""
    for tks in generate_tokens(StringIO(exp).readline):
        tk = tks[1]
        if tks[0] == token.NUMBER:
            tk = Configuration.HexRegex.sub(lambda m:str(int(m.group(0), 16)), tk)
            tk = Configuration.OctRegex.sub(lambda m:str(int(m.group(0), 8)), tk)
        yield tk
    raise StopIteration()

class GrayToken(object):
    def __init__(self, exp):

        try:self.context = deque(pretokens(exp))
        except:raise Exception("unrecognizable expression")

        self.tokens = []
        self.state = self.init_state
        self.done = None

    def _try_append(self, tokentype, tk):
        """如果一个标识符符合给定的类型模式,则包装成指定类型的元素"""
        val = tokentype(tk)#返回符合模式的部分
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
            raise Exception("tokens state error because of error expression")

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
            raise Exception("tokens state error because of error expression")

    def end_state(self):
        self.tokens = tuple(self.tokens)
        self.done = True

    def __call__(self):
        if self.done == None:
            self.done = False
            #转移状态直至到达终态
            while self.context:
                tk = self.context.popleft()
                self.state(tk)
                if self.done:break
            else:
                raise Exception("tokens finished error because of error expression")
        return self.tokens

