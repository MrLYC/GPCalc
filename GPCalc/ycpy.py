# coding:utf-8
# Name: ycpy
# Author: LYC
# Created: 2014-03-19

import sys
import StringIO

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
        self.__stdin = stdin
        self.__stdout = stdout
        self.__stderr = stderr

        #运行环境
        self.Environment = {}

        self.init()

    def init(self):
        """初始化运行环境"""
        self.Environment = dict(YCPY.DefaultEnvironment)

    def __switch_stream(self):
        """切换stdin,stdout,stderr"""
        self.__stdin, self.__stdout, self.__stderr, sys.stdin,    sys.stdout,    sys.stderr = \
         sys.stdin,   sys.stdout,    sys.stderr,    self.__stdin, self.__stdout, self.__stderr

    def __write_error(self):
        """遇到错误把错误信息写入stderr"""
        info = sys.exc_info()
        sys.stderr.write("\n".join([str(i) for i in info]) + "\n")

    def exec_code(self, code):
        """执行代码段"""
        self.__switch_stream()

        try:
            #使用指定运行环境以隔离对当前运行环境的影响
            exec(code, self.Environment)
        except:
            self.__write_error()
        finally:
            self.__switch_stream()

    def eval_exp(self, exp):
        """执行表达式"""
        self.__switch_stream()

        try:
            #返回表达式的值
            return eval(exp, self.Environment)
        except:
            self.__write_error()
        finally:
            self.__switch_stream()

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

        super(YCPY,self).__init__(self.stdin, self.stdout, self.stderr)

        self.init()

    def init(self):
        """初始化运行环境"""
        super(YCPY, self).init()
        self.Environment.update(self.api_dct)

    def __set_stdin(self, input_list):
        """将输入列表写进stdin"""
        input_txt = "\n".join(input_list) + "\n"
        self.stdin.write(input_txt)
        self.stdin.seek(0)

    def __read_stream(self, stream):
        buf = stream.getvalue()
        stream.buf = ""
        return buf

    def exec_code(self, code, *input_list):
        """执行指定的代码,并返回(stdout,stderr),input_list是stdin,一个元素代表一行"""
        self.__set_stdin(input_list)

        super(YCPY,self).exec_code(code)

        return self.__read_stream(self.stdout), self.__read_stream(self.stderr)

    def eval_exp(self, exp, *input_list):
        """执行指定的代码,并返回(结果值,stdout,stderr),input_list是stdin,一个元素代表一行"""
        self.__set_stdin(input_list)

        result = super(YCPY,self).eval_exp(exp)

        return result, self.__read_stream(self.stdout), self.__read_stream(self.stderr)

def main():
    pass

if __name__ == '__main__':
    main()
