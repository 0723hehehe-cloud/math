---
type: 错题本
tags:
  - 错题本/高等数学/05-二重积分/交换积分次序与凑微分dtan/二重积分交换次序与凑微分dtany秒杀计算
---

# 二重积分交换次序与凑微分d(tany)秒杀计算

### 题目

计算二重积分：
$$I = \int_0^1 \frac{1}{3}x^{-\frac{2}{3}} dx \int_{\arctan x}^{\frac{\pi}{4}} \csc 2y \\, dy$$

[!failure] ❌ 真实错因剖析
**做错/卡壳原因**：**交换积分次序换限之后，外层积分不会积！**
顺利交换次序算完内层积出 $(\tan y)^{1/3}$ 后，面对外层被积函数 $\csc 2y \cdot (\tan y)^{1/3}$ 感到棘手卡住，没有想到利用三角恒等式 $\csc 2y = \frac{\sec^2 y}{2\tan y}$ 凑微分出 $d(\tan y)$！ > [!tip] 💡 核心秒杀法宝：【交换次序 + 凑微分 $d(\tan y)$】 1. **交换积分次序**：原区域 $0 \le x \le 1, \arctan x \le y \le \frac{\pi}{4}$ 转化为先 $x$ 后 $y$：  $$I = \int_0^{\frac{\pi}{4}} \csc 2y \\, dy \int_0^{\tan y} \frac{1}{3}x^{-\frac{2}{3}} dx = \int_0^{\frac{\pi}{4}} \csc 2y \cdot (\tan y)^{\frac{1}{3}} \\, dy$$
2. **凑微分恒等式**：利用 $\csc 2y = \frac{1}{2\sin y \cos y} = \frac{1}{2} \frac{\sec^2 y}{\tan y}$，凑出 $d(\tan y)$：  $$I = \frac{1}{2} \int_0^{\frac{\pi}{4}} (\tan y)^{-\frac{2}{3}} \\, d(\tan y) = \frac{1}{2} \int_0^1 u^{-\frac{2}{3}} du = \frac{3}{2}$$

### 解析与答案

1. **交换积分次序（画图换限）**：
   原区域 $D: \begin{cases} 0 \le x \le 1 \\\\ \arctan x \le y \le \frac{\pi}{4} \end{cases} \iff \begin{cases} 0 \le y \le \frac{\pi}{4} \\\\ 0 \le x \le \tan y \end{cases}$。 > 2. **先算内层对 $x$ 的积分**：  $$\int_0^{\tan y} \frac{1}{3} x^{-\frac{2}{3}} dx = \left[ x^{\frac{1}{3}} \right]_0^{\tan y} = (\tan y)^{\frac{1}{3}}$$

3. **凑微分求外层积分**：
   因为 $\csc 2y = \frac{1}{\sin 2y} = \frac{1}{2\sin y \cos y} = \frac{\sec^2 y}{2\tan y}$，代入得：  $$I = \int_0^{\frac{\pi}{4}} \frac{\sec^2 y}{2\tan y} \cdot (\tan y)^{\frac{1}{3}} dy = \frac{1}{2} \int_0^{\frac{\pi}{4}} (\tan y)^{-\frac{2}{3}} \sec^2 y \\, dy$$
   由 $\sec^2 y dy = d(\tan y)$，令 $u = \tan y$：  $$I = \frac{1}{2} \int_0^1 u^{-\frac{2}{3}} du = \frac{1}{2} \left[ 3 u^{\frac{1}{3}} \right]_0^1 = \frac{3}{2}$$

### 易错点 & 核心考点

⚠️ **避坑死穴与高频恒等式**：
1. **$\csc 2y$ 凑微分公式**：遇 $\csc 2y \cdot f(\tan y)$ 必用 $\csc 2y \, dy = \frac{1}{2\tan y} d(\tan y)$！ 2. **反三角函数换限**：$y = \arctan x \implies x = \tan y$（注意取值范围 $y \in [0, \pi/4]$）。

![题目图片](file:///D:/ob/考研数学/.images/media__1785374017615.png)