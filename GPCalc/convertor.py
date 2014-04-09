# coding: UTF-8
# Name:表达式的Tokenizer
# Author: LYC
# Created: 2014-03-28

import graytokenizer
from expelement import ElementTypeEnum
import operators
import re
from gpcalccfg import Configuration
from collections import deque

class Convertor(object):
    """
    转换器
    """
    @classmethod
    def __replace(cls, tk):
        """替换"""
        if tk.type == ElementTypeEnum.NUM:
            #注入点,可改为Decimal,但内置的Decimal不支持与复数运算,因此使用float
            #2014-04-07 实现了一个可自动转换类型的Decimal的子类实现高精度
            if tk.value.endswith("l"):tk.value = tk.value[:-1]
            tk.value = "%s('%s')" % (Configuration.AutoNumFunc, tk.value)

        elif tk.type != ElementTypeEnum.VAR:
            if tk.type == ElementTypeEnum.LBK:
                tk.value = "("
            elif tk.type == ElementTypeEnum.RBK:
                tk.value = ")"
            #单目运算符需要明确指定,以区分+-号
            if tk.type == ElementTypeEnum.UOP:tk.value = operators.operator_factory(tk.value, True)
            else:tk.value = operators.operator_factory(tk.value)

        return tk


    @classmethod
    def __opstack_pop(cls, op_stack, tk):
        """从运算符栈弹出若干合适的运算符"""
        while op_stack:
            os_tk = op_stack[-1]
            #若栈顶优先级小于当前标识符或遇到左括号,右括号的优先级是最小的
            if os_tk.value < tk.value or os_tk.type == ElementTypeEnum.LBK:break
            yield op_stack.pop()
        raise StopIteration()
#-------------------------------------------------------------------------------

    @classmethod
    def format_usrname(cls, exp):
        exp = exp.replace(Configuration.VarPrefix, Configuration.VarRealPrefix)#处理变量
        exp = exp.replace(Configuration.FuncPrefix, Configuration.FuncRealPrefix)#处理函数
        return exp

    @classmethod
    def preprocessing(cls, exp):
        """预处理"""
        exp = exp.strip()#取出前后空白字符
        exp = exp.lower()#转为小写
        exp = cls.format_usrname(exp)
        return exp

    @classmethod
    def tokenize(cls, exp):
        """获取标记"""
        #获取葡萄表达式的标识符
        gtk = graytokenizer.GrayToken(exp)
        return map(cls.__replace, gtk())#检查并替换标识符

    @classmethod
    def topostfix(cls, tokens):
        """转为后缀表达式"""
        ETE = ElementTypeEnum
        postfix = deque()#保存后缀表达式
        op_stack = deque()#运算符栈

        #最难看的一段代码,因为没有参考资料,纯原创
        #但是工作的挺好,有空再重构
        #2014年04月05日下午14:15已重构
        for tk in tokens:
            #遇到数字和变量直接追加到后缀表达式
            if tk.type in (ETE.NUM, ETE.VAR):
                postfix.append(tk)

            elif tk.type not in (ETE.UOP, ETE.LBK):
                #右括号,逗号和双目运算符需要弹出栈顶一部分合适的运算符
                #追加到后缀表达式中
                postfix.extend(cls.__opstack_pop(op_stack, tk))

                if tk.type == ETE.RBK:op_stack.pop()#把栈顶的左括号弹出

            if tk.type in (ETE.UOP, ETE.LBK, ETE.CMM, ETE.BOP):
                #运算符和左括号直接入运算符栈
                op_stack.append(tk)

        #将栈中剩余的操作符追加到表达式
        else:
            op_stack.reverse()
            postfix.extend(op_stack)

        return postfix

    @classmethod
    def format(cls, exp):
        """格式化表达式"""
        exp = cls.preprocessing(exp)#预处理
        gtk = cls.tokenize(exp)#获取标识符
        postfix = cls.topostfix(gtk)#转为逆波兰表达式
        return postfix

Convertor.format("8-(3+2*6)/5+4")