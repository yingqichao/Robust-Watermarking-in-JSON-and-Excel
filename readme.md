Readme.md

version 1.1：

不需要知道所有的键值，用自定义的算法通过键值的string计算出每个键值的专属伪随机序列种子（基本不会重复）

【信息嵌入】
第一环节：水印信息分块
-----例如将“zhenxingqian”按照每个ASCLL码为一个块，分成12块

第二环节：LT编码，每个输出块的度的确定与对应关系的随机生成
-----例如，如果要让输出块2是服从均匀分布的2个随机水印块的异或，那么度=2。这里的伪随机种子，我们用键值本身计算得到（而且很长，确保足够
随机性，例如：logDataeventInfodetectStart被映射为15540831722377），通过这个种子，嵌入端与提取端会得到同样的度和对应关系（伪随机序
列第一个值作为度函数的CDF，剩下的值为选中的水印块的序号）。假设从12个块中选中的2个输入块为[4,6]，那么这里我们就得到了完整的嵌入参数：
（2，[4，6]）。


第三环节：过滤无效JSON键值，对有效键值的value做喷泉码嵌入数据
-----这里我们对每个value，最多修改5个bit，使用的方法是LSB replacement。5bit是因为2^6=64，能够表示所有大小写和数字。喷泉码中，每个
输出块都是若干（d）个水印块的异或。我们对于每个有效的键值，都会进行嵌入，也就是说，JSON的键值就是“喷泉”，而里面有效简直数量就是“喷泉”
里面的“水滴”数量。

【信息提取】
第一环节：LT解码，根据每个键值得到每个“水滴”的度与对应关系
------上面说到了，伪随机序列的种子在这个版本中，由于是从键值计算来的，所以可以直接被接收者获得。接收者可以用这个种子生成伪随机序列，
得到信息嵌入者使用的度和对应关系

第二环节：利用置信传播算法，收集“水滴”，直到发现所有的信息都可以被解析

第三环节：信息提取：接收者将每个接收到的键值的value按照LSB取出异或后的秘密信息，根据置信传播算法，得到每个水印块应该如何被这些块异或可
以被解析，从而获取到原始水印信息

【嵌入规则】
每个key嵌入5bit，表示一个A-Z 或 a-z 或0-9
对于string：只修改字母和数字，其他的都不修改（比如‘、’，‘/’等）
对于double和int：去掉小数点并记录它的位置，记录并去掉数字的第一位（不做嵌入信息，防止变成0导致长度变化），将剩下部分转为string，然后
嵌入规则同上，最后再把小数点和第一位补回去

【注意事项】
1.水印目前只支持小写字母
2.接收者必须知道水印的长度（也即水印信息分块数量）


version 1.0（original）:

假定知道所有的键值（JSON中的key），用伪随机序列的seed确定哪些key（字段）用于嵌入信息，如果该字段长度不够，就跳过，继续寻找下一个

//用户需要一个用于鲁棒弧度分布的密钥Key1（seed），这个seed只会使用一次，作为RSD的起始

发送的时候，由于已经知道了所有的key值，所以对于接收端的每一个key，接收者都会知道这个key有否被用来嵌入信息，如果有，对应的序号也会知道
这是一个强前提，否则对应关系需要一并嵌入到文本中去

每个伪随机种子会用三次：第一次为度函数确定 第二次为均值随机 第三次为选择嵌入位置

