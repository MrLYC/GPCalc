# coding: UTF-8
# Name:表达式的Tokenizer
# Author: LYC
# Created: 2014-03-28

import graytokenizer
from expelement import ElementTypeEnum
import operators

class Convertor(object):
    """
    转换器
    """
    @staticmethod
    def __replace(tk):
        """替换"""
        if tk.type == ElementTypeEnum.NUM:
            #注入点,可改为Decimal
            if tk.value.find("j") == -1:tk.value = float(tk.value)
            else:tk.value = complex(tk.value) #此项支持复数

        elif tk.type != ElementTypeEnum.VAR:
            if tk.type == ElementTypeEnum.LBK:
                tk.value = "("
            elif tk.type == ElementTypeEnum.RBK:
                tk.value = ")"
            #单目运算符需要明确指定,以区分+-号
            if tk.type == ElementTypeEnum.UOP:tk.value = operators.operator_factory(tk.value, True)
            else:tk.value = operators.operator_factory(tk.value)

        return tk
#-------------------------------------------------------------------------------

    @staticmethod
    def preprocessing(exp):
        """预处理"""
        exp = exp.strip()#取出前后空白字符
        exp = exp.lower()#转为小写
        exp = exp.replace("$", "_")#处理变量
        return exp

    @staticmethod
    def tokenize(exp):
        """获取标记"""
        #获取葡萄表达式的标识符
        gtk = graytokenizer.GrayToken(exp)
        return map(Convertor.__replace, gtk())#检查并替换标识符


    @staticmethod
    def topostfix(tokens):
        """转为后缀表达式"""
        postfix = []#保存后缀表达式
        op_stack = []#运算符栈

        #最难看的一段代码,因为没有参考资料,纯原创
        #但是工作的挺好,有空再重构
        for tk in tokens:
            #遇到数字和变量直接追加到后缀表达式
            if tk.type == ElementTypeEnum.NUM or tk.type == ElementTypeEnum.VAR:postfix.append(tk)
            elif tk.type == ElementTypeEnum.BOP:
                #遇到
                while op_stack:
                    os_tk = op_stack[-1]
                    if os_tk.value >= tk.value :postfix.append(op_stack.pop())
                    else:break
                op_stack.append(tk)
            else:
                if tk.type in (ElementTypeEnum.UOP, ElementTypeEnum.LBK):
                    op_stack.append(tk)
                elif tk.type == ElementTypeEnum.RBK:
                    while op_stack:
                        os_tk = op_stack.pop()
                        if os_tk.type == ElementTypeEnum.LBK:break
                        postfix.append(os_tk)
                    else:raise Exception("error expression.")
                elif tk.type == ElementTypeEnum.CMM:
                    while op_stack:
                        os_tk = op_stack[-1]
                        if os_tk.type == ElementTypeEnum.LBK:break
                        postfix.append(op_stack.pop())
                    else:raise Exception("error expression.")
                    op_stack.append(tk)
        else:postfix += op_stack[::-1]

        return postfix

    @staticmethod
    def format(exp):
        exp = Convertor.preprocessing(exp)
        gtk = Convertor.tokenize(exp)
        postfix = Convertor.topostfix(gtk)
        return postfix
