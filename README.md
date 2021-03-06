# 因子挖掘：反转&小市值。

- **动量因子**多以行为金融学解释（过度反应、反应不足）。根据EMH，在相对弱有效的市场下因子效果会更好，如中国市场。经实证，动量因子在中国市场具有相对强的识股能力

- **市值因子**则一直是金融市场非常强劲的因子，尤其是在中国市场的效果特别好

此项目旨在研究这两种中国A股市场表现相对较好的因子，并尝试通过这两种因子的组合挖掘新的因子，并评估其效果。

> 反转与动量因子最早在1993年由Jegadeesh和Titman在[《Returns to Buying Winners and Selling Losers: Implication for Stock Market Efficiency》, *The Journal of Finance, 1993*](http://www.business.unr.edu/faculty/liuc/files/BADM742/Jegadeesh_Titman_1993.pdf)里面提出，本研究中所称的“反转”、“动量”因子计算方式与此论文大致相同。
> 
> 其它细节之处之不同则参考了这篇研究中国A股市场异象的论文：[《Anomalies in Chinese A-Share》, 2017](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2955144)。
> 
> 其论文中关于A股市场反转的实证研究我也复现验证了一次，在收益和统计显著性上的趋势都与论文吻合，这部分的代码见[Research.py](https://github.com/KasperLXK/Contrarian/blob/master/Contrarian%20Codes/Research.py)。

# 1. 研究及回测方式

## 1.1 研究方式

- **数据来源**：[CSMAR](http://www.gtarsc.com/Home)，所需数据及数据说明保存在[Contrarian Data](https://github.com/KasperLXK/Contrarian/tree/master/Contrarian%20Data)。
- **数据分析工具**：主要采用Python进行数据分析，部分步骤采用R，大部分研究代码可在[Contrarian Codes](https://github.com/KasperLXK/Contrarian/tree/master/Contrarian%20Codes)中找到。其中各代码文件的主要内容：
    - [Contrarian.py](https://github.com/KasperLXK/Contrarian/blob/master/Contrarian%20Codes/Contrarian.py)：数据处理与策略算法
    - [Backtest.py](https://github.com/KasperLXK/Contrarian/blob/master/Contrarian%20Codes/Backtest.py)：策略回测
    - [Analysis.py](https://github.com/KasperLXK/Contrarian/blob/master/Contrarian%20Codes/Analysis.py)：回测绩效分析

## 1.2 回测方式

如无特殊说明，本研究中所有回测皆遵循以下规则：

- 排序期：对因子暴露进行观察和排序的时间
- 持有期：决定出投资组合后的持有时间
- 回测样本期：2009年至2018年共十年
- 股票数量：如无特殊说明，默认选取各因子排序期的前100支股票的交集作为持有期投资组合
- 交易成本：默认计入，按照<u>双向千分之二</u>收取交易费用
- 基准指标：选择沪深300作为基准
- 剔除ST股票

# 2. 因子选择

## 2.1 反转因子

我的研究和回测结果显示：

- 反转因子（做多输家组合、做空赢家组合）比动量因子（做多赢家组合、做空输家组合）表现好
- 其中，输家的反转效应相对赢家的更显著

以排序持有期皆为一个月的：
- 单边做多输家组合的纯反转策略
- 单边做多赢家组合的纯动量策略

为例，两种策略的十年回测结果主要指标分别为：

策略|复合年化收益率|夏普比率|最大回撤
:--:|:--:|:--:|:--:
反转策略|10.025%|2.048|-60.901%
动量策略|-16.729%|-1.511|-91.174%

可以看出，输家组合和赢家组合都呈现反转效应，其中反转策略表现更佳。

> 考虑到中国股票市场还没有完善的做空机制，我们不研究做空。

故本研究专注于：

- 单边做多输家策略

## 2.2 小市值因子

考虑到中国市场市值的波动率也较国际市场更大，风格轮换更快，根据回测，故采用相对较小的观察期窗口（以若干月为单位），以期更好地捕捉小市值因子。

同样以排序持有期皆为一个月的：

- 单边做多小市值组合的纯小市值策略
- 单边做多大市值组合的纯大市值策略

为例，两种策略的十年回测结果的主要指标分别为：

策略|复合年化收益率|夏普比率|最大回撤
:--:|:--:|:--:|:--:
小市值策略|40.237%|4.993|-42.757%
大市值策略|-0.452%|-0.531|-54.413%

在小市值与大市值的选择上，由于小市值因子大幅超越了大市值因子，而二者收益率的相关性亦十分高。

故本研究专注于：

- 小市值因子

# 3. 新因子初步研究

## 3.1 取交集方式的研究

想要同时获取两种因子的选股能力，我们初步有三种取交集的方式：

- 简单交集
- 收益优先
- 市值优先

他们分别用以下介绍的不同方法取两种因子的交集。

### 3.1.1 简单交集

- 取排序期收益最差的N支股票作为输家组合
- 取排序期市值最小的N支股票作为小市值组合
- 取输家组合和小市值组合的交集作为持有期的投资组合

即：取排序期收益最差的N支股票和市值最小的N支股票的交集。

### 3.1.2 收益优先

- 取排序期收益最差的2N支股票作为输家组合
- 取输家组合中市值最小的N支股票作为持有期的投资组合

即：取排序期收益最差的2N支股票中市值最小的N支股票，为“输家中的小市值”。

> 这里放大N的参数2是可变的，暂时取2，下同。

### 3.1.3 市值优先

- 取排序期市值最小的2N支股票作为小市值组合
- 取小市值组合中收益最差的N支股票作为持有期的投资组合

即：取排序期市值最小的2N支股票中收益最差的N支股票，为“小市值中的输家”。

### 3.1.4 三种取交集方式的比较

分别计算股票数量为10至200支的时候，3-1反转+小市值策略的回测表现，并求指标平均值作为最终结果。

分别计算采用上述三种取交集方式的最终结果，如下👇。

![三种取交集方式的研究.png](https://i.loli.net/2019/03/30/5c9f851970a44.png)

可以从图中看出，市值优先是平均表现最好的取交集方式，具有：

- 最高的复合年化收益率
- 最高的夏普比率
- 最低的最大回撤

> 不过值得注意的是，即使名义上的N值（投资组合中的股票数量）相同，简单交集方式下的实际投资组合股票数量却不等于（一般远小于）N。因为取交集之后数量变少。而剔除ST股票后也会使所有的取交集方式的实际投资组合股票数量都不一定等于N。

故这一研究下虽然同为股票数量10至200支，但简单交集的实际投资组合数量是远小于另外两种取交集方式的，而股票数量小的时候更容易具有高收益率、高夏普。

综上，接下来的研究主要聚焦于市值优先取交集方式，如无特殊说明皆采用此方式。

## 3.2 取两个因子的交集，表现是否确实超过原来的因子？

以排序持有期3-1为例，比较以下三种策略：

- 纯反转策略，取排序期收益最差的N支股票作为持有期投资组合
- 纯小市值策略，取排序期市值最小的N支股票作为持有期投资组合
- 反转+小市值策略，按照市值优先方式取排序期交集作为持有期投资组合

分别对三种策略取股票数量为10至500支时的回测表现。

![三种策略的收益率对比.png](https://i.loli.net/2019/03/30/5c9f8e01d5eed.png)

![三种策略的夏普比率对比.png](https://i.loli.net/2019/03/30/5c9f8e0212281.png)

![三种策略的最大回撤对比.png](https://i.loli.net/2019/03/30/5c9f8e0213c90.png)

可以看出：

- 大致呈现“股票数量越多，回测表现越差”的规律
- 在三个指标上都呈现出，反转+小市值策略 > 小市值策略 >> 反转策略
- 在股票数量超过30支后，反转+小市值策略的复合年化收益率、夏普比率开始显著超过小市值策略
- 最大回撤上，反转+小市值策略更是一直比小市值策略低近10个百分点
- 综合来看，反转+小市值策略是三个里面最好的策略

单独比较小市值策略与反转+小市值策略👇。

![三种策略的对比.png](https://i.loli.net/2019/03/30/5c9f8fdf56929.png)

以反转+小市值策略来说，有两种选取股票的方式比较吸引人：

- 激进：股票数量为30支左右时，高收益、高回撤
- 保守：股票数量为100支左右时，相对高收益、相对低回撤

至少在排序持有期为3-1的时候，取两种因子的交集确实获得了比原始因子更好的表现。

故研究聚焦于反转+小市值策略（市值优先取交集法），如无特殊说明皆采用此策略。

# 4. 排序持有期研究

## 4.1 持有期研究

对上述总结的策略：

- 反转+小市值
- 市值优先取交集
- 股票数量N=100

分别尝试一到十二个月的不同排序持有期排列组合，结果如下👇。

![排序持有期研究.png](https://i.loli.net/2019/03/31/5ca028319859c.png)

可以看出：

- 复合年化收益率来看，持有期为一个月的表现大幅领先其它持有期
- 一般来说持有期越长，复合年化收益率越低
- 值得注意的是，持有期为六个月左右的复合年化收益率表现相对突出
- 夏普比率来看，一般有两个波峰：持有期一个月左右，和持有期六个月左右
- 最大回撤来看，一般也有两个波谷：持有期一个月左右，和持有期六个月左右

故接下来的研究聚焦于：

- 持有期一个月
- 持有期六个月

的策略。其中持有期一个月的综合表现尤其突出，以下如无特殊说明皆采用持有期为一个月的策略。

## 4.2 排序期研究

倘若固定持有期为一个月，分别尝试十二个月的排序期，得到下图👇。

![排序期研究.png](https://i.loli.net/2019/03/31/5ca02696c9bff.png)

可以看出：

- 复合年化收益率来看，排序期超过三个月后开始上升，在六个月的时候达到顶峰，在超过九个月之后开始明显下降
- 夏普比率来看也是，三至九个月似乎是表现最佳的区间
- 最大回撤则较为平均

故接下来的研究聚焦于排序期为六个月的策略，如无特殊说明皆采用排序期为六个月的策略。

# 5. 止损

经过研究发现，持有期投资组合在排序期的股票交易量平均值与持有期投资组合的收益率具有一定的相关性，可以对收益率进行一定程度的预测。本研究用于止损。

如图为分别对股票数量在10至200支的反转+小市值、市值优先取交集策略计算其当前投资组合在排序期的股票交易量平均值与持有期（即下一期）投资组合的收益率的相关性和P值👇。

![交易量与下一期收益的相关系数.png](https://i.loli.net/2019/03/31/5ca081a8265d8.png)

可以看出：

- 在股票数量超过30支之后，相关系数基本超过0.15，最高超过0.2
- 与之相应的P值也在股票数量超过30支后稳定在0.05左右

故我们尝试用投资组合在排序期的平均股票交易量对已有的策略进行止损。

我们设定如下止损规则：

- 计算投资组合在排序期的平均股票交易量的过去三期（月）移动平均值，作为交易量三月移动均值
- 假如当期交易量小于指定参数倍的交易量三月移动均值，则下一期空仓，收益记为零
- 经过调参优化，指定参数在股票数量为30支的时候取0.82

这样的止损是否有效呢？我们观察股票数量在10至20支下原始策略与止损策略的平均回撤，对比如下图👇。

![止损后平均回撤对比.png](https://i.loli.net/2019/03/31/5ca0805a2b5c1.png)

可以看出：

- 止损策略的平均回撤一般比原始策略要低
- 尤其是股票数量小于50支的时候

---

这一新因子相比于传统的反转因子、小市值因子表现如何呢？我们着重和小市值因子作比较。

对三个策略：

- 小市值
- 小市值+反转
- 小市值+反转+止损

分别取5至150支股票，并取表现最佳的一次回测做对比，结果如下👇。

![策略最佳表现对比.png](https://i.loli.net/2019/04/01/5ca0e55820cd1.png)

可以看出：

- 新因子比原本的小市值因子收益率更高
- 新因子比原本的小市值因子最大回撤更低
- 新因子比原本的小市值因子夏普比率更高
- 经过止损后的新因子在保持收益率没有大幅下降的前提下，可以进一步降低最大回撤，但效果不明显

我们单独对风险指标进行分析👇：

![策略最佳表现风险对比.png](https://i.loli.net/2019/04/01/5ca0e55820994.png)

可以看出：

- 新因子比原本的小市值因子平均回撤更低
- 但小市值因子波动率更低
- 经过止损后的新因子比原本的小市值因子平均回撤又更低一些

为避免取最佳回测表现，只有一个统计样本不具有代表性，我们对三个策略一次选取30个回测样本（即5至500支股票），并对上述指标取平均值，结果如下👇：

![策略平均表现对比.png](https://i.loli.net/2019/04/01/5ca0e558207b6.png)

![策略平均表现风险对比.png](https://i.loli.net/2019/04/01/5ca0e558207f2.png)

可以看出，取30个回测样本的平均值，上述结论依然成立。

于是我们可以通过调整：

- 股票数量
- 止损等参数

分别调节策略的风格：

- 收益：激进或者保守
- 风险：止损或不限制

总结各种风格的上述指标，结果如下图👇，依然，为了防止个别回测不具有代表性，每个风格的策略都取了三个回测样本取平均。

![不同风格的策略表现对比.png](https://i.loli.net/2019/04/01/5ca0e55810699.png)

综上，可以看出综合表现最好的应该是“激进的反转+小市值+止损”策略。经过统计与调参，我们可以生成截至目前最好的策略：

- 反转+小市值
- 市值优先取交集方式，参数为2
- 股票数量为N=10
- 剔除ST股票
- 排序期为6个月
- 持有期为1个月
- 采用投资组合在排序期的平均交易量进行止损，参数为0.77

这一策略从2009至2018共十年的回测表现为：

- 年化复合增长率：128.39%
- 夏普比率：7.497
- 波动率：2.811
- 最大回撤：-39.638%
- 平均回撤：-7.549%
- 平均回撤时间：91.476天