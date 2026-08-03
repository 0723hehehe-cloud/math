---
type: 错题本
tags:
  - 错题本/高等数学/01-函数极限与连续/对数比值极限与拆分化简/已知fg比值极限求对数比值极限
source: 考研数学经典题

---

# 已知fg比值极限求对数比值极限

### ❌ 为什么错（个人错因与盲区）

- **核心错因**: 误用洛必达法则。题目仅给出极限 $\lim f(x)=\dots, \lim g(x)=\dots$，并未保证 $f(x)$ 与 $g(x)$ 可导，且无法保证求导后极限存在，故不能直接对原式使用洛必达法则。

### 题目

设 $\lim_{x \to +\infty} f(x) = +\infty, \lim_{x \to +\infty} g(x) = +\infty$, 且 $\lim_{x \to +\infty} \frac{f(x)}{g(x)} = a > 0$, 计算 $\lim_{x \to +\infty} \frac{\ln f(x)}{\ln g(x)}$.

![题目图片](file:///D:/ob/考研数学/.images/media_1785756807021.png)

### 解析与答案

**相关知识点**: [[对数比值极限与拆分化简]]

本题的核心破局点是：**利用对数性质将 $\ln f(x)$ 拆分为 $\ln g(x) + \ln \frac{f(x)}{g(x)}$（或分子加减 $\ln g(x)$），将式子变形为 $1 + \frac{\ln (f(x)/g(x))}{\ln g(x)}$ 求解。**

**正确推导步骤**：

利用对数的乘积拆分性质（或分子加减 $\ln g(x)$ 化简）：
$$\ln f(x) = \ln \left( g(x) \cdot \frac{f(x)}{g(x)} \right) = \ln g(x) + \ln \left( \frac{f(x)}{g(x)} \right)$$

代入欲求极限中：
$$\frac{\ln f(x)}{\ln g(x)} = \frac{\ln g(x) + \ln \left( \frac{f(x)}{g(x)} \right)}{\ln g(x)} = 1 + \frac{\ln \left( \frac{f(x)}{g(x)} \right)}{\ln g(x)}$$

考虑 $x \to +\infty$ 时的极限：
1. 因为 $\lim_{x \to +\infty} \frac{f(x)}{g(x)} = a > 0$，根据对数函数的连续性，有：
$$\lim_{x \to +\infty} \ln \left( \frac{f(x)}{g(x)} \right) = \ln a$$

2. 因为 $\lim_{x \to +\infty} g(x) = +\infty$，所以：
$$\lim_{x \to +\infty} \ln g(x) = +\infty$$

由于分子为有限常数 $\ln a$，分母趋于 $+\infty$，故：
$$\lim_{x \to +\infty} \frac{\ln \left( \frac{f(x)}{g(x)} \right)}{\ln g(x)} = 0$$

最终得出：
$$\lim_{x \to +\infty} \frac{\ln f(x)}{\ln g(x)} = 1 + 0 = 1$$

填空题答案为 **1**。

### 易错点 & 核心考点

- **核心考点**: 对数比值极限与拆分化简。
- **解题关键**: 利用对数性质将 $\ln f(x)$ 拆分为 $\ln g(x) + \ln \frac{f(x)}{g(x)}$（或分子加减 $\ln g(x)$），将式子变形为 $1 + \frac{\ln (f(x)/g(x))}{\ln g(x)}$ 求解。
- **易错点**: 误用洛必达法则。题目仅给出极限 $\lim f(x)=\dots, \lim g(x)=\dots$，并未保证 $f(x)$ 与 $g(x)$ 可导，且无法保证求导后极限存在，故不能直接对原式使用洛必达法则。
