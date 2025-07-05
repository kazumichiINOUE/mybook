# なぜ固有ベクトルで行列の対角化ができるか

これは \\( x = 2y \\) です．

\\( n \\) 次正方行列 \\( A \\)は対角化できるとし，それを\\( \Lambda \\)とする．
対角化の前後で行列\\(A\\)のサイズは変わらないとすると，
行列\\(\Lambda\\)も\\(n\\)次正方行列である．
具体的な成分は次のように書ける．

\[
\Lambda = \left[ 
\begin{matrix}
\lambda_1 & 0         & 0         & \cdots     & 0 \\
0         & \lambda_2 & 0         & \cdots     & 0 \\
0         & 0         & \ddots    &            & \vdots \\
\vdots    & \vdots    &           & \ddots     & 0 \\
0         & 0         & \cdots    & 0          & \lambda_n
\end{matrix}
\right]
\]

\\[
\Lambda = \left[ 
\begin{matrix}
\lambda _1 &  \\
           & \lambda_2 & & \text{\huge{0}} \\ 
           &           & \ddots \\
           & \text{\huge{0}} & & \ddots \\
           & & & & \lambda _n
\end{matrix}
\right]
\\]

それでは，行列$\Lambda$の成分や，対角化するために必要な変換行列を求める．逆行列が存在する行列$T$を仮定し，以下のような変換が成り立つとする．
$$
T^{-1} A T  = \Lambda 
$$
すなわち，行列$T$およびその逆行列$T^{-1}$を行列$A$の両側からかけると，その結果が対角化した行列$\Lambda$となる，と仮定する．

さらに式を変形する．

$$
\begin{aligned}
T^{-1} A T  &= \Lambda \\
T (T^{-1} A T)  &= T \Lambda \quad \text{（両辺に左から$T$をかける）} \\
A T  &= T \Lambda
\end{aligned}
$$
逆行列の定義より，$T \, T^{-1} = I$に注意する．$I$は単位行列である．

$T = [\mathbf{v}_1 \quad \mathbf{v}_2 \quad \cdots \quad \mathbf{v}_n]$と置き，式を展開する．$\mathbf{v}_{i}$ はサイズ$n$の列ベクトルとする．
見やすいように行列$\Lambda$のゼロ成分を明示して展開する．

$$
\begin{aligned}
A T &= T \Lambda \\
A \, [\mathbf{v}_1 \quad \mathbf{v}_2 \quad \cdots \quad \mathbf{v}_n] &= 
[\mathbf{v}_1 \quad \mathbf{v}_2 \quad \cdots \quad \mathbf{v}_n] 
\left[ 
\begin{matrix}
\lambda _1 &  0        & 0     & \cdots & 0\\
         0 & \lambda_2 & 0     & \cdots & \vdots\\ 
    \vdots &         0 & \ddots & & \vdots  \\
       \vdots &    \vdots &        & \ddots & \vdots \\
         0 &         0 &      \cdots &       & \lambda _n
\end{matrix}
\right] \\
\\
[A \, \mathbf{v}_1 \quad A \, \mathbf{v}_2 \quad \cdots \quad A \, \mathbf{v}_n] &= 
[\lambda _1 \mathbf{v}_1 \quad \lambda _2 \mathbf{v}_2 \quad \cdots \quad \lambda _n \mathbf{v}_n] 
\end{aligned}
$$

両辺のベクトルの，同じ成分同士を以下のように並べてみる．
$$
\begin{aligned}
A \, \mathbf{v}_1 &= \lambda _1 \mathbf{v}_1 \\
A \, \mathbf{v}_2 &= \lambda _2 \mathbf{v}_2 \\
&\vdots \\
A \, \mathbf{v}_n &= \lambda _n \mathbf{v}_n
\end{aligned}
$$

これは，それぞれの式が行列$A$に対する固有方程式になっている．これらの方程式を満たすベクトル$\mathbf{v}_{i}$とスカラー$\lambda _{i}$を固有ベクトル・固有値と呼ぶのであった．したがって，行列$T$は固有ベクトルを並べた行列であり，対角行列$\Lambda$の対角成分は固有値であることがわかった．

最初の質問に回答するならば，以下のように言えるだろう．
> [!TIP]
> 対角化された行列の対角成分は固有方程式を満たす

---
### 関連
[[固有方程式はどのような座標変換を表現するか]]


