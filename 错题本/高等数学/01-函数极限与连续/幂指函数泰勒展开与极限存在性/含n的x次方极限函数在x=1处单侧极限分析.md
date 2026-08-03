---
type: 错题本
tags:
  - 错题本/高等数学/01-函数极限与连续/幂指函数泰勒展开与极限存在性/含n的x次方极限函数在x=1处单侧极限分析
source: 风中羽小易

---

# 含n的x次方极限函数在x=1处单侧极限分析

### ❌ 为什么错（个人错因与盲区）

- **核心错因**: 没有想到将 $(1+\frac{1}{n})^n$ 改写为幂指函数后对指数部分 $n\ln(1+\frac{1}{n})$ 进行泰勒展开（展开到 $\frac{1}{n^2}$ 项），导致无法准确得到 $(1+\frac{1}{n})^n - e \sim -\frac{e}{2n}$ 的主部阶数，从而无法判定 $x < 1$ 与 $x > 1$ 时 $n^{x-1}$ 的收敛性。

### 题目

设 $f(x) = \lim_{n \to \infty} n^x \left[ \left(1 + \frac{1}{n}\right)^n - e \right]$，讨论 $f(x)$ 在 $x = 1$ 处的左右极限与连续性。

(A) 左极限存在，右极限不存在
(B) 左极限不存在，右极限存在
(C) 左、右极限都存在，但不相等
(D) 连续

![题目图片](file:///D:/ob/考研数学/.images/media__1785747149464.png)

### 解析与答案

**相关知识点**: [[幂指函数泰勒展开与极限存在性]]

本题的核心破局点是：**将 $(1+\frac{1}{n})^n$ 化为幂指函数 $e^{n \ln(1+\frac{1}{n})}$，展开指数至 $\frac{1}{n}$ 二阶项，求出 $f(x)$ 随 $x$ 取值范围的分段表达式。**

1. **化简括号内结构**：
将 $(1+\frac{1}{n})^n$ 改写为幂指形式：
$$(1+\frac{1}{n})^n = e^{n \ln\left(1 + \frac{1}{n}\right)}$$
利用麦克劳林展开式 $\ln(1+t) = t - \frac{t^2}{2} + o(t^2)$，设 $t = \frac{1}{n}$，得：
$$n \ln\left(1 + \frac{1}{n}\right) = n \left( \frac{1}{n} - \frac{1}{2n^2} + o\left(\frac{1}{n^2}\right) \right) = 1 - \frac{1}{2n} + o\left(\frac{1}{n}\right)$$
因此：
$$(1+\frac{1}{n})^n = e^{1 - \frac{1}{2n} + o\left(\frac{1}{n}\right)} = e \cdot e^{-\frac{1}{2n} + o\left(\frac{1}{n}\right)}$$
再利用 $e^u = 1 + u + o(u)$（取 $u = -\frac{1}{2n}$）：
$$(1+\frac{1}{n})^n = e \left( 1 - \frac{1}{2n} + o\left(\frac{1}{n}\right) \right) = e - \frac{e}{2n} + o\left(\frac{1}{n}\right)$$
即：
$$\left(1+\frac{1}{n}\right)^n - e = -\frac{e}{2n} + o\left(\frac{1}{n}\right) \sim -\frac{e}{2n}$$

2. **求出 $f(x)$ 的分段表达式**：
将上述展开式代入 $f(x)$：
$$f(x) = \lim_{n \to \infty} n^x \left( -\frac{e}{2n} + o\left(\frac{1}{n}\right) \right) = \lim_{n \to \infty} \left( -\frac{e}{2} n^{x-1} \right)$$
- 当 $x < 1$ 时，$x - 1 < 0$，$n^{x-1} = \frac{1}{n^{1-x}} \to 0$，故 $f(x) = 0$；
- 当 $x = 1$ 时，$x - 1 = 0$，$n^{0} = 1$，故 $f(1) = -\frac{e}{2}$；
- 当 $x > 1$ 时，$x - 1 > 0$，$n^{x-1} \to +\infty$，故 $f(x) = -\infty$（极限不存在）。

3. **讨论 $x = 1$ 处的左右极限**：
- 左极限：$\lim_{x \to 1^-} f(x) = \lim_{x \to 1^-} 0 = 0$（存在）；
- 右极限：由于当 $x > 1$ 时 $f(x) = -\infty$，故 $\lim_{x \to 1^+} f(x)$ 不存在。

综上所述，左极限存在，右极限不存在。正确选项为 **A**。

填空题答案为 **A**。

### 易错点 & 核心考点

- **核心考点**: 幂指函数泰勒展开与极限存在性。
- **解题关键**: 将 $(1+\frac{1}{n})^n$ 化为幂指函数 $e^{n \ln(1+\frac{1}{n})}$，展开指数至 $\frac{1}{n}$ 二阶项，求出 $f(x)$ 随 $x$ 取值范围的分段表达式。
- **易错点**: 没有想到将 $(1+\frac{1}{n})^n$ 改写为幂指函数后对指数部分 $n\ln(1+\frac{1}{n})$ 进行泰勒展开（展开到 $\frac{1}{n^2}$ 项），导致无法准确得到 $(1+\frac{1}{n})^n - e \sim -\frac{e}{2n}$ 的主部阶数，从而无法判定 $x < 1$ 与 $x > 1$ 时 $n^{x-1}$ 的收敛性。
