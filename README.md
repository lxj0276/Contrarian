# 因子挖掘：反转&小市值。

- 关于**动量因子与反转因子**的经济学原理多以行为金融学解释（过度反应、反应不足）。那么根据EMH，则在相对弱有效的市场下这些因子的效果会更好。经实证动量因子，尤其是其中的高频**反转因子**，在中国市场具有相对强识股能力。

- 而**市值因子**则一直是金融市场非常重要的因子，尤其是在中国市场，**小市值因子**的效果特别好。

此项目旨在研究这两种中国A股市场表现相对较好的因子，并尝试通过这两种因子的组合挖掘新的因子，并评估其效果。

> 反转与动量因子最早在1993年由Jegadeesh和Titman在[《Returns to Buying Winners and Selling Losers: Implication for Stock Market Efficiency》, *The Journal of Finance, 1993*](http://www.business.unr.edu/faculty/liuc/files/BADM742/Jegadeesh_Titman_1993.pdf)里面提出，本研究中所称的“反转”、“动量”因子计算方式与此论文大致相同。
> 
> 其它细节之处之不同则参考了这篇研究中国A股市场异象的论文：[《Anomalies in Chinese A-Share》, 2017](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2955144)。其论文中关于股市场反转的实证研究我也复现验证了一次，在收益、规律、统计显著性（t统计量）上都与论文吻合，这部分的代码见[Research.py](https://github.com/KasperLXK/Contrarian/blob/master/Contrarian%20Codes/Research.py)。

# 1. 因子选择

## 1.1 反转因子

在发达金融市场上，中长期的动量因子（如美股3个月动量）表现较佳。但据我的研究，尽管中长期的动量因子在中国市场也具有一定收益能力，但较为**短期、反转**的因子表现更佳。回测结果也显示在A股市场反转因子较动量因子表现好得多。

故主要研究**短中期的反转因子**。

# 1.2 小市值因子

小市值因子在全世界的金融市场都有不错的表现，在中国市场更是有十分强劲的收益能力（尽管2017年后有所减弱）.同时中国市场市值的波动率也较国际市场更大，风格轮换更快，根据回测，较小的观察期窗口更能够捕捉到小市值因子。

故主要研究**短中期的小市值因子**。

# 2. 回测

## 2.1 回测方式

- **Rank&Hold**（排序&持有）：采用“对过去J期因子暴露总和排序，以此决定下一期的投资组合，并持有K期”的方式捕捉因子风格
> 以下简称为 “因子名 J-K” ，例如 “反转 6-3” 表示每一次交易观察过去6个月收益表现最差的输家组合作为下一期的投资组合，并持有该组合3个月。
- **满仓运行**：每次持仓都（尽可能）用全部资金；
- **增量调仓**：每次调仓时，上一期投资组合与下一期投资组合重合的部分只交易其差额；
- **交易成本**：按照<u>双向千分之二</u>收取交易费用；
- **换仓**：不加减仓，净值变化的计算按累计复利，持有K期期间不调仓，直到K期结束后才进行下一次交易；

## 2.2 回测实现

- **数据来源**：[CSMAR](http://www.gtarsc.com/Home)，所需数据及数据说明保存在[Contrarian Data](https://github.com/KasperLXK/Contrarian/tree/master/Contrarian%20Data)。
- **数据分析工具**：主要采用Python进行数据分析，部分步骤采用R，大部分研究代码可在[Contrarian Codes](https://github.com/KasperLXK/Contrarian/tree/master/Contrarian%20Codes)中找到。

# 3. 反转因子研究

## 3.1 反转频率研究

