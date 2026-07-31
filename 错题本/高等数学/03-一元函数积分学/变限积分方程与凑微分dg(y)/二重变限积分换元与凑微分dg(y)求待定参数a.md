---
type: 错题本
tags:
  - 错题本/高等数学/03-一元函数积分学/变限积分方程与凑微分dg(y)/二重变限积分换元与凑微分dg(y)求待定参数a
---


# 二重变限积分平移换元与凑微分d[g(y)]求待定参数a

> [!question] 题目
> 设 $f(x)$ 是 $[0,1]$ 上的连续函数且其在 $[0,1]$ 上的平均值 $\bar{{f}} = \frac{{1}}{{2}}$，满足 $f(x) + a \int_1^x f(y) f(y-x) dy = 1$，求常数 $a$ 的值。
>
> ![题目图片](file:///D:/ob/考研数学/.images/media__1785492363087.png)

![题目图片](file:///D:/ob/考研数学/.images/media__1785492363087.png)

> [!tip] ⚡ 秒杀法宝：【两端求积分 + 平移换元 + 凑微分 $dg(y)$】
> 1. **平均值解码**：$\bar{{f}} = \int_0^1 f(x) dx = \frac{{1}}{{2}}$；
> 2. **两端求积分**：$\int_0^1 f(x) dx - a \int_0^1 dx \int_x^1 f(y)f(y-x) dy = 1 mplies \frac{{1}}{{2}} - a I = 1 mplies a I = -\frac{{1}}{{2}}$；
> 3. **内层平移换元**：交换次序后内层 $\int_0^y f(y-x) dx \xrightarrow{{t=y-x}} \int_0^y f(t) dt$；
> 4. **变限积分凑微分**：设 $g(y) = \int_0^y f(t) dt mplies f(y) dy = dg(y)$！
>    $$I = \int_0^1 g(y) dg(y) = \frac{{1}}{{2}} g^2(1) = \frac{{1}}{{2}} \left(\frac{{1}}{{2}}\right)^2 = \frac{{1}}{{8}}$$
>    瞬间得出 $a = -4$！

> [!failure] ❌ 真实错因剖析
> **做错/卡壳原因**：**没有想到凑微分 $d\left[\int_0^y f(t)dt\right]$！**
> 在对已知关系式两端积分并交换次序、平移换元后，得到 $I = \int_0^1 f(y) \left[\int_0^y f(t)dt\right] dy$。
> 面对含有抽象函数 $f(y)$ 的二重变限积分，没有敏锐识别出 $f(y)dy = d\left[\int_0^y f(t)dt\right]$ 凑微分，导致计算卡死。

> [!success] 解析与答案
> 1. **两端取积分与方程关系**：
>    已知 $\int_0^1 f(x) dx = \frac{{1}}{{2}}$。
>    对 $f(x) - a \int_x^1 f(y)f(y-x) dy = 1$ 两端求积分：
>    $$\int_0^1 f(x) dx - a \int_0^1 dx \int_x^1 f(y)f(y-x) dy = \int_0^1 1 \, dx = 1$$
>    设 $I = \int_0^1 dx \int_x^1 f(y)f(y-x) dy$，则有：
>    $$\frac{{1}}{{2}} - a I = 1 mplies a I = -\frac{{1}}{{2}}$$
>
> 2. **交换积分次序与平移换元**：
>    交换次序为先 $x$ 后 $y$：
>    $$I = \int_0^1 dy \int_0^y f(y)f(y-x) dx = \int_0^1 f(y) dy \int_0^y f(y-x) dx$$
>    内层令 $t = y - x mplies dx = -dt$：
>    $$\int_0^y f(y-x) dx = \int_0^y f(t) dt$$
>    故：
>    $$I = \int_0^1 f(y) \left[ \int_0^y f(t) dt \right] dy$$
>
> 3. **凑微分计算 $I$**：
>    令 $g(y) = \int_0^y f(t) dt mplies dg(y) = f(y) dy$。
>    $g(0) = 0, g(1) = \int_0^1 f(t) dt = \frac{{1}}{{2}}$。
>    $$I = \int_0^1 g(y) \, dg(y) = \left[ \frac{{1}}{{2}} g^2(y) \right]_0^1 = \frac{{1}}{{2}} \left(\frac{{1}}{{2}}\right)^2 = \frac{{1}}{{8}}$$
>
> 4. **求解常数 $a$**：
>    $$a \times \frac{{1}}{{8}} = -\frac{{1}}{{2}} mplies a = -4$$

> [!warning] 易错点 & 核心考点
> ⚠️ **避坑死穴与高频模型**：
> 1. **平均值翻译**：$\bar{{f}} = \frac{{1}}{{b-a}} \int_a^b f(x) dx$。
> 2. **二重积分凑微分模式**：遇 $\int_0^1 f(y) \left[\int_0^y f(t)dt\right] dy$ 必须自动触发凑微分 $g \, dg = \frac{{1}}{{2}} g^2(1)$！