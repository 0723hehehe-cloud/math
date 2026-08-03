---
type: 解题技巧与易错陷阱
tags:
  - 解题技巧与易错陷阱/高等数学/05-二重积分/极坐标换限与反三角函数定义域/极坐标积分范围与arcsinsin x主值定义域易错陷阱

---

# 极坐标积分范围与arcsin(sin x)主值定义域易错陷阱

### 题目

设 $D: -1 \le x \le 0, \, 1 - \sqrt{1-x^2} \le y \le -x$，则

$$
I = \iint_{D} \frac{\,dx\,dy}{\sqrt{x^2+y^2}\,\sqrt{4-x^2-y^2}} = \underline{\quad\quad}
$$

![[images/media__1785377023961.png|题目图片]]

### ⚡ 秒杀法宝：【反三角主值范围 + 负坐标轴极坐标方程】

1. **$\arcsin(\sin \theta)$ 的第二象限主值**：当 $\theta \in [\frac{3\pi}{4}, \pi]$ 在第二象限时，必须使用诱导公式化简为 **$\arcsin(\sin \theta) = \pi - \theta$**（切勿盲目脱去符号写成 $\theta$）！
2. **负坐标轴直线极坐标方程**：在第二象限，$x = -1$ 的极坐标方程为 **$r = -\sec \theta$**（因 $\cos \theta < 0$，加负号保证半径 $r > 0$）！

### ❌ 真实错因剖析

**做错核心原因**：**没注意反三角函数 $\arcsin$ 的主值范围！** 在计算内层积分 $\int \frac{dr}{\sqrt{4-r^2}} = \arcsin\frac{r}{2}$ 并代入下限 $r = 2\sin \theta$ 时，把 $\arcsin(\sin \theta)$ 错写成了 $\theta$。 忽视了当 $\theta \in [\frac{3\pi}{4}, \pi]$ 时，$\theta$ 已经超出了 $\arcsin$ 的主值范围 $[-\frac{\pi}{2}, \frac{\pi}{2}]$，正确化简应当是 $\arcsin(\sin \theta) = \pi - \theta$！

### 解析与答案

1. **画图与极坐标换限**：
   - 区域 $D$ 在第二象限，角度范围为 $\frac{3\pi}{4} \le \theta \le \pi$。
- 下边界 $y = 1 - \sqrt{1-x^2} ff x^2 + (y-1)^2 = 1 \implies r = 2\sin \theta$。
- 上边界为直线 $x = -1 \implies r = -\sec \theta$。
   故极坐标范围为：

$$
\frac{3\pi}{4} \le \theta \le \pi, \quad 2\sin \theta \le r \le -\sec \theta
$$

2. **列极坐标积分与内层计算**：

$$
I = \int_{\frac{3\pi}{4}}^\pi d\theta \int_{2\sin \theta}^{-\sec \theta} \frac{dr}{\sqrt{4-r^2}} = \int_{\frac{3\pi}{4}}^\pi \left[ \arcsin\left(-\frac{\sec \theta}{2}\right) - \arcsin(\sin \theta) \right] d\theta
$$

3. **精准处理反三角主值与外层积分**：
   因 $\theta \in [\frac{3\pi}{4}, \pi]$，则 $\arcsin(\sin \theta) = \arcsin(\sin(\pi-\theta)) = \pi - \theta$。
   代入并分步计算得出最终结果：

$$
I = \frac{\pi}{4} \ln(\sqrt{2}+1) - \frac{\pi^2}{32}
$$

### 易错点 & 核心考点

⚠️ **避坑死穴**：
1. **反三角脱帽规则**：$\arcsin(\sin x) = x$ **仅在 $x \in [-\frac{\pi}{2}, \frac{\pi}{2}]$ 时成立**！若在第二象限必写为 $\pi - x$。
2. **极坐标半径正负校验**：极坐标半径 $r$ 必须大于零，当 $\theta \in [\frac{3\pi}{4}, \pi]$ 时 $\cos \theta \le 0$，故 $r = -\sec \theta > 0$。