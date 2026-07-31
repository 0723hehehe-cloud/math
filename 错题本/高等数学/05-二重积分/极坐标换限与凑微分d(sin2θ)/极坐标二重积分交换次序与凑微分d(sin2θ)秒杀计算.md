---
type: 错题
tags:
  - 错题本/高等数学/05-二重积分/极坐标换限与凑微分d(sin2θ)

# 极坐标二重积分交换次序与凑微分d(sin2θ)秒杀计算

> [!question] 题目
> 设有界区域 $D$ 是由圆 $x^2 + y^2 = 1$ 和直线 $y = x$ 以及 $X$ 轴所围成的在第一象限的图形，计算二重积分：
> $$I = \i\int_D e^{(x+y)^2} (x^2 - y^2) dxdy$$
>
> ![题目图片](file:///D:/ob/考研数学/.images/media__1785498465403.png)

> [!tip] ⚡ 秒杀法宝：【极坐标 ⟹ 交换次序（先 $\theta$ 后 $r$） ⟹ 凑微分 $d(\sin 2\theta)$】
> 1. **三角恒等转换**：$(x+y)^2 = r^2(1+\sin 2\theta)$，$x^2-y^2 = r^2 \cos 2\theta$；
> 2. **交换次序化简**：转为先对 $\theta$ 积分：$I = \int_0^1 r^3 dr \int_0^{\frac{\pi}{4}} e^{r^2(1+\sin 2\theta)} \cos 2\theta d\theta$；
> 3. **凑微分秒杀**：内层凑微分 $\frac{1}{2r^2} d[r^2(1+\sin 2\theta)]$，把内层瞬间积出为 $\frac{1}{2r^2}(e^{2r^2}-e^{r^2})$，外层直接转化为 $\frac{1}{4} \int_0^1 (e^{2u}-e^u) du = \mathbf{\frac{(e-1)^2}{8}}$！

> [!failure] ❌ 真实错因剖析
> **做错/卡壳原因**：**直接硬算计算量极大死掉！**
> 如果在直角坐标系下硬算，或者在极坐标下顺手先对 $r$ 积分（需要对 $r^3 e^{r^2 k}$ 进行繁琐的分部积分），导致计算量巨大且极易算错死掉。

> [!success] 解析与答案
> 1. **转极坐标与化简被积函数**：
>    区域 $D: 0 \le \theta \le \frac{\pi}{4}, 0 \le r \le 1$。
>    $(x+y)^2 = r^2(1+\sin 2\theta)$， $x^2-y^2 = r^2 \cos 2\theta$， $dxdy = r dr d\theta$。
>    $$I = \int_0^{\frac{\pi}{4}} \cos 2\theta d\theta \int_0^1 r^3 e^{r^2(1+\sin 2\theta)} dr$$
>
> 2. **交换积分次序（先对 $\theta$ 积分）**：
>    $$I = \int_0^1 r^3 dr \int_0^{\frac{\pi}{4}} e^{r^2(1+\sin 2\theta)} \cos 2\theta d\theta$$
>
> 3. **内层凑微分 $d(\sin 2\theta)$**：
>    $$\int_0^{\frac{\pi}{4}} e^{r^2(1+\sin 2\theta)} \cos 2\theta d\theta = \frac{1}{2r^2} \int_0^{\frac{\pi}{4}} e^{r^2(1+\sin 2\theta)} d[r^2(1+\sin 2\theta)]$$
>    代入上下限 $\theta = 0 \to r^2$, $\theta = \frac{\pi}{4} \to 2r^2$：
>    $$= \frac{1}{2r^2} (e^{2r^2} - e^{r^2})$$
>
> 4. **外层求积分得出结果**：
>    $$I = \int_0^1 r^3 \cdot \frac{1}{2r^2} (e^{2r^2} - e^{r^2}) dr = \frac{1}{2} \int_0^1 r (e^{2r^2} - e^{r^2}) dr$$
>    令 $u = r^2 \implies du = 2r dr$：
>    $$I = \frac{1}{4} \int_0^1 (e^{2u} - e^u) du = \frac{1}{4} \left[ \frac{1}{2} e^{2u} - e^u \right]_0^1 = \frac{(e-1)^2}{8}$$

> [!warning] 易错点 & 核心考点
> ⚠️ **避坑死穴与高频模型**：
> 1. **遇到 $\cos 2	heta \cdot e^{\sin 2	heta}$ 必定交换次序**：极坐标下先对 $	heta$ 凑微分能绝杀一切复杂的 $r$ 幂次！
> 2. **三角恒等变形**：$(x+y)^2 = r^2(1+\sin 2	heta)$，$x^2-y^2 = r^2 \cos 2	heta$ 是考研极度高频的转化公式！
