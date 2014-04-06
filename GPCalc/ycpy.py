# coding:utf-8
# Name: ycpy
# Author: LYC
# Created: 2014-03-19

import sys
import StringIO
import random

class YCTools(object):
    """提供API以及安全机制"""
    @classmethod
    def raw_input(cls, msg):
        """替换默认raw_input以应用stdin"""
        #sys.stdout.write(msg)
        txt = sys.stdin.readline()
        return txt[:-1]

    @classmethod
    def input(cls, msg):
        """替换默认input以应用stdin"""
        r = cls.raw_input(msg)
        return eval(r)

    @classmethod
    def buildins(cls):
        """替换__builtins__,防止注入"""
        return None

class YCPYBase(object):
    """提供一个基本的Python运行环境"""
    DefaultEnvironment = {
        "Author": {
            "Name": "LYC",
            "Blog": "http://mrlyc.blogger.com",
            "Version": "0.1.1",
        },
        "raw_input": YCTools.raw_input,
        "input": YCTools.input,
    }

    def __init__(self, stdin = sys.stdin, stdout = sys.stdout, stderr = sys.stderr):
        self._stdin = stdin
        self._stdout = stdout
        self._stderr = stderr

        #运行环境
        self.Environment = {}

        self.init()

    def init(self):
        """初始化运行环境"""
        self.Environment = dict(YCPY.DefaultEnvironment)

    def __write_error(self):
        """遇到错误把错误信息写入stderr"""
        info = sys.exc_info()
        sys.stderr.write("\n".join([str(i) for i in info]) + "\n")

    def exec_code(self, code):
        """执行代码段"""

        try:
            #使用指定运行环境以隔离对当前运行环境的影响
            exec(code, self.Environment)
        except:
            self.__write_error()

    def eval_exp(self, exp):
        """执行表达式"""

        try:
            #返回表达式的值
            return eval(exp, self.Environment)
        except:
            self.__write_error()

class YCPY(YCPYBase):
    """针对易用性做了一些改进"""
    def __init__(self, apis = {}, **kw):
        """apis是个字典,会添加进虚拟运行环境,也可用kw达到相同功能"""
        #默认对以下流做重定向
        self.api_dct = {
            "__builtins__": YCTools.buildins(),
        }

        self.stdin = StringIO.StringIO()
        self.stdout = StringIO.StringIO()
        self.stderr = StringIO.StringIO()
        self.api_dct.update(apis)
        self.api_dct.update(kw)

        self.stream_key = 1#初始值是random不会产生的值

        super(YCPY,self).__init__(self.stdin, self.stdout, self.stderr)

        self.init()

    def init(self):
        """初始化运行环境"""
        super(YCPY, self).init()
        self.Environment.update(self.api_dct)

    def add_api(self, name, val):
        """添加api"""
        self.Environment.update({name: val})

    def __set_stdin(self, input_list):
        """将输入列表写进stdin"""
        input_txt = "\n".join(input_list) + "\n"
        self.stdin.write(input_txt)
        self.stdin.seek(0)

    def __read_stream(self, stream):
        buf = stream.getvalue()
        stream.buf = ""
        return buf

    def __switch_stream(self, old, new):
        """切换stdin,stdout,stderr"""
        if old == self.stream_key:
            self._stdin, self._stdout, self._stderr, sys.stdin,    sys.stdout,    sys.stderr = \
            sys.stdin,   sys.stdout,    sys.stderr,    self._stdin, self._stdout, self._stderr
            self.stream_key = new

    def exec_code(self, code, *input_list):
        """执行指定的代码,并返回(stdout,stderr),input_list是stdin,一个元素代表一行"""
        self.__set_stdin(input_list)

        key = random.random()
        self.__switch_stream(1, key)#加锁
        super(YCPY,self).exec_code(code)
        self.__switch_stream(key, 1)

        return self.__read_stream(self.stdout), self.__read_stream(self.stderr)

    def eval_exp(self, exp, *input_list):
        """执行指定的代码,并返回(结果值,stdout,stderr),input_list是stdin,一个元素代表一行"""
        self.__set_stdin(input_list)

        key = random.random()
        self.__switch_stream(1, key)
        result = super(YCPY,self).eval_exp(exp)
        self.__switch_stream(key, 1)

        return result, self.__read_stream(self.stdout), self.__read_stream(self.stderr)

def main():
    pass

if __name__ == '__main__':
    main()
