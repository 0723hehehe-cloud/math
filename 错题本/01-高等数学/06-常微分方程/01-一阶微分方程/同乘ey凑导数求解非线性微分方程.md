---
type: 错题
source: 张宇1000题
tags:
  - 错题本/01-高等数学/06-常微分方程/01-导数与微分/导数定义
---

# 同乘ey凑导数求解非线性微分方程

> [!danger] ❌ 为什么错（个人错因与盲区）
> - **核心错因**: 做题时没有想到给方程两边同乘 $e^y$ 来“凑复合函数求导 $(e^y)' = e^y y'$”，被非线性的 $e^{-y}$ 困住且无法直接分离变量。

> [!question] 题目
> 微分方程 $y' + 1 = e^{-y} \sin x$ 的通解为 ______。

> [!success] 解析与答案
> **相关知识点**: [[同乘法与凑全微分求解非线性微分方程]]
> 
> 本题的核心破局点是：**方程两边同乘 $e^y$ 凑出全微分 $(e^y)' + e^y = \sin x$，令 $u = e^y$ 转化为标准一阶线性微分方程**。
> 
> 本题的核心技巧是：**“同乘 $e^y$ 凑全微分 $(e^y)' = e^y y'$，将非线性微分方程转化为一阶线性微分方程”**。
> 
> ### 1. 两边同乘 $e^y$ 凑导数
> 给原方程 $y' + 1 = e^{-y} \sin x$ 两边同时乘以 $e^y$（由于 $e^y > 0$，恒成立）：
> $\displaystyle e^y y' + e^y = \sin x$
> 
> 注意到复合函数求导公式 $\frac{d}{dx}(e^y) = e^y y'$，方程可变形为：
> $\displaystyle \frac{d}{dx}(e^y) + e^y = \sin x$
> 
> ### 2. 换元转化为标准一阶线性微分方程
> 令 $u = e^y$，则 $u' = e^y y'$，方程化为关于 $u(x)$ 的标准一阶线性微分方程：
> $\displaystyle u' + u = \sin x$
> 
> 积分因子为 $\mu(x) = e^{\int 1 \, dx} = e^x$。两边同乘 $e^x$ 得：
> $\displaystyle (e^x u)' = e^x \sin x$
> 
> ### 3. 积分求解 $u(x)$ 倒推 $y(x)$
> 两边对 $x$ 积分：
> $\displaystyle e^x u = \int e^x \sin x \, dx$
> 利用标准积分公式 $\int e^x \sin x \, dx = \frac{1}{2} e^x (\sin x - \cos x) + C$：
> $\displaystyle e^x u = \frac{1}{2} e^x (\sin x - \cos x) + C$
> 
> 两边同除以 $e^x$ 得：
> $\displaystyle u = \frac{1}{2}(\sin x - \cos x) + C e^{-x}$
> 
> 将 $u = e^y$ 代回：
> $\displaystyle e^y = \frac{1}{2}(\sin x - \cos x) + C e^{-x}$
> 
> 或显式写为：
> $\displaystyle y = \ln \left[ \frac{1}{2}(\sin x - \cos x) + C e^{-x} \right]$
> 
> 填空题答案为 **$e^y = \frac{1}{2}(\sin x - \cos x) + C e^{-x}$**（或其对数显式形式）。

> [!warning] 易错点 & 核心考点
> - **核心考点**: 凑全微分法、换元法化非线性微分方程为一阶线性方程。
> - **解题关键**: 看到方程中含有 $y'$ 与 $e^{-y}$，直接联想“同乘 $e^y$”；看到 $y'$ 与 $y^n$（一阶非线性微分方程（换元法）），直接联想“同乘 $y^{-n}$”。
> - **易错点**: 硬去分离变量导致分母 $e^{-y}\sin x - 1$ 无法积分；积分 $\int e^x \sin x dx$ 时忘记系数 $\frac{1}{2}$。