---
title: 如何在学习机器学习时学习数学？
description: 如何在学习机器学习时学习数学？
---

## 如何在学习机器学习时学习数学？



【方向】

 

2018-08-14 09:22:20

 

浏览1041

 

评论0

- [云栖社区](https://yq.aliyun.com/tags/type_blog-tagid_1/)
-  

- [函数](https://yq.aliyun.com/tags/type_blog-tagid_422/)
-  

- [神经网络](https://yq.aliyun.com/tags/type_blog-tagid_13435/)

*摘要：* 机器学习到底需要怎么样的数学基础？高段位机器学习如何练成？来瞧瞧。

到目前为止，我们都还不完全清楚开始机器学习需要什么样的数学水平，特别是那些没有在学校学习数学或统计学的人。

在这篇文章中，我的目标是提出建立产品或进行机器学习学术研究所需的数学背景。这些建议源于与机器学习工程师、研究人员和教育工作者的对话以及我在机器学习研究和行业角色方面的经验。

首先，我会提出不同的思维模式和策略，以便在传统课堂之外接近真正的数学教育。然后，我将概述不同类型的机器学习工作所需的具体背景，这些学科的范围涉及到高中统计和微积分到概率图形模型（PGM）。

**关于数学焦虑的一个解释**

事实证明，很多人包括工程师都害怕数学。首先，我想谈谈“善于数学”的神话。

事实是，擅长数学的人有很多练习数学的习惯。并不是他们先天就是擅长数学，你可能在看他们做数学时发现他们得心应手。要清楚，要达到这种舒适状态需要时间和精力，但这肯定不是你生就有的。本文的其余部分将帮助你确定所需的数学基础水平，并概述构建它的策略。

**入门**

作为先决条件，我们假设你有[线性代数/矩阵运算以及概率计算的](http://cs229.stanford.edu/section/cs229-linalg.pdf)基本知识点。我还希望你有一些基本的编程能力，这将支持作为在上下文中学习数学的工具。之后，你可以根据你感兴趣的工作类型调整你的主要方向。

如何在校外学习数学？这个问题几乎困扰我们很多人。我相信专心学习数学的最佳方式是在学生的时代。在这种环境之外，你可能不会拥有学术课堂中的氛围、同伴和可用资源。

在校外学习数学，我建议组成学习小组，并学会及时分享各自的资源。相互激励在这里发挥着重要作用，这种“额外”的研究应该受到鼓励和激励，这样在学习上就会很有动力。

**数学和代码**

数学和代码在机器学习工作流程中是高度交织在一起的。代码通常是由数学模型构建，它甚至共享了数学符号。实际上，现代数据科学框架（例如[NumPy](http://www.numpy.org/)）使得将数学运算（例如矩阵/矢量积）转换为可读代码变得直观和有效。

我鼓励你将写代码作为巩固学习的一种方式，数学和代码都是基于理性思考，写代码的过程其实就是理解数学公式的过程。例如，损失函数或优化算法的手动实现可以是真正理解基础概念的好方法。

通过代码学习数学的一个例子：在神经网络中实现ReLU激活的反向传播。作为简要的入门读物，反向传播是一种依赖于微积分链规则来有效计算梯度的技术。

首先，我们可视化[ReLU](https://en.wikipedia.org/wiki/Rectifier_%28neural_networks%29)激活，定义如下：

![2eb7203d4a0fe09e5f732b5f0fe5b17216188abc](https://yqfile.alicdn.com/2eb7203d4a0fe09e5f732b5f0fe5b17216188abc.png)



要计算梯度（直观地说，斜率），你可以想象一个分段函数，由指标函数表示如下：

![e7018c1ce34682151c7c48683387f4f0da3b8d0c](https://yqfile.alicdn.com/e7018c1ce34682151c7c48683387f4f0da3b8d0c.png)

NumPy为我们提供了有用、直观的语法，我们的激活函数（蓝色曲线）可以在代码中解释，其中x是我们的输入，relu是我们的输出：

relu = np.maximum(x, 0)

接下来是渐变（红色曲线），其中grad描述了upstream渐变：

grad[x < 0] = 0

在没有首先自己推导出梯度的情况下，这行代码你可能看的不是很明白。在我们的代码行中，(grad)对于满足条件的所有元素，将upstream梯度中的所有值设置为0 [h<0]。在数学上，这实际上相当于ReLU梯度的分段表示，当乘以upstream梯度时，它会将小于0的所有值压缩为0！

正如我们在这里看到的那样，通过我们对微积分的基本理解，我们可以清楚地思考代码。可以在[此处](https://pytorch.org/tutorials/beginner/pytorch_with_examples.html)找到此神经网络实现的完整示例。

**为构建机器学习产品的数学**

为了写这部分，我与机器学习工程师进行了交谈，以确定数学在调试系统时最有帮助的地方。以下是工程师自己回答的数学在机器学习中的问题。希望你能从中发现一些有价值的问题。

问：我应该使用什么样的聚类方法来可视化高维客户数据？
方法：[PCA与tSNE](https://stats.stackexchange.com/questions/238538/are-there-cases-where-pca-is-more-suitable-than-t-sne)

问：我应该如何校准“阻止”欺诈性用户交易的阈值？
方法：[概率校准](http://scikit-learn.org/stable/modules/calibration.html)

通常，统计和线性代数可以以某种方式用于这些问题中的每一个。但是，要获得满意的答案通常需要针对特定领域的方法。如果是这样的话，你如何缩小你需要学习的数学类型？

**定义你的系统**

市场上有很多资源（例如，数据分析的[scikit-learn](http://scikit-learn.org/stable/)，深度学习的[keras](https://keras.io/)）它们将帮助你跳转编写代码来为你的系统建模。在你打算这样做的时候，尝试回答以下有关你需要构建管道的问题：

1.你系统的输入/输出是什么？

2.你应该如何准备数据以适合你的系统？

3.如何构建特征或策划数据以帮助你的模型进行概括？

4.你如何为你的问题定义合理的目标？

你可能会感到惊讶，定义一个系统竟然需要处理那么多问题！之后，管道建设所需的工程也是非常重要的。换句话说，构建机器学习产品需要大量繁重的工作，不需要深入的数学背景。

资源

• Google的研究科学家Martin Zinkevich [为ML工程提供](https://developers.google.com/machine-learning/guides/rules-of-ml/)的[最佳实践](https://developers.google.com/machine-learning/guides/rules-of-ml/)

**需要什么数学知识就需要什么！**

当你的头脑中完全进入到机器学习工作流程时，你可能会发现有一些步骤会被卡住，特别是在调试时。当你被困住时，你知道要查找什么吗？你的权重是否合理？为什么你的模型不能与特定的损失定义融合？衡量成功的正确方法是什么？此时，对数据进行假设，以不同方式约束优化或尝试不同的算法可能会有所帮助。

通常，你会发现建模/调试过程中存在数学直觉（例如，选择损失函数或评估指标），这些直觉可能有助于做出明智的工程决策。这些都是你学习的机会！来自[Fast.ai的](http://www.fast.ai/) Rachel Thomas 是这种“按需”学习方法的支持者。

**资源：**

•课程：[计算线性代数](http://www.fast.ai/2017/07/17/num-lin-alg/) by fast.ai ；

•YouTube：[3blue1brown](https://www.youtube.com/channel/UCYO_jab_esuFRV4b17AJtAw)：[线性代数](https://www.youtube.com/watch?v=kjBOesZCoqc&list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab)和[微积分的](https://www.youtube.com/watch?v=WUvTyaaNkzM&list=PLZHQObOWTQDMsr9K-rj53DwVRMYO3t5Yr)本质；

•教科书：[线性代数](http://linear.axler.net/)，Axler；

•教科书：Tibshirani等人[的统计学习元素](https://web.stanford.edu/~hastie/ElemStatLearn/)；

•课程：[斯坦福大学的CS229（机器学习）课程笔记](http://cs229.stanford.edu/syllabus.html#opt)。

**数学用于机器学习研究**

我现在想要描述对于机器学习中以研究为导向的工作有用的数学思维方式。机器学习研究的观点指向即插即用系统，在这些系统中，模型会投入更多计算以训练出更高的性能。在某些圈子里，[研究人员仍然怀疑](https://arxiv.org/ftp/arxiv/papers/1801/1801.00631.pdf)缺乏数学严谨性的方法可以将我们带入人类智慧的圣杯。

值得关注的是，研究人员需要提供原始资源，例如新的基础构建模块，可用于获取全新的洞察力和实地目标的方法。这可能意味着重新思考用于图像分类的卷积神经网络等基础模块，正如Geoff Hinton在他最近的Capsule Networks [论文](https://arxiv.org/pdf/1710.09829v1.pdf)中所做的[那样](https://arxiv.org/pdf/1710.09829v1.pdf)。

为了实现机器学习的下一步，我们需要提出基本问题。这需要深度数学成熟，因为整个过程涉及数千小时的“卡住”，提出问题，并在追求新问题时翻转问题观点。“有趣的探索”使科学家们能够提出深刻，富有洞察力的问题，而不仅仅是简单的想法/架构的结合。



ML研究是一个非常丰富的研究领域，在公平性、可解释性和可访问性方面都存在紧迫问题。越来越多的研究者希望从数学的角度来解决这些问题，而非辩证性的去看待问题。

 [**数十款阿里云产品限时折扣中，赶紧点击领劵开始云上实践吧！**](https://promotion.aliyun.com/ntms/act/ambassador/sharetouser.html?userCode=j4nkrg1c&utm_source=j4nkrg1c)

以上为译文。

本文由[阿里云云栖社区](http://weibo.com/taobaodeveloperclub)组织翻译。

**文章原标题《learning-math-for-machine-learning****》，**

**作者：**[Vincent Chen](https://blog.ycombinator.com/author/vincent-chen/) **译者：虎说八道**，审校：。

















**文章为简译，更为详细的内容，请查看****原文****。**





https://yq.aliyun.com/articles/625130?utm_content=m_1000012615

