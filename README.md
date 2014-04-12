#GPCalc by 刘奕聪
## 题目
我们需要完成一个可以自动解析计算表达式，并进行运算返回结果的一个科学计算器程序。
详细：[完整题目][1]

## 作品说明
### 数据类型
#### 实数
基本数值类型，如：`123`，`123.45`，`.123`，`123.`。
可以使用8进制和16进制表示，但仅支持表示整数：

- 8进制：`0o125`。
- 16进制：`0xAC`，`0Xb1`。

#### 复数
使用**Python**表示方式，其中虚部数值后必须加上复数单位量`j`，如：`1+2j`，`0.5j`，`0.5-0.5j`。  
当实数和复数混合运算时会隐式转换成复数。
复数单位量`j`之前必须有系数。

#### 数组
复合类型，多个数据的集合，表示方式：括号包围，逗号分割元素，如：`[1,2]`，`(3.5,1+0j)`,`(1,(2,3),(4,(5,6)))`。  
嵌套型数组会被系统降维成一维数组。

### 运算符
#### 单目运算符
单目运算符包括以下三种：

 1. +：表示正数。
 2. -：表示负数。
 3. 引用符：包括变量引用符`$`和自定义函数引用符`#`。
 4. 函数：由英文开始且仅包含英文数字和下划线的符号。
 
#### 双目运算符

 1. +：加。
 2. -：减。
 3. *：乘。
 4. /：除。
 5. mod：模除，同`%`。
 6. \^：乘幂，同`**`。
 7. ,：数组化操作。

### 优先级说明
以下运算符优先级从高到低排序：

 1. 单目运算符：`+`，`-`，引用符与函数。
 2. 乘幂和模除：`mod`与`^`。
 3. 乘法和除法：`*`与`/`。
 4. 假发和减法：`+`与`-`。
 5. 数组化操作符：逗号`,`。
 6. 括号：`()`同`[]`。

### 特殊说明

 - 数组作为一种特殊的数据类型，仅有少数个可用的运算符，仅包括数组的拼接`+`和函数。
 - `$`变量引用符仅能作用于变量。
 - `#`函数引用符仅能作用于自定义函数。
 
### 变量
变量是数据暂存的存储单元，在一定程度上简化表达式和免去重复计算而提高效率。  
变量声明格式如下：

> $变量名:表达式

其中，`$`为变量引用符，变量名仅能使用若干个仅包含英文数字和下划线的符号，`:`为声明符，其后跟表达式，系统会计算表达式的值并将结果赋值给变量。  
所有未初始化的变量的值都为`None`，不能参与计算。  
初始化后的变量能够作为表达式的一份子参与计算，如：`$x + $$ans`。

### 自定义函数
系统允许用户定义临时的lambda表达式，其使用方式与内置函数一样。  
对于一些被大量重复计算的表达式推荐定义成函数，第一个好处是避免重复输入表达式，第二个是自定义函数比重复输入表达式的方式的性能要高。  
声明格式如同变量：

> \#函数名:表达式

和变量类似，`#`为函数引用符，命名规则同变量，和变量相同的命名不会造成冲突。`:`为声明符，其后跟表达式，函数中使用位置变量来代替参数，如形为：`#f (5,6,7,8)`的函数调用，则在自定义函数`#f`中可以使用`$1`，`$2`，`$3`，`$4`来分别表示参数`5`，`6`，`7`，`8`。特殊的，`$0`表示整个参数数组。

#### 内置常量

 - $$ans：上次表达式的结果。
 - $$0：空数组。
 - $$pi：圆周率。
 - $$e：自然底数。
 - $$c：真空中光速。
 - $$h：普朗克常数。
 - $$g：引力常数。
 - $$f：法拉第常数。
 - $$inf：无穷大。

### 方程
系统提供了解一元一次方程的功能。  
方程格式如下：

> 表达式1 = 表达式2

其中，用`$$`表示未知数，方程的结果是`$$`的值。  
注意，`$$`不能用于函数，不能作为数组元素。   
正确格式如：`fact(10) * sin($$pi * 2) * $$ = sum([1, 2, 3, 4, 5]) - 1`。
未知数`$$`不能在表达式中作为分母，分母中含有未知数的方程是分式方程，不属于一元一次方程。

## 扩展函数
### 三角函数
三角函数有三组：  
支持角度表示：`sin`，`cos`，`tan`，`arcsin`，`arccos`，`arctan`。  
支持弧度表示：`rsin`，`rcos`，`rtan`，`rarcsin`，`rarccos`，`rarctan`。  
支持复数弧度表示：`zsin`，`zcos`，`ztan`，`zarcsin`，`zarccos`，`zarctan`。  

### 数值相关
#### floor
对参数向下取整。

#### real
取数值的实部。

#### imag
取数值的虚部。

### 数组相关
#### len
计算数组的长度。

#### head
取数组的头部（参见广义表的head操作）。

#### tail
取数组的尾部（参见广义表的tail操作）。

#### left
取数组的左半部分。

#### right
取数组的右半部分，当元素个数是奇数时包括中间元素。

### 其他功能
#### tuple
返回参数形式表示的数组，提供了构造元素个数为1的数组的方法。

#### val
输出参数的各种进制的表示（进制转换）。

## 在Google Talk上使用

1. 添加帐号：lycbot@appspot.com。
2. 请向该帐号发送你的表达式，每个表达式占一行。
3. 因为该聊天机器人托管在Google App Engine上，因此一次执行完后会退出，所定义的函数和变量会被删除。

注：因为GAE的Python版本较低和限制较多，其上面搭载的GPClac是修改过的，会有一些差别。
 
  [1]: https://git.oschina.net/Mr_LYC/GPCalc/blob/master/%E9%A2%98%E7%9B%AE.md#tree-content-holder