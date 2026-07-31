---
type: 错题
tags:
  - 错题本/高等数学/05-二重积分/椭圆区域广义极坐标与雅可比行列式

# 椭圆区域广义极坐标与雅可比行列式J=abr计算二重积分

> [!question] 题目
> 设 $D = \{(x,y) \mid 4x^2 + y^2 < 1, \, x \ge 0, \, y \ge 0\}$，则积分 $I = \i\int_D (1 - 12x^2 - y^2) dxdy = \text{______}$。
>
> ![题目图片](file:///D:/ob/考研数学/.images/media__1785499842986.png)

> [!tip] ⚡ 秒杀法宝：【广义极坐标 + 雅可比行列式 $J = rac{1}{2}r$ 秒杀】
> 1. **广义极坐标代换**：
>    对椭圆 $4x^2 + y^2 < 1$（即 $\frac{x^2}{(1/2)^2} + y^2 < 1$），令 $x = \frac{1}{2} r \cos \theta, \, y = r \sin \theta$；
> 2. **雅可比行列式微元**：
>    $$J = \frac{\partial(x,y)}{\partial(r,\theta)} = \begin{vmatrix} \frac{1}{2}\cos\theta & -\frac{1}{2}r\sin\theta \\ \sin\theta & r\cos\theta \end{vmatrix} = \frac{1}{2}r \implies dxdy = \frac{1}{2}r \, dr d\theta$$
> 3. **极速积为 0**：
>    被积函数 $1 - 12x^2 - y^2 = 1 - r^2(2+\cos 2\theta)$，积分结果极速得出 **$0$**！

> [!failure] ❌ 真实错因剖析
> **做错/卡壳原因**：
> 1. 广义极坐标代换写错：没有注意到 $x = \frac{1}{2} r \cos \theta$ 对应的系数，或者遗漏了雅可比行列式系数 $J = \frac{1}{2}r$；
> 2. 展开 $12x^2 + y^2 = 3r^2\cos^2\theta + r^2\sin^2\theta$ 时三角降次运算粗心出错。

> [!success] 解析与答案
> 1. **建立广义极坐标与雅可比行列式**：
>    区域 $D$ 是第一象限椭圆域 $\frac{x^2}{(1/2)^2} + y^2 < 1, x \ge 0, y \ge 0$。
>    令 $x = \frac{1}{2} r \cos \theta, y = r \sin 	heta$，此时范围为 $0 \le \theta \le \frac{\pi}{2}, 0 \le r < 1$。
>    面积微元：$dxdy = \frac{1}{2} r \, dr d\theta$。
>
> 2. **代入被积函数**：
>    $$1 - 12x^2 - y^2 = 1 - 12\left(\frac{1}{4} r^2 \cos^2 \theta\right) - r^2 \sin^2 \theta = 1 - r^2 (3\cos^2 \theta + \sin^2 \theta)$$
>    利用恒等式 $3\cos^2 \theta + \sin^2 \theta = 2\cos^2 \theta + 1 = 2 + \cos 2\theta$：
>    $$= 1 - r^2 (2 + \cos 2\theta)$$
>
> 3. **计算二重积分**：
>    $$I = \int_0^{\frac{\pi}{2}} d\theta \int_0^1 \left[ 1 - r^2 (2 + \cos 2\theta) \right] \cdot \frac{1}{2} r \, dr$$
>    先算内层对 $r$ 的积分：
>    $$\int_0^1 \left( \frac{1}{2} r - \frac{1}{2} r^3 (2 + \cos 2\theta) \right) dr = \frac{1}{4} - \frac{1}{8} (2 + \cos 2\theta) = -\frac{1}{8} \cos 2\theta$$
>    外层对 $\theta$ 积分：
>    $$I = \int_0^{\frac{\pi}{2}} \left( -\frac{1}{8} \cos 2\theta \right) d\theta = \left[ -\frac{1}{16} \sin 2\theta \right]_0^{\frac{\pi}{2}} = 0$$

> [!warning] 易错点 & 核心考点
> ⚠️ **雅可比行列式避坑死穴**：
> 1. **椭圆变换微元**：对 $\frac{x^2}{a^2} + \frac{y^2}{b^2} \le 1$，做 $x = a r \cos \theta, y = b r \sin \theta$，微元必为 **$dxdy = a b r \, dr d\theta$**（切勿漏乘 $a \cdot b$）！
> 2. **三角偶次方降次**：$\cos^2 \theta = \frac{1+\cos 2\theta}{2}, \sin^2 \theta = \frac{1-\cos 2\theta}{2}$。
