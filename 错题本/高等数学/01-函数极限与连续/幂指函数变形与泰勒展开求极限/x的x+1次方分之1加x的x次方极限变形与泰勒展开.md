---
type: 错题本
tags:
  - 错题本/高等数学/01-函数极限与连续/幂指函数变形与泰勒展开求极限/x的x+1次方分之1加x的x次方极限变形与泰勒展开
source: 张宇1000题

---

# x的x+1次方分之1加x的x次方极限变形与泰勒展开

### ❌ 为什么错（个人错因与盲区）

- **核心错因**: 没有想到在第一步将 $x^{x+1}$ 拆出一个 $x$，把分子分母同除以 $x^x$ 化简为基本函数结构 $\frac{x}{\left(1+\frac{1}{x}\right)^x}$；若直接对整体通分或盲目求导容易导致计算非常繁琐陷入困境。

### 题目

计算 $\lim_{x \to +\infty} \left[ \frac{x^{x+1}}{(1+x)^x} - \frac{x}{e} \right]$。

![题目图片](file:///D:/ob/考研数学/.images/media__1785747706021.png)

### 解析与答案

**相关知识点**: [[幂指函数变形与泰勒展开求极限]]

本题的核心破局点是：**第一步将 $\frac{x^{x+1}}{(1+x)^x}$ 拆分为 $x \cdot \left(\frac{x}{1+x}\right)^x = \frac{x}{\left(1+\frac{1}{x}\right)^x}$，提出 $x$ 转化为基本幂指函数 $\left(1+\frac{1}{x}\right)^{-x}$，再利用泰勒展开（展开到 $\frac{1}{x}$ 一阶项）破局。**

1. **第一步变形（化为基本函数结构）**：
观察分子 $x^{x+1} = x \cdot x^x$，分母为 $(1+x)^x$。
将 $x^x$ 与分母结合，分子分母同除以 $x^x$：
$$\frac{x^{x+1}}{(1+x)^x} = x \cdot \frac{x^x}{(1+x)^x} = x \cdot \left( \frac{x}{1+x} \right)^x = \frac{x}{\left( 1 + \frac{1}{x} \right)^x} = x \left( 1 + \frac{1}{x} \right)^{-x}$$
原式可变形为：
$$\lim_{x \to +\infty} \left[ \frac{x^{x+1}}{(1+x)^x} - \frac{x}{e} \right] = \lim_{x \to +\infty} x \left[ \left( 1 + \frac{1}{x} \right)^{-x} - \frac{1}{e} \right]$$

2. **使用换元与泰勒展开化简**：
设 $t = \frac{1}{x}$，当 $x \to +\infty$ 时，$t \to 0^+$。原式变为：
$$\lim_{t \to 0^+} \frac{1}{t} \left[ (1+t)^{-1/t} - \frac{1}{e} \right]$$
对 $(1+t)^{-1/t}$ 进行泰勒展开：
$$(1+t)^{-1/t} = e^{-\frac{1}{t} \ln(1+t)}$$
利用 $\ln(1+t) = t - \frac{t^2}{2} + o(t^2)$，得：
$$-\frac{1}{t} \ln(1+t) = -\frac{1}{t} \left( t - \frac{t^2}{2} + o(t^2) \right) = -1 + \frac{t}{2} + o(t)$$
因此：
$$(1+t)^{-1/t} = e^{-1 + \frac{t}{2} + o(t)} = \frac{1}{e} \cdot e^{\frac{t}{2} + o(t)}$$
再利用 $e^u = 1 + u + o(u)$（取 $u = \frac{t}{2}$）：
$$(1+t)^{-1/t} = \frac{1}{e} \left( 1 + \frac{t}{2} + o(t) \right) = \frac{1}{e} + \frac{t}{2e} + o(t)$$

3. **代入求极限**：
将展开式代入极限中：
$$\lim_{t \to 0^+} \frac{1}{t} \left[ \left( \frac{1}{e} + \frac{t}{2e} + o(t) \right) - \frac{1}{e} \right] = \lim_{t \to 0^+} \frac{1}{t} \left( \frac{t}{2e} + o(t) \right) = \frac{1}{2e}$$

故最终答案为 $\frac{1}{2e}$。

填空题答案为 **\frac{1}{2e}**。

### 易错点 & 核心考点

- **核心考点**: 幂指函数变形与泰勒展开求极限。
- **解题关键**: 第一步将 $\frac{x^{x+1}}{(1+x)^x}$ 拆分为 $x \cdot \left(\frac{x}{1+x}\right)^x = \frac{x}{\left(1+\frac{1}{x}\right)^x}$，提出 $x$ 转化为基本幂指函数 $\left(1+\frac{1}{x}\right)^{-x}$，再利用泰勒展开（展开到 $\frac{1}{x}$ 一阶项）破局。
- **易错点**: 没有想到在第一步将 $x^{x+1}$ 拆出一个 $x$，把分子分母同除以 $x^x$ 化简为基本函数结构 $\frac{x}{\left(1+\frac{1}{x}\right)^x}$；若直接对整体通分或盲目求导容易导致计算非常繁琐陷入困境。
