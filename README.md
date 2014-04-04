#GPCalc by 刘奕聪
## 题目
我们需要完成一个可以自动解析计算表达式，并进行运算返回结果的一个科学计算器程序。
详细：[完整题目][1]

## 作品说明
### 数据类型
#### 实数
基本数值类型，如：`123`，`123.45`，`.123`，`123.`。

#### 复数
使用**Python**表示方式，其中虚部必须数值后必须加上复数单位量`j`，如：`1+2j`，`0.5j`，`0.5-0.5j`。
当实数和复数混合运算时会饮食转换成复数。

#### 数组
复合类型，多个数据的集合，表示方式：括号包围，逗号分割元素，如：`[1,2]`，`(3.5,1+0j)`,`(1,(2,3),(4,(5,6)))`。

### 运算符
#### 单目运算符
单目运算符包括以下三种：

 1. +：表示正数。
 2. -：表示负数。
 3. $：变量引用符。
 4. 函数：由英文开始且仅包含英文数字和下划线的符号。
 
#### 双目运算符

 1. +：加。
 2. -：减。
 3. *：乘。
 4. /：除。
 5. mod：模除，同`%`。
 6. \^：乘幂，同`**`。

### 优先级说明
以下运算符优先级从高到低排序：

 1. 括号：`()`同`[]`。
 2. 单目运算符：`+`，`-`，`$`与函数。
 3. 乘幂和模除：`mod`与`^`。
 4. 乘法和除法：`*`与`/`。
 5. 假发和减法：`+`与`-`。
 6. 数组化操作符：逗号`,`。

### 特殊说明

 - 数组作为一种特殊的数据类型，仅有少数个可用的运算符，仅包括数组的拼接`+`和函数。
 - `$`变量引用符仅能作用于变量。
 
### 变量
变量是数据暂存的存储单元，在一定程度上简化表达式和免去重复计算而提高效率。
变量声明格式如下：

> $变量名:表达式

其中，`$`为变量引用符，变量名仅能使用若干个仅包含英文数字和下划线的符号，`:`为声明符，其后跟表达式，系统会计算表达式的值并将结果赋值给变量。
所有未初始化的变量的值都为`None`，不能参与计算。
初始化后的变量能够作为表达式的一份子参与计算，如：`$x + $ans`。

#### 内置变量

 - ans：上次表达式的结果。
 - pi：圆周率。
 - e：常量e。

### 方程
系统提供了解一元一次方程的功能。
方程格式如下：

> 表达式1 = 表达式2

其中，用`$$`表示未知数，方程的结果是`$$`的值。
注意，`$$`不能用于函数，不能作为数组元素。
正确格式如：`fact(10) * sin($pi * 2) / $$ = sum([1, 2, 3, 4, 5]) - 1`。


 
  [1]: https://git.oschina.net/Mr_LYC/GPCalc/blob/master/%E9%A2%98%E7%9B%AE.md#tree-content-holder