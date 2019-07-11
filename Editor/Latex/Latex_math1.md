# [MathJax basic tutorial and quick reference](https://math.meta.stackexchange.com/questions/5020/mathjax-basic-tutorial-and-quick-reference)


## Tutorial 
1. To see how any formula was written in any question or answer, including this one, right-click on the expression it and choose "`Show Math As` > `TeX Commands`". (When you do this, the `$` will not display. Make sure you add these. See the next point.)

2. **For inline formulas, enclose the formula in `$...$`. For displayed formulas, use `$$...$$`.**
These render differently. For example, type
`$\sum_{i=0}^n i^2 = \frac{(n^2+n)(2n+1)}{6}$`
to show $\sum_{i=0}^n i^2 = \frac{(n^2+n)(2n+1)}{6}$(which is inline mode) or type
`$$\sum_{i=0}^n i^2 = \frac{(n^2+n)(2n+1)}{6}$$`
to show
$$\sum_{i=0}^n i^2 = \frac{(n^2+n)(2n+1)}{6}$$
(which is display mode).

3. **For Greek letters**, use `\alpha`, `\beta`, …, `\omega`: $\alpha$, $\beta$, …, $\omega$. For uppercase, use `\Gamma`, `\Delta`, …, `\Omega`: $\Gamma$, $\Delta$, …, $\Omega$.

4. For **superscripts and subscripts**, use `^` and `_`. For example, `x_i^2`: $x_i^2$, `\log_2 x`: $\log_2 x$.

5. **Groups**. Superscripts, subscripts, and other operations apply only to the next “group”. A “group” is either a single symbol, or any formula surrounded by curly braces {…}. If you do 10^10, you will get a surprise: 1010. But 10^{10} gives what you probably wanted: 1010. Use curly braces to delimit a formula to which a superscript or subscript applies: x^5^6 is an error; {x^y}^z is 𝑥𝑦𝑧, and x^{y^z} is 𝑥𝑦𝑧. Observe the difference between x_i^2 𝑥2𝑖 and x_{i^2} 𝑥𝑖2.

6. **Parentheses** Ordinary symbols` ()[]` make parentheses and brackets `(2+3)[4+4]`. Use `\{` and `\}` for curly braces `{}`.  
These do not scale with the formula in between, so if you write `(\frac{\sqrt x}{y^3})` the parentheses will be too small: $(\frac{\sqrt x}{y^3})$. Using `\left(…\right)` will make the sizes adjust automatically to the formula they enclose: `\left(\frac{\sqrt x}{y^3}\right)` is $\left(\frac{\sqrt x}{y^3}\right)$.  
`\left` and `\right` apply to all the following sorts of parentheses: `(` and `)` $(x)$, `[` and `]` $[x]$, `\{` and `\}` $\{x\}$, `|` $|x|$, `\vert` $\vert x \vert$, `\Vert` $\Vert x \Vert$, `\langle` and `\rangle` $\langle x \rangle$,  `\lceil` and `\rceil` $\lceil x \rceil$, and `\lfloor` and `\rfloor` $\lfloor x  \rfloor$. `\middle` can be used to add additional dividers. There are also invisible parentheses, denoted by `.`:   `\left.\frac12\right\rbrace` is $\left.\frac12\right\rbrace$.  
If manual size adjustments are required: `\Biggl(\biggl(\Bigl(\bigl((x)\bigr)\Bigr)\biggr)\Biggr)` gives $\Biggl(\biggl(\Bigl(\bigl((x)\bigr)\Bigr)\biggr)\Biggr)$.

7. **Sums and integrals** `\sum` and `\int`; the subscript is the lower limit and the superscript is the upper limit, so for example `\sum_1^n` $\sum_1^n$. Don't forget `{…}` if the limits are more than a single symbol. For example, `\sum_{i=0}^\infty i^2` is $\sum_{i=0}^\infty i^2$. Similarly, `\prod` $\prod$, `\int` $\int$, `\bigcup` $\bigcup$, `\bigcap` $\bigcap$, `\iint` $\iint$, `\iiint` $\iiint$, `\idotsint` , `\oint` $\oint$.

8. **Fractions** There are three ways to make these. `\frac ab` applies to the next two groups, and produces $\frac ab$; for more complicated numerators and denominators use `{…}`:` \frac{a+1}{b+1}` is $\frac{a+1}{b+1}$. If the numerator and denominator are complicated, you may prefer `\over`, which splits up the group that it is in: `{a+1\over b+1}` is ${a+1\over b+1}$. Using `\cfrac{a}{b} `command is useful for continued fractions $\cfrac{a}{b}$, more details for which are given in this sub-article.

9. **Fonts**  
    - Use `\mathbb` or `\Bbb` for "blackboard bold": $\mathbb{CHNQRZ}$.  
    - Use `\mathbf` for boldface: $\mathbf{ABCDEFGHIJKLMNOPQRSTUVWXYZ}$  $\mathbf{abcdefghijklmnopqrstuvwxyz}$.
    - Use `\mathit` for italics: $\pmb{ABCDEFGHIJKLMNOPQRSTUVWXYZ}$ $\pmb{abcdefghijklmnopqrstuvwxyz}$  
    - Use `\pmb` for boldfaced italics: $\mathit{ABCDEFGHIJKLMNOPQRSTUVWXYZ}$ $\mathit{abcdefghijklmnopqrstuvwxyz}$
    - Use `\mathtt` for "typewriter" font: $\mathtt{ABCDEFGHIJKLMNOPQRSTUVWXYZ}$ $\mathrm{abcdefghijklmnopqrstuvwxyz}$
    - Use `\mathrm` for roman font: $\mathrm{ABCDEFGHIJKLMNOPQRSTUVWXYZ}$ $\mathrm{abcdefghijklmnopqrstuvwxyz}$
    - Use `\mathsf` for sans-serif font: $\mathsf{ABCDEFGHIJKLMNOPQRSTUVWXYZ}$$\mathsf{abcdefghijklmnopqrstuvwxyz}$.
    - Use `\mathcal` for "calligraphic" letters: $\mathcal{ ABCDEFGHIJKLMNOPQRSTUVWXYZ}$
    - Use `\mathscr` for script letters: $\mathscr{ABCDEFGHIJKLMNOPQRSTUVWXYZ}$
    - Use `\mathfrak` for "Fraktur" (old German style) letters: $\mathfrak{ABCDEFGHIJKLMNOPQRSTUVWXYZ} \mathfrak{abcdefghijklmnopqrstuvwxyz}$

10. **Radical signs** Use sqrt, which adjusts to the size of its argument: `\sqrt{x^3}` $\sqrt{x^3}$; `\sqrt[3]{\frac xy}` $\sqrt[3]{\frac xy}$. For complicated expressions, consider using `{...}^{1/2}` instead.

11. Some **special functions** such as "`lim`", "`sin`", "`max`", "`ln`", and so on are normally set in roman font instead of italic font. Use `\lim`, `\sin`, etc. to make these: `\sin x` $\sin x$, not `sin x` $sin x$. Use subscripts to attach a notation to `\lim`: `\lim_{x\to 0}` $\lim_{x\to 0}$

12. There are a very large number of **special symbols and notations**, too many to list here; see this shorter listing, or this exhaustive listing. Some of the most common include:  
    - `\lt` `\gt` `\le` `\leq` `\leqq` `\leqslant` `\ge` `\geq` `\geqq` `\geqslant` `\neq` $\lt \gt \le \leq \leqq \leqslant \ge \geq \geqq \geqslant \neq$. You can use `\not` to put a slash through almost anything: `\not\lt` $\not\lt$ but it often looks bad.
    - `\times` `\div` `\pm` `\mp` $\times \div \pm \mp$. `\cdot` is a centered dot: $x \cdot y$
    - `\cup \cap \setminus \subset \subseteq \subsetneq \supset \in \notin \emptyset \varnothing` $\cup \cap \setminus \subset \subseteq \subsetneq \supset \in \notin \emptyset \varnothing$
    - {`n+1 \choose 2k}` or `\binom{n+1}{2k}` $\binom{n+1}{2k}$
    - `\to \rightarrow \leftarrow \Rightarrow \Leftarrow \mapsto` $\to \rightarrow \leftarrow \Rightarrow \Leftarrow \mapsto$
    - `\land \lor \lnot \forall \exists \top \bot \vdash \vDash` $\land \lor \lnot \forall \exists \top \bot \vdash \vDash$
    - `\star \ast \oplus \circ \bulle`t $\star \ast \oplus \circ \bullet$
    - `\approx \sim \simeq \cong \equiv \prec \lhd \therefore` $\approx \sim \simeq \cong \equiv \prec \lhd \therefore$
    - `\infty \aleph_0` $\infty \aleph_0$ `\nabla` `\partial` $\nabla$ $ \partial$ `\Im \Re` $\Im $ $\Re$
    - For modular equivalence, use `\pmod` like this: `a\equiv b\pmod n` $a\equiv b\pmod n$.
    - `\ldots` is the dots in $a_1, a_2, \ldots ,a_n$ `\cdots` is the dots in $a_1+a_2+\cdots+a_n$
    - Some Greek letters have variant forms:` \epsilon \varepsilon` $ \epsilon \varepsilon$, `\phi \varphi` $\phi \varphi$, and others. Script lowercase `l` is `\ell` $\ell$.  
Detexify lets you draw a symbol on a web page and then lists the $\TeX$ symbols that seem to resemble it. These are not guaranteed to work in MathJax but are a good place to start. To check that a command is supported, note that MathJax.org maintains a list of currently supported $\LaTeX$ commands, and one can also check Dr. Carol JVF Burns's page of $\TeX$ Commands Available in MathJax.

13.  **Spaces** MathJax usually decides for itself how to space formulas, using a complex set of rules. Putting extra literal spaces into formulas will not change the amount of space MathJax puts in: `a␣b` and `a␣␣␣␣b` are both $ab$. To add more space, use `\,` for a thin space $a\,b$; `\;` for a wider space $a\;b$.  `\quad` and `\qquad` are large spaces: $a\quad b$, $a\quad b$.  
To set plain text, use `\text{…}`: 
$$\text{ \{ $x \in s$ | $x$ is extra large \} }.$$ 
You can nest `$…$ `inside of `\text{…}`.

14.  **Accents and diacritical marks** Use `\hat` for a single symbol $\hat{x}$ , `\widehat` for a larger formula $\widehat{xy}$. If you make it too wide, it will look silly. Similarly, there are `\bar` $\bar{x}$ and `\overline` $\overline{xyz}$ and `\vec`$\vec{x}$  and `\overrightarrow` $\overrightarrow{xy}$ and `\overleftrightarrow ` $\overleftrightarrow{xy}$. For dots, as in $\frac{d}{dx}x\dot{x}=\dot{x}^2+x\ddot{x}$, use `\dot` and `\ddot`.

15.  Special characters used for MathJax interpreting can be escaped using the `\` character: `\$ ``$`, `\{` `{`, `\_` `_`, etc. If you want `\` itself, you should use `\backslash` `∖`, because `\\` is for a new line.

(Tutorial ends here.)

----
 
It is important that this note be reasonably short and not suffer from too much bloat. To include more topics, please create short addenda and post them as answers instead of inserting them into this post.



## Matrices

Use `$$\begin{matrix}…\end{matrix}$$` In between the `\begin` and `\end`, put the matrix elements. End each matrix row with `\\`, and separate matrix elements with &. For example,

```
$$
    \begin{matrix}
    1 & x & x^2 \\
    1 & y & y^2 \\
    1 & z & z^2 \\
    \end{matrix}
$$
```

produces:


$$
    \begin{matrix}
    1 & x & x^2 \\
    1 & y & y^2 \\
    1 & z & z^2 \\
    \end{matrix}
$$

MathJax will adjust the sizes of the rows and columns so that everything fits.

To add brackets, either use \left…\right as in section 6 of the tutorial, or replace matrix with  `pmatrix ` (), `bmatrix` [], `Bmatrix` {}, `vmatrix` ∣∣, `Vmatrix` ‖‖.

Use `\cdots` ⋯ `\ddots` ⋱ `vdots` ⋮ when you want to omit some of the entries:

$$
\begin{pmatrix}
 1 & a_1 & a_1^2 & \cdots & a_1^n \\
 1 & a_2 & a_2^2 & \cdots & a_2^n \\
 \vdots  & \vdots& \vdots & \ddots & \vdots \\
 1 & a_m & a_m^2 & \cdots & a_m^n    
 \end{pmatrix}
 $$

For horizontally "augmented" matrices, put parentheses or brackets around a suitably-formatted table; see [arrays]() below for details. Here is an example:


$$ \left[
\begin{array}{cc|c}
  1&2&3\\
  4&5&6
\end{array}
\right] $$

is produced by:

```
$$ \left[
\begin{array}{cc|c}
  1&2&3\\
  4&5&6
\end{array}
\right] $$

```
The cc|c is the crucial part here; it says that there are three centered columns with a vertical bar between the second and third.

For vertically "augmented" matrices, use `\hline`. For example

$$
  \begin{pmatrix}
    a & b\\
    c & d\\
  \hline
    1 & 0\\
    0 & 1
  \end{pmatrix}
$$

is produced by

```
$$
  \begin{pmatrix}
    a & b\\
    c & d\\
  \hline
    1 & 0\\
    0 & 1
  \end{pmatrix}
$$
```

For small inline matrices use `\bigl(\begin{smallmatrix} ... \end{smallmatrix}\bigr)`, e.g. 

```
 $\bigl( \begin{smallmatrix} a & b \\ c & d \end{smallmatrix} \bigr)$
```



## Aligned equations

Often people want a series of equations where the equals signs are aligned. To get this, use `\begin{align}…\end{align}`. Each line should end with `\\`, and should contain an ampersand at the point to align at, typically immediately before the equals sign.

For example,

$$
\begin{align}
\sqrt{37} & = \sqrt{\frac{73^2-1}{12^2}} \\
 & = \sqrt{\frac{73^2}{12^2}\cdot\frac{73^2-1}{73^2}} \\ 
 & = \sqrt{\frac{73^2}{12^2}}\sqrt{\frac{73^2-1}{73^2}} \\
 & = \frac{73}{12}\sqrt{1 - \frac{1}{73^2}} \\ 
 & \approx \frac{73}{12}\left(1 - \frac{1}{2\cdot73^2}\right)
\end{align}
$$


is produced by

```
\begin{align}
\sqrt{37} & = \sqrt{\frac{73^2-1}{12^2}} \\
 & = \sqrt{\frac{73^2}{12^2}\cdot\frac{73^2-1}{73^2}} \\ 
 & = \sqrt{\frac{73^2}{12^2}}\sqrt{\frac{73^2-1}{73^2}} \\
 & = \frac{73}{12}\sqrt{1 - \frac{1}{73^2}} \\ 
 & \approx \frac{73}{12}\left(1 - \frac{1}{2\cdot73^2}\right)
\end{align}
```

The usual `$$` marks that delimit the display may be omitted here.


## Symbols

In general, you have to search in long tables about a specific symbol you're looking for, things like $\Psi$, $\delta$, $\zeta$, $\ge$, $\subseteq$ ... And it turns out that this operation can be frustrating and time consuming, which can cause the buddy to abandon writing the complete $\LaTeX$ sentence in his answer, or in some cases, the complete answer itself.

That's why the tool that I will present you in this post was conceived. Basically, it is a $\LaTeX$ handwritten symbol recognition. Example in image:

enter image description here

Here is the website: Detexify² No more frustration.



## Definitions by cases (piecewise functions)

Use `\begin{cases}…\end{cases}`. End each case with a `\\`, and use & before parts that should be aligned.

For example, you get this:

$$
  f(n) =
\begin{cases}
n/2,  & \text{if $n$ is even} \\
3n+1, & \text{if $n$ is odd}
\end{cases}
$$

by writing this:

```
f(n) =
\begin{cases}
n/2,  & \text{if $n$ is even} \\
3n+1, & \text{if $n$ is odd}
\end{cases}
```

The brace can be moved to the right:

$$
\left.
\begin{array}{l}
\text{if $n$ is even:}&n/2\\
\text{if $n$ is odd:}&3n+1
\end{array}
\right\}
=f(n)
$$

by writing this:

```
\left.
\begin{array}{l}
\text{if $n$ is even:}&n/2\\
\text{if $n$ is odd:}&3n+1
\end{array}
\right\}
=f(n)
```

To get a larger vertical space between cases we can use `\\[2ex]` instead of `\\`. For example, you get this:

$$
f(n) =
\begin{cases}
\frac{n}{2},  & \text{if $n$ is even} \\[2ex]
3n+1, & \text{if $n$ is odd}
\end{cases}
$$


by writing this:

```
f(n) =
\begin{cases}
\frac{n}{2},  & \text{if $n$ is even} \\[2ex]
3n+1, & \text{if $n$ is odd}
\end{cases}
```

(An ‘ex’ is a length equal to the height of the letter x; 2ex here means the space should be two exes high.)



## Arrays

It is often easier to read tables formatted in MathJax rather than plain text or a fixed width font. Arrays and tables are created with the array environment. Just after `\begin{array}` the format of each column should be listed, use `c` for a center aligned column, `r` for right aligned, `l` for left aligned and a `|` for a vertical line. Just as with matrices, cells are separated with & and rows are broken using `\\.` A horizontal line spanning the array can be placed before the current line with \hline.

For example,

$$
\begin{array}{c|lcr}
n & \text{Left} & \text{Center} & \text{Right} \\
\hline
1 & 0.24 & 1 & 125 \\
2 & -1 & 189 & -8 \\
3 & -20 & 2000 & 1+10i
\end{array}
$$

```
$$
\begin{array}{c|lcr}
n & \text{Left} & \text{Center} & \text{Right} \\
\hline
1 & 0.24 & 1 & 125 \\
2 & -1 & 189 & -8 \\
3 & -20 & 2000 & 1+10i
\end{array}
$$
```

Arrays can be nested to make an array of tables.

For example,

$$
% outer vertical array of arrays
\begin{array}{c}
% inner horizontal array of arrays
\begin{array}{cc}
% inner array of minimum values
\begin{array}{c|cccc}
\text{min} & 0 & 1 & 2 & 3\\
\hline
0 & 0 & 0 & 0 & 0\\
1 & 0 & 1 & 1 & 1\\
2 & 0 & 1 & 2 & 2\\
3 & 0 & 1 & 2 & 3
\end{array}
&
% inner array of maximum values
\begin{array}{c|cccc}
\text{max}&0&1&2&3\\
\hline
0 & 0 & 1 & 2 & 3\\
1 & 1 & 1 & 2 & 3\\
2 & 2 & 2 & 2 & 3\\
3 & 3 & 3 & 3 & 3
\end{array}
\end{array}
\\
% inner array of delta values
\begin{array}{c|cccc}
\Delta&0&1&2&3\\
\hline
0 & 0 & 1 & 2 & 3\\
1 & 1 & 0 & 1 & 2\\
2 & 2 & 1 & 0 & 1\\
3 & 3 & 2 & 1 & 0
\end{array}
\end{array}
$$



## Fussy spacing issues
These are issues that won't affect the correctness of formulas, but might make them look significantly better or worse. Beginners should feel free to ignore this advice; someone else will correct it for them, or more likely nobody will care.

Don't use `\frac` in exponents or limits of integrals; it looks bad and can be confusing, which is why it is rarely done in professional mathematical typesetting. Write the fraction horizontally, with a slash:

$$
\begin{array}{cc}
\mathrm{Bad} & \mathrm{Better} \\
\hline \\
e^{i\frac{\pi}2} \quad e^{\frac{i\pi}2}& e^{i\pi/2} \\
\int_{-\frac\pi2}^\frac\pi2 \sin x\,dx & \int_{-\pi/2}^{\pi/2}\sin x\,dx \\
\end{array}
$$

```
\begin{array}{cc}
\mathrm{Bad} & \mathrm{Better} \\
\hline \\
e^{i\frac{\pi}2} \quad e^{\frac{i\pi}2}& e^{i\pi/2} \\
\int_{-\frac\pi2}^\frac\pi2 \sin x\,dx & \int_{-\pi/2}^{\pi/2}\sin x\,dx \\
\end{array}
```

The `|` symbol has the wrong spacing when it is used as a divider, for example in set comprehensions. Use `\mid` instead:

$$
\begin{array}{cc}
\mathrm{Bad} & \mathrm{Better} \\
\hline \\
\{x|x^2\in\Bbb Z\} & \{x\mid x^2\in\Bbb Z\} \\
\end{array}
$$

```
\begin{array}{cc}
\mathrm{Bad} & \mathrm{Better} \\
\hline \\
\{x|x^2\in\Bbb Z\} & \{x\mid x^2\in\Bbb Z\} \\
\end{array}
```

For double and triple integrals, don't use `\int\int` or `\int\int\int`. Instead use the special forms `\iint` and `\iiint`:

$$
\begin{array}{cc}
\mathrm{Bad} & \mathrm{Better} \\
\hline \\
\int\int_S f(x)\,dy\,dx & \iint_S f(x)\,dy\,dx \\
\int\int\int_V f(x)\,dz\,dy\,dx & \iiint_V f(x)\,dz\,dy\,dx
\end{array}
$$

```
\begin{array}{cc}
\mathrm{Bad} & \mathrm{Better} \\
\hline \\
\int\int_S f(x)\,dy\,dx & \iint_S f(x)\,dy\,dx \\
\int\int\int_V f(x)\,dz\,dy\,dx & \iiint_V f(x)\,dz\,dy\,dx
\end{array}
```



Use `\`, to insert a thin space before differentials; without this $\TeX$ will mash them together:

$$
\begin{array}{cc}
\mathrm{Bad} & \mathrm{Better} \\
\hline \\
\iiint_V f(x)dz dy dx & \iiint_V f(x)\,dz\,dy\,dx
\end{array}
$$

```
\begin{array}{cc}
\mathrm{Bad} & \mathrm{Better} \\
\hline \\
\iiint_V f(x)dz dy dx & \iiint_V f(x)\,dz\,dy\,dx
\end{array}
```

 - Worth nothing you can use` \middle` with `|` to get it to work with `\left` and `\right`, like `\left\{x\middle | \frac{x^2}{2} \in \mathbb{z}\right\}`: $\left\{x\middle | \frac{x^2}{2} \in \mathbb{z}\right\}$

 - I always use `\left\{\, ... \,\middle|\, ... \,\right\}` like in $\left\{\,x\in\Bbb R\,\middle|\, \frac{x^2}{2}\in\Bbb Z\,\right\}$.



## Crossing things out
Use `\require{cancel}` in the first formula in your post that requires cancelling; you need it only once per page. Then use:

```
\require{cancel}
\begin{array}{rl}
\verb|y+\cancel{x}| & y+\cancel{x}\\
\verb|\cancel{y+x}| & \cancel{y+x}\\
\verb|y+\bcancel{x}| & y+\bcancel{x}\\
\verb|y+\xcancel{x}| & y+\xcancel{x}\\
\verb|y+\cancelto{0}{x}| & y+\cancelto{0}{x}\\
\verb+\frac{1\cancel9}{\cancel95} = \frac15+& \frac{1\cancel9}{\cancel95} = \frac15 \\
\end{array}
```
Use `\require{enclose}` for the following:

```
\require{enclose}\begin{array}{rl}
\verb|\enclose{horizontalstrike}{x+y}| & \enclose{horizontalstrike}{x+y}\\
\verb|\enclose{verticalstrike}{\frac xy}| & \enclose{verticalstrike}{\frac xy}\\
\verb|\enclose{updiagonalstrike}{x+y}| & \enclose{updiagonalstrike}{x+y}\\
\verb|\enclose{downdiagonalstrike}{x+y}| & \enclose{downdiagonalstrike}{x+y}\\
\verb|\enclose{horizontalstrike,updiagonalstrike}{x+y}| & \enclose{horizontalstrike,updiagonalstrike}{x+y}\\
\end{array}
```

`\enclose` can also produce enclosing boxes, circles, and other notations; see [MathML]() menclose documentation for a complete list.



## System of equations
Use `\begin{array}…\end{array}` and `\left\{…\right`.. For example, you get this:

$$
\left\{ 
\begin{array}{c}
a_1x+b_1y+c_1z=d_1 \\ 
a_2x+b_2y+c_2z=d_2 \\ 
a_3x+b_3y+c_3z=d_3
\end{array}
\right. 
$$

by writing this:

```
$$
\left\{ 
\begin{array}{c}
a_1x+b_1y+c_1z=d_1 \\ 
a_2x+b_2y+c_2z=d_2 \\ 
a_3x+b_3y+c_3z=d_3
\end{array}
\right. 
$$
```

Alternatively we can use \begin{cases}…\end{cases}. The same system

$$\begin{cases}
a_1x+b_1y+c_1z=d_1 \\ 
a_2x+b_2y+c_2z=d_2 \\ 
a_3x+b_3y+c_3z=d_3
\end{cases}
$$

is produced by the following code
```
$$\begin{cases}
a_1x+b_1y+c_1z=d_1 \\ 
a_2x+b_2y+c_2z=d_2 \\ 
a_3x+b_3y+c_3z=d_3
\end{cases}
$$
```

To align the `=` signs use `\begin{aligned}...\end{aligned}` and `\left\{…\right`. 

$$
\left\{
\begin{aligned} 
a_1x+b_1y+c_1z &=d_1+e_1 \\ 
a_2x+b_2y&=d_2 \\ 
a_3x+b_3y+c_3z &=d_3 
\end{aligned} 
\right. 
$$

whose code is
```
$$
\left\{
\begin{aligned} 
a_1x+b_1y+c_1z &=d_1+e_1 \\ 
a_2x+b_2y&=d_2 \\ 
a_3x+b_3y+c_3z &=d_3 
\end{aligned} 
\right. 
$$
```

To align the `=` signs and the terms as in

$$
\left\{
\begin{array}{ll}
a_1x+b_1y+c_1z &=d_1+e_1 \\ 
a_2x+b_2y &=d_2 \\ 
a_3x+b_3y+c_3z &=d_3 
\end{array} 
\right.
$$

use array with `l` (for "align left"; there are also `c` and `r`) parameters
```
$$
\left\{
\begin{array}{ll}
a_1x+b_1y+c_1z &=d_1+e_1 \\ 
a_2x+b_2y &=d_2 \\ 
a_3x+b_3y+c_3z &=d_3 
\end{array} 
\right.
$$
```

Vertical space between equations. As explained in Definition by cases to get a larger vertical space between equations we can use `\\[2ex]` instead of `\\`. The system

$$\begin{cases}
a_1x+b_1y+c_1z=d_1 \\[2ex] 
a_2x+b_2y+c_2z=d_2 \\[2ex] 
a_3x+b_3y+c_3z=d_3
\end{cases}
$$

is generated by the following code

```
$$\begin{cases}
a_1x+b_1y+c_1z=d_1 \\[2ex] 
a_2x+b_2y+c_2z=d_2 \\[2ex] 
a_3x+b_3y+c_3z=d_3
\end{cases}
$$
```

in comparison with

$$\begin{cases}
a_1x+b_1y+c_1z=\frac{p_1}{q_1} \\
a_2x+b_2y+c_2z=\frac{p_2}{q_2} \\
a_3x+b_3y+c_3z=\frac{p_3}{q_3}
\end{cases}
$$

whose code is

```
$$\begin{cases}
a_1x+b_1y+c_1z=\frac{p_1}{q_1} \\
a_2x+b_2y+c_2z=\frac{p_2}{q_2} \\
a_3x+b_3y+c_3z=\frac{p_3}{q_3}
\end{cases}
$$
```

In response to elect's comment. The following code

```
$$ \left\{ \begin{array}{l}
0 = c_x-a_{x0}-d_{x0}\dfrac{(c_x-a_{x0})\cdot d_{x0}}{\|d_{x0}\|^2} + c_x-a_{x1}-d_{x1}\dfrac{(c_x-a_{x1})\cdot d_{x1}}{\|d_{x1}\|^2} \\[2ex] 
0 = c_y-a_{y0}-d_{y0}\dfrac{(c_y-a_{y0})\cdot d_{y0}}{\|d_{y0}\|^2} + c_y-a_{y1}-d_{y1}\dfrac{(c_y-a_{y1})\cdot d_{y1}}{\|d_{y1}\|^2} \end{array} \right. 
$$
```

produces

$$ \left\{ \begin{array}{l}
0 = c_x-a_{x0}-d_{x0}\dfrac{(c_x-a_{x0})\cdot d_{x0}}{\|d_{x0}\|^2} + c_x-a_{x1}-d_{x1}\dfrac{(c_x-a_{x1})\cdot d_{x1}}{\|d_{x1}\|^2} \\[2ex] 
0 = c_y-a_{y0}-d_{y0}\dfrac{(c_y-a_{y0})\cdot d_{y0}}{\|d_{y0}\|^2} + c_y-a_{y1}-d_{y1}\dfrac{(c_y-a_{y1})\cdot d_{y1}}{\|d_{y1}\|^2} \end{array} \right. 
$$


## Colors
Named colors are browser-dependent; if a browser doesn't know a particular color name, it may render the text as black. The following colors are standard in HTML4 and CSS2 and should be interpreted the same by most browsers:

$$
\begin{array}{|rc|}
\hline
\verb+\color{black}{text}+ & \color{black}{text} \\
\verb+\color{gray}{text}+ & \color{gray}{text} \\
\verb+\color{silver}{text}+ & \color{silver}{text} \\
\verb+\color{white}{text}+ & \color{white}{text} \\
\hline
\verb+\color{maroon}{text}+ & \color{maroon}{text} \\
\verb+\color{red}{text}+ & \color{red}{text} \\
\verb+\color{yellow}{text}+ & \color{yellow}{text} \\
\verb+\color{lime}{text}+ & \color{lime}{text} \\
\verb+\color{olive}{text}+ & \color{olive}{text} \\
\verb+\color{green}{text}+ & \color{green}{text} \\
\verb+\color{teal}{text}+ & \color{teal}{text} \\
\verb+\color{aqua}{text}+ & \color{aqua}{text} \\
\verb+\color{blue}{text}+ & \color{blue}{text} \\
\verb+\color{navy}{text}+ & \color{navy}{text} \\
\verb+\color{purple}{text}+ & \color{purple}{text} \\ 
\verb+\color{fuchsia}{text}+ & \color{magenta}{text} \\
\hline
\end{array}
$$


HTML5 and CSS 3 define an additional 124 color names that will be supported on many browsers.

Math Stack Exchange's default style uses a light-colored page background, so avoid using light colors for text. Stick to darker colors like maroon, green, blue, and purple, and remember also that 7–10% of men are color-blind and have difficulty distinguishing red and green.

The color may also have the form `#rgb` where 𝑟,𝑔,𝑏 are in the range or 0–9, a–f and represent the intensity of red, green, and blue on a scale of 0–15, with a=10, b=11, … f=15. For example:

$$
\begin{array}{|rrrrrrrr|}\hline
\verb+#000+ & \color{#000}{text} & & &
\verb+#00F+ & \color{#00F}{text} & & \\
& & \verb+#0F0+ & \color{#0F0}{text} &
& & \verb+#0FF+ & \color{#0FF}{text}\\
\verb+#F00+ & \color{#F00}{text} & & &
\verb+#F0F+ & \color{#F0F}{text} & & \\
& & \verb+#FF0+ & \color{#FF0}{text} &
& & \verb+#FFF+ & \color{#FFF}{text}\\
\hline
\end{array}
$$

$$
\begin{array}{|rrrrrrrr|}
\hline
\verb+#000+ & \color{#000}{text} & \verb+#005+ & \color{#005}{text} & \verb+#00A+ & \color{#00A}{text} & \verb+#00F+ & \color{#00F}{text}  \\
\verb+#500+ & \color{#500}{text} & \verb+#505+ & \color{#505}{text} & \verb+#50A+ & \color{#50A}{text} & \verb+#50F+ & \color{#50F}{text}  \\
\verb+#A00+ & \color{#A00}{text} & \verb+#A05+ & \color{#A05}{text} & \verb+#A0A+ & \color{#A0A}{text} & \verb+#A0F+ & \color{#A0F}{text}  \\
\verb+#F00+ & \color{#F00}{text} & \verb+#F05+ & \color{#F05}{text} & \verb+#F0A+ & \color{#F0A}{text} & \verb+#F0F+ & \color{#F0F}{text}  \\
\hline
\verb+#080+ & \color{#080}{text} & \verb+#085+ & \color{#085}{text} & \verb+#08A+ & \color{#08A}{text} & \verb+#08F+ & \color{#08F}{text}  \\
\verb+#580+ & \color{#580}{text} & \verb+#585+ & \color{#585}{text} & \verb+#58A+ & \color{#58A}{text} & \verb+#58F+ & \color{#58F}{text}  \\
\verb+#A80+ & \color{#A80}{text} & \verb+#A85+ & \color{#A85}{text} & \verb+#A8A+ & \color{#A8A}{text} & \verb+#A8F+ & \color{#A8F}{text}  \\
\verb+#F80+ & \color{#F80}{text} & \verb+#F85+ & \color{#F85}{text} & \verb+#F8A+ & \color{#F8A}{text} & \verb+#F8F+ & \color{#F8F}{text}  \\
\hline
\verb+#0F0+ & \color{#0F0}{text} & \verb+#0F5+ & \color{#0F5}{text} & \verb+#0FA+ & \color{#0FA}{text} & \verb+#0FF+ & \color{#0FF}{text}  \\
\verb+#5F0+ & \color{#5F0}{text} & \verb+#5F5+ & \color{#5F5}{text} & \verb+#5FA+ & \color{#5FA}{text} & \verb+#5FF+ & \color{#5FF}{text}  \\
\verb+#AF0+ & \color{#AF0}{text} & \verb+#AF5+ & \color{#AF5}{text} & \verb+#AFA+ & \color{#AFA}{text} & \verb+#AFF+ & \color{#AFF}{text}  \\
\verb+#FF0+ & \color{#FF0}{text} & \verb+#FF5+ & \color{#FF5}{text} & \verb+#FFA+ & \color{#FFA}{text} & \verb+#FFF+ & \color{#FFF}{text}  \\
\hline
\end{array}
$$

You can have a look here for quick reference on colors in HTML.


## Additional decorations

- `\overline`
- `\underline`
- `\widetilde`
- `\widehat`
- `\fbox` or `\boxed` 
$$ \fbox {$EE$}$$ 
$$\boxed{EEE}$$
- `\underleftarrow`
- `\underrightarrow`
- `\underleftrightarrow`
- `\overbrace` 
$$
\overbrace{(n - 2) + \overbrace{(n - 1) + n + (n + 1)} + (n + 2)}
$$
- `\underbrace` 
- `\overbrace` and `\underbrace` accept a superscript or a subscript, respectively, to annotate the brace. For example,` \underbrace{a\cdot a\cdots a}_{b\text{ times}}` is
$$
\underbrace{a\cdot a\cdots a}_{b\text{ times}}
$$

Note: `\varliminf` and` \varlimsup` have special symbol of their own.

## Single character accents
- `\check`
- `\acute `
- `\grave`
- `\vec`
- `\bar`
- `\hat` 
- `\tilde` 
- `\dot \ddot \dddot`
- `\mathring`

## General stacking
If you cannot find your symbol remember that you can stack various symbols using 
`\overset{above}{below}` 

$$
\overset{@}{ABC}\ \overset{x^2}{\longmapsto}\ \overset{\bullet\circ\circ\bullet}{T}
$$


## Commutative diagrams
AMScd diagrams must start with a "require":

```
$$
$\require{AMScd}$
\begin{CD}
    A @>a>> B\\
    @V b V V= @VV c V\\
    C @>>d> D
\end{CD}
$$
```

$$
$\require{AMScd}$
\begin{CD}
    A @>a>> B\\
    @V b V V= @VV c V\\
    C @>>d> D
\end{CD}
$$

to get this diagram: 



- `@>>>` is used for arrow right
- `@<<<` is used for arrow left
- `@VVV` is used for arrow down
- `@AAA` is used for arrow up is used for horizontal double line
- `@|` is used for vertical double line
- `@.` is used for no arrow

Another example:
```
\begin{CD}
    A @>>> B @>{\text{very long label}}>> C \\
    @. @AAA @| \\
    D @= E @<<< F
\end{CD}
```

$$
\begin{CD}
    A @>>> B @>{\text{very long label}}>> C \\
    @. @AAA @| \\
    D @= E @<<< F
\end{CD}
$$

Long labels increase the length of the arrow and in this version also automatically increase corresponding arrows.

```
$\require{AMScd}$
\begin{CD}
      RCOHR'SO_3Na @>{\text{Hydrolysis,$\Delta, Dil.HCl$}}>> (RCOR')+NaCl+SO_2+ H_2O 
\end{CD}
```

$$
$\require{AMScd}$
\begin{CD}
      RCOHR'SO_3Na @>{\text{Hydrolysis,$\Delta, Dil.HCl$}}>> (RCOR')+NaCl+SO_2+ H_2O 
\end{CD}
$$

## Continued fractions

To make a continued fraction, use `\cfrac`, which works just like `\frac` but typesets the results differently:

$$
x = a_0 + \cfrac{1^2}{a_1
          + \cfrac{2^2}{a_2
          + \cfrac{3^2}{a_3 + \cfrac{4^4}{a_4 + \cdots}}}}
$$

Don't use regular `\frac` or `\over`, or it will look awful:

$$
x = a_0 + \frac{1^2}{a_1
          + \frac{2^2}{a_2
          + \frac{3^2}{a_3 + \frac{4^4}{a_4 + \cdots}}}}
$$

You can of course use `\frac` for the compact notation:

$$
x = a_0 + \frac{1^2}{a_1+}
          \frac{2^2}{a_2+}
          \frac{3^2}{a_3 +} \frac{4^4}{a_4 +} \cdots
$$

Continued fractions are too big to put inline. Display them with `$$…$$` or use a notation like 
$[a_0; a_1, a_2, a_3, \ldots]$.

- $$\underset{j=1}{\overset{\infty}{\LARGE\mathrm K}}\frac{a_j}{b_j}=\cfrac{a_1}{b_1+\cfrac{a_2}{b_2+\cfrac{a_3}{b_3+\ddots}}}$$
- $$\cfrac{a_{1}}{b_{1}+\cfrac{a_{2}}{b_{2}+\cfrac{a_{3}}{b_{3}+\ddots }}}=   {\genfrac{}{}{}{}{a_1}{b_1}}   {\genfrac{}{}{0pt}{}{}{+}}   {\genfrac{}{}{}{}{a_2}{b_2}}   {\genfrac{}{}{0pt}{}{}{+}}   {\genfrac{}{}{}{}{a_3}{b_3}}   {\genfrac{}{}{0pt}{}{}{+\dots}}$$



## Using `\newcommand`
I would like to remark that it is possible to define LaTeX commands as you do in your TeX files. I felt so happy when I first discovered it! It's enough to insert something like


```
$ \newcommand{\SES}[3]{ 0 \to #1 \to #2 \to #3 \to 0 } $
```

 at the top of your post (remember the dollars!). Then you can just use your commands as you are used to do: in my example typing  `$$ \SES{A}{B}{C} $$` will produce the following:
 

$\newcommand{\SES}[3]{ 0 \to #1 \to #2 \to #3 \to 0 }
\ses{A}{B}{C}$

```
$\newcommand{\SES}[3]{ 0 \to #1 \to #2 \to #3 \to 0 }
\ses{A}{B}{C}$
```

It's also possible to use plain `\def`:

```
\def\ses#1#2#3{0 \to #1 \to #2 \to #3 \to 0}
```
$\def\ses#1#2#3{0 \to #1 \to #2 \to #3 \to 0}
\ses{A}{B}{C}$

```
$\def\ses#1#2#3{0 \to #1 \to #2 \to #3 \to 0}
\ses{A}{B}{C}$
```

and then `$\ses{A}{B}{C}$` will produce the same output.



## Tags & References
For longer calculations (or referring to other post's results) it is convenient to use the tagging/labelling/referencing system. To tag an equation use `\tag{yourtag}`, and if you want to refer to that tag later on, add `\label{somelabel}` right after the `\tag`. It is not necessary that yourtag and somelabel are the same, but it usually is more convenient to do so:

$$ a := x^2-y^3 \tag{*}\label{*} $$

```
$$ a := x^2-y^3 \tag{*}\label{*} $$
```

In order to refer to an equation, just use `\eqref{somelabel}` 

$$ a+y^3 \stackrel{\eqref{*}}= x^2 $$

```
$$ a+y^3 \stackrel{\eqref{*}}= x^2 $$
```

or `\ref{somelabel}`

Equations are usually referred to as $\eqref{*}$(`$\eqref{*}$`), but you can also use $\ref{*}$(`$\ref{*}$`).
Equations are usually referred to as `(*)`, but you can also use `*`.

As you can see, references are even turned into hyperlinks, which you can use externally as well, e.g. like this. Note that you can also reference labels in other posts as long as they appear on the same site, which is especially useful when referring to a question with multiple equations, or when commenting on a post.

Due to a bug blocks containing a `\label` will break in preview, as a workaround you can put `$\def\label#1{}$` in your post while editing and remove that on submission - unfortunately this means you won't spot misspelled references before submitting... Just don't forget to remove that `\def` again



- `\implies` ($\implies$) is a marginally preferable alternative to `\Rightarrow` ($\Rightarrow$) for implication.

- There's also `\iff` $\iff$ and `\impliedby` $\impliedby$.

- `\to` ($\to$) is preferable to `\rightarrow` or `\longrightarrow` for things like $f\colon A \to B$. The reverse is `\gets` ($\gets$).


## Big braces
Use `\left` and `\right` to make braces - (round), [square] and {curly} - scale up to be the size of their arguments. Thus
```
$$
f\left(
   \left[ 
     \frac{
       1+\left\{x,y\right\}
     }{
       \left(
          \frac{x}{y}+\frac{y}{x}
       \right)
       \left(u+1\right)
     }+a
   \right]^{3/2}
\right)
$$
```

renders as

$$
f\left(
   \left[ 
     \frac{
       1+\left\{x,y\right\}
     }{
       \left(
          \frac{x}{y}+\frac{y}{x}
       \right)
       \left(u+1\right)
     }+a
   \right]^{3/2}
\right)
$$
.
Note that curly braces need to be escaped as `\{` `\}`.

If you start a big brace with `\left` and then need to match that to a `\right` brace that's on a different line, use the forms `\right.` and `\left.` to make "shadow" braces. Thus,
```
$$
\begin{aligned}
a=&\left(1+2+3+  \cdots \right. \\
& \cdots+ \left. \infty-2+\infty-1+\infty\right)
\end{aligned}
$$
```

renders as
$$
\begin{aligned}
a=&\left(1+2+3+  \cdots \right. \\
& \cdots+ \left. \infty-2+\infty-1+\infty\right)
\end{aligned}.
$$

There is also a `\middle` construct which is useful when one has a mid-expression brace which must also scale up:

```
$$
\left\langle  
  q
\middle\|
  \frac{\frac{x}{y}}{\frac{u}{v}}
\middle| 
   p 
\right\rangle
$$
```

renders as

$$
\left\langle  
  q
\middle\|
  \frac{\frac{x}{y}}{\frac{u}{v}}
\middle| 
   p 
\right\rangle
$$

-  Note that constructs like `\left\langle`, `\left|` and `\left\|` are also possible.

- Note: `\Big( ... \Big)` produces `(…)` but this bracket size is fixed in all situations unlike `\left( ... \right)` which varies in size with its contents. `\Big` can be useful in various situations.



## Limits
To make a limit (like l$\lim\limits_{x \to 1} \frac{x^2-1}{x-1}$), use this syntax: 

First, start off with `$\lim`. This renders as $\lim$. The backslash is there to prevent things like $lim$, where the letters are slanted. 

Second, add `\limits_{x \to 1}` inside. The code now looks like `$\lim \limits_{x \to 1}$`, and renders as $\lim \limits_{x \to 1}$. The `\to` inside makes the right arrow, rendered as $\to$. The `_` makes the $x \to 1$ go underneath the $\lim$. Finally, the pair of curly braces `{ }` makes sure that $x \to 1$ is treated as a whole object, and not two separate things. 

Lastly, add the function you want to apply the limit to. To make the limit mentioned above, $\lim\limits_{x \to 1} \frac{x^2-1}{x-1}$, simply use `$\lim\limits_{x \to 1} \frac{x^2-1}{x-1}$`. 

And that is how you make a limit using MathJax.



## Arbitrary operators
If an operator is not available as a built-in command, use `\operatorname{…}`. So for things like
$$\operatorname{arsinh(𝑥)}$$
write `\operatorname{arsinh}(x)` since `\arsinh(x)` will give an error and `arsinh(x)` has wrong font and spacing: $\operatorname{arsinh}(x)$.

This was already mentioned in a comment by Charles Staats. You might consider this an addition to the FAQ section on `\lim,` `\sin` and so on.

For operators which need limits above and below the operator, use `\operatorname*{…}`, as in
$$
\operatorname*{Res}_{z=1}\left(\frac1{z^2-z}\right)=1
$$


## Highlighting equation
To highlight an equation, `\bbox` can be used. E.g,


$$ \bbox[yellow]
{
e^x=\lim_{n\to\infty} \left( 1+\frac{x}{n} \right)^n
\qquad (1)
}
$$

```
$$ \bbox[yellow]
{
e^x=\lim_{n\to\infty} \left( 1+\frac{x}{n} \right)^n
\qquad (1)
}
$$
```




By default, the bounding box is "tight", so it doesn't extend beyond the characters used in the formula. You can add a little space around the equation by adding a measurement after the color. E.g.,

$$ \bbox[yellow,5px]
{
e^x=\lim_{n\to\infty} \left( 1+\frac{x}{n} \right)^n
\qquad (1)
}
$$

```
$$ \bbox[yellow,5px]
{
e^x=\lim_{n\to\infty} \left( 1+\frac{x}{n} \right)^n
\qquad (1)
}
$$
```




To add a border, use

```
$$ \bbox[5px,border:2px solid red]
{
e^x=\lim_{n\to\infty} \left( 1+\frac{x}{n} \right)^n
\qquad (2) 
}
$$
```

$$ \bbox[5px,border:2px solid red]
{
e^x=\lim_{n\to\infty} \left( 1+\frac{x}{n} \right)^n
\qquad (2) 
}
$$



You can do both border and background, as well:

```
$$ \bbox[yellow,5px,border:2px solid red]
{
e^x=\lim_{n\to\infty} \left( 1+\frac{x}{n} \right)^n
\qquad (1)
}
$$
```

$$ \bbox[yellow,5px,border:2px solid red]
{
e^x=\lim_{n\to\infty} \left( 1+\frac{x}{n} \right)^n
\qquad (1)
}
$$



## Absolute values and norms
The absolute value of some expression can be denoted as `\lvert x\rvert` or, more generally, as `\left\lvert … \right\rvert`. It renders as $\left\lvert x \right\rvert$.

The norm of a vector (or similar) can be denoted as `\lVert v\rVert` or, more generally, as `\left\lVert … \right\rVert`. It renders as $\left\lVert v \right\rVert$. (You may also write `\left\|…\right\|` instead.)

In both cases, the rendering is better than what you'd get from `|x|` or `||v||`, which render with bars that don't descend low enough and sub-optimal spacing. At least on some browsers, so here is a screenshot how it looks for me, using Firefox 31 on OS X:



And here is the same formula rendered by your browser:$$|x|, ||v|| \quad\longrightarrow\quad \lvert x\rvert, \lVert v\rVert$$
It was typeset as
```
$$|x|, ||v|| \quad\longrightarrow\quad \lvert x\rvert, \lVert v\rVert$$
```



## Giving reasons on each line of a sequence of equations
To produce this:

$$
\begin{align}
   v + w & = 0  &&\text{Given} \tag 1\\
   -w & = -w + 0 && \text{additive identity} \tag 2\\
   -w + 0 & = -w + (v + w) && \text{equations $(1)$ and $(2)$}
\end{align}
$$

write this:
```
\begin{align}
   v + w & = 0  &&\text{Given} \tag 1\\
   -w & = -w + 0 && \text{additive identity} \tag 2\\
   -w + 0 & = -w + (v + w) && \text{equations $(1)$ and $(2)$}
\end{align}
```



## Pack of cards
If you are asking (or answering) a combinatorics question involving packs of cards you can make it look more elegant by using `\spadesuit`, `\heartsuit`, `\diamondsuit`, `\clubsuit` in math mode:
$$\spadesuit\quad\heartsuit\quad\diamondsuit\quad\clubsuit$$
Or if you're really fussy:
`\color{red}{\heartsuit}` and `\color{red}{\diamondsuit}`
$$\color{red}{\heartsuit}\quad\color{red}{\diamondsuit}$$
You can also enter the standard Unicode characters (U+2660 BLACK SPADE SUIT etc.) literally.




## Left and Right Implication Arrows
Another way to display the arrows for right and left implication instead of using

`$\Rightarrow$`, `$\Leftarrow$` and `$\Leftrightarrow$`

which produces $\Rightarrow$, $\Leftarrow$ and $\Leftrightarrow$ respectively, you can use

`$\implies$` for ⟹, `$\impliedby$` for ⟸ and `$\iff$` for ⟺
The latter of which produces longer arrows which may be more desirable to some.


### Long division
```
$$
\require{enclose}
\begin{array}{r}
                13  \\[-3pt]
4 \enclose{longdiv}{52} \\[-3pt]
     \underline{4}\phantom{2} \\[-3pt]
                12  \\[-3pt]
     \underline{12}
\end{array}
$$
```
One important trick shown here is the use of `\phantom{2}` to make a blank space that is the same size and shape as the digit `2` just above it.

This is adapted from https://stackoverflow.com/a/22871404/3466415 (which uses slightly different but not less valid formatting).


$$x^3−6x^2+11x−6=(x−{\color{red}1})(x^2−5x+6)+{\color{blue}0}$$

$$\begin{array}{c|rrrr}& x^3 & x^2 & x^1 &  x^0\\ & 1 & -6 & 11 & -6\\ {\color{red}1} & \downarrow & 1 & -5 & 6\\ \hline & 1 & -5 & 6 & |\phantom{-} {\color{blue}0} \end{array}$$
$$\dfrac{x^3-6x^2+11x-6}{x-1}=x^2-5x+6$$
$$\begin{array}{rrrr|ll} x^3 & -6x^2 & +11x & -6   & x  -  1  \\   -x^3 & +x^2 &  &  &   x^2-5x+6 \\ \hline     & -5x^2 & +11x & -6\\ & \phantom{-}5x^2 & -5x & & & & \\ \hline  & & +6x & -6 \\ & & -6x & +6 \\ \hline & &  0 & 0 \end{array}$$


## Degree symbol
Standard Mathjax does not yet support a dedicated degree symbol, so here are some of the ways to try and emulate one :

```tex
$$
\begin{array} \\
\text{$45^\text{o}$} & \text{renders as} & 45^\text{o} \\
\text{45^o} & \text{renders as} & 45^o \\
\text{45^\circ} & \text{renders as} & 45^\circ \\
\text{90°} & \text{renders as} & 90° & \text{Using keyboard entry of symbol}
\end{array}
$$
```

The degree symbol for angles is not `^\circ`. Although many people use this notation, the result looks quite different from the canonical degree symbol shipped with the font, as seen above.

If your keyboard doesn't have a `°` key, feel free to copy from this post here, or follow these suggestions.

Note that comments below indicate that on some configurations at least, `°` renders inferior to `^\circ`. And I recently had a post of mine edited just for the sake of turning `°` into `^\circ`, indicating that someone felt rather strongly about this. So the suggestion above does seem somewhat controversial at the moment. I maintain that from a semantic point of view, `°` is superior to `^\circ`, and if the rendering suffers from this, then it's a bug in MathJax. After all, LaTeX offers a proper degree symbol in the tex companion fonts, indicating that someone there, too, decided that ^`\circ` is not perfect. But if things are broken now, I can't fault people from pragmatically sticking with the rendering they prefer. Personally I prefer semantics, also for the sake of screen readers.

#### Accessibility

Aside from appearance, one consideration in choosing which notation to use is how it will get parsed by screen readers. For example, ChromeVox reads both 4`5^\circ` and `45°` as "forty-five degrees", while the other two are pronounced as "forty-five oh", which may be a reason to avoid them.

#### Usepackage

Commonly in Latex you can `\usepackage{gensymb}` to get the `\degree` symbol, however on Stack Exchange this is not an option. Note that even if you can do this it will typically affect the entire page, which may have side effects for other users. So don't rely on this approach.



## Displaystyle and Textstyle
Many things like fractions, sums, limits, and integrals display differently when written inline versus in a displayed formula. You can switch styles back and forth with \displaystyle and \textstyle in order to achieve the desired appearance.

Here's an example switching back and forth in a displayed equation:

```
$$\sum_{n=1}^\infty \frac{1}{n^2} \to
  \textstyle \sum_{n=1}^\infty \frac{1}{n^2} \to
  \displaystyle \sum_{n=1}^\infty \frac{1}{n^2}$$
```

$$\sum_{n=1}^\infty \frac{1}{n^2} \to
  \textstyle \sum_{n=1}^\infty \frac{1}{n^2} \to
  \displaystyle \sum_{n=1}^\infty \frac{1}{n^2}$$

It is possible to switch style inline as well:

```
Compare $\displaystyle \lim_{t \to 0} \int_t^1 f(t)\, dt$ versus $\lim_{t \to 0} \int_t^1 f(t)\, dt$.
```

Compare $\displaystyle \lim_{t \to 0} \int_t^1 f(t)\, dt$ versus $\lim_{t \to 0} \int_t^1 f(t)\, dt$.



## Vertical Spacing
Some formulas such as $\overline a+\overline b=\overline {a\cdot b}$, $\sqrt{a}-\sqrt{b}$, do not look quite right when it comes to vertical spacing. Fortunately, there is more than one way to fix this. One can for instance employ the `\mathstrut` command as follows:

```
$\sqrt{\mathstrut a} - \sqrt{\mathstrut b}$
```

Which yields: $\sqrt{a}-\sqrt{b}$. Or using` \vphantom` (vertical phantom) command, which measures the height of its argument and places a math strut of that height into the formula.

```
$\sqrt{\vphantom{b} a} - \sqrt{b}$
```
Which renders as: $\sqrt{\vphantom{b} a} - \sqrt{b}$.

Another issue is with the spacing within lines in situations like this,

> Based on the previous technique, we can simplify $\dfrac{1}{\sqrt{\vphantom{b} a} - \sqrt{b}}$, and we thus get the result of the previous limit.

These two lines are too far apart, but this is unnecessary since the second line is very short. We can solve this by using the `\smash` command, to get:

> Based on the previous technique, we can simplify $\smash{\dfrac{1}{\sqrt{\vphantom{b} a} - \sqrt{b}}}$, and we thus get the result of the previous limit.


## Equation numbering
####Simple equation
To give an equation a number, use the `\tag{}`. To refer to it later, use `\label{}` to label this equation. When you want to refer to it, use `\eqref{}`. For example,

```tex
$$
e=mc^2 \tag{1}\label{eq1}
$$
```

Equation (1) is one the greatest equations in mankind history. Equation `$\eqref{eq1}$` is produced using the following code,

```tex
$$e=mc^2 \tag{1}\label{eq1}$$
```
To refer to it, use `\eqref{eq1}`.

#### Multi-line equation
Multi-line equation is actually just one equation rather than several equations. So the correct environment is aligned instead of align.


Equation (2) is a multi-line equation. The code to produce equation (2) is
```
$$\begin{equation}\begin{aligned}
a &= b + c \\
  &= d + e + f + g \\
  &= h + i
\end{aligned}\end{equation}\tag{2}\label{eq2}$$
```

### Multiple aligned equations
For multiple aligned equations, we use the align environment.

Equation (3), (4) and (5) are multiple equations aligned together. The code to produce these equations is,
```
$$\begin{align}
a &= b + c \tag{3}\label{eq3} \\
x &= yz \tag{4}\label{eq4}\\
l &= m - n \tag{5}\label{eq5}
\end{align}$$
```


# Units
While $\LaTeX$ has packages that format units, MathJax does not. For visual consistency, one should format units within the same string of MathJax code as the value to which it corresponds, separating the value and unit with `\` (space-backslash-space) since the BIPM recommends a small space between the value and units. In addition, follow the below conventions for formatting values and units:

#### Decimal Separator & Digit Separation
Following the conventions of the English-speaking world, a `.` . should be used to separate the decimal part of a number from the integral part, not `,` , as is common in some languages. This is because commas are already reserved for separating mathematical notation such as arguments of multivariate functions, elements of a set, and the coordinates of ordered tuples.

No punctuation should be used to separate multiples of three digits on either side of the decimal separator; instead, a small space rendered by `\`, should be used on both sides of the decimal marker when the string of digits consists of more than four or five digits. For example,  
- `4321.1234 ` $4321.1234$
- `54\,321.123\,45`  $54\,321.123\,45$
- `0.56789`  $0.56789$
- `0.567\,89 `  $0.567\,89$

If you use a decimal separator, you should include a digit on both sides of the separator, even if the digit is simply 0.

#### Powers of 10
Seeing as we are not calculators, it is preferable to fully write without abbreviation `\times10^{n}` $\times10^{n}$ when scientific or engineering notation is helpful or necessary. Do not precede or follow this markdown with positive nor negative spaces; \times takes care of that on its own.

Nevertheless, if necessary, use an upright variant of the letter ‘E’ or ‘e’ to indicate order of magnitude, such as

- `\mathrm{E}\,6` $\mathrm{E}\,6$
- `\scriptsize{\mathrm{E}}\,\normalsize{6}` $\scriptsize{\mathrm{E}}\,\normalsize{6}$
- `\mathrm{e}\,6` $\mathrm{e}\,6$

A small space on either side is perfectly fine and recommended.

#### Single Units
The symbol of any unit—especially SI units—should follow the form `\mathrm{u}`. (I have this command saved under the keyboard shortcut usin on my devices.) For example,

- `\mathrm{m}` $\mathrm{m}$
- `\mathrm{kg}` $\mathrm{kg}$
- `\mathrm{ft.}` $\mathrm{ft.}$

Do not use a period with symbolic units; do use a period with abbreviated units.

#### Units with a Dot Multiplier
Multiplied units conjoined by a dot should follow the form `\mathrm{u}\!\cdot\!\mathrm{v}` $\mathrm{u}\!\cdot\!\mathrm{v}$. (I have this sequence of commands saved under the keyboard shortcut umul on my devices.) Because of how \cdot is designed (i.e., to separate numbers), the small negative space \! on either side maintains uniform spacing throughout the whole compound unit. For example,

- `\mathrm{N}\!\cdot\!\mathrm{m}` $\mathrm{N}\!\cdot\!\mathrm{m}$
- `\mathrm{s}\!\cdot\!\mathrm{A}`  $\mathrm{s}\!\cdot\!\mathrm{A} $
  
Do not use \times × as a separator.

#### Units with a Solidus Separator
Divided units conjoined by a solidus should follow the form `\left.\mathrm{u}\middle/\mathrm{v}\right.` $\left.\mathrm{u}\middle/\mathrm{v}\right.$. (I have this sequence of commands saved under the keyboard shortcut udiv on my devices.) The extra markdown is to ensure that solidus stretches the entire height of the unit, especially when exponents are involved. For example,

- `\left.\mathrm{J}\middle/\mathrm{s}\right.` $\left.\mathrm{J}\middle/\mathrm{s}\right.$
- `\left.\mathrm{m}\middle/\mathrm{s}^2\right.`$\left.\mathrm{m}\middle/\mathrm{s}^2\right.$
You may include small negative spaces `\!` on either side of the solidus if you please.

#### Exponents
Exponents can be rendered with the standard MathJax markdown. The carat and number should immediately follow the closing brace of the `mathrm{}` argument. For example,

- `\mathrm{m}^2` $\mathrm{m}^2$
- `\left.\mathrm{m}\middle/\mathrm{s}^2\right.` $\left.\mathrm{m}\middle/\mathrm{s}^2\right.$


#### Parentheses
Parentheses can also be rendered with standard MathJax markdown using `\left(` and `\right)` outside the argument of \mathrm. For example,
```
\left.\mathrm{kg}\!\cdot\!\mathrm{m}^2\middle/\left(\mathrm{C}\!\cdot\!\mathrm{s}\right)\right. 
```

$$\left.\mathrm{kg}\!\cdot\!\mathrm{m}^2\middle/\left(\mathrm{C}\!\cdot\!\mathrm{s}\right)\right.$$

#### Exponents in Place of Separators
If you prefer to use no separators and only powers, separator each single `\mathrm{}` with a small space `\`, and use exponents as necessary. For example,

- `\mathrm{m}\,\mathrm{s}^{-2}` $\mathrm{m}\,\mathrm{s}^{-2}$
- `\mathrm{s}^{-1}\,\mathrm{mol}` $\mathrm{s}^{-1}\,\mathrm{mol}$

#### Examples in Context

```
\mu_0=4\pi\times10^{-7} \ \left.\mathrm{\mathrm{T}\!\cdot\!\mathrm{m}}\middle/\mathrm{A}\right.
```
$$\mu_0=4\pi\times10^{-7} \ \left.\mathrm{\mathrm{T}\!\cdot\!\mathrm{m}}\middle/\mathrm{A}\right.$$

```
180^\circ=\pi \ \mathrm{rad}
```

$$180^\circ=\pi \ \mathrm{rad}$$

```
N_A = 6.022\times10^{23} \ \mathrm{mol}^{-1}
```
$$N_A = 6.022\times10^{23} \ \mathrm{mol}^{-1}$$



## Mixing code and MathJax formatting on lines
To give an example of how this might be useful, I wanted to express an algorithm in more or less the same indentation and symbolic way it appears in a paper.

On my desktop browsers (Chrome, Firefox) the following appears reasonably well spaced and indented, but loses indentation on my Android smartphone:

**Input**: positive integer $n$  
**Output**: Tangent numbers $T_1,\ldots,T_n$  
$T_1\gets 1$  
for $k$ from 2 to $n$  
&nbsp;&nbsp;&nbsp;&nbsp; $T_k\gets (k−1)T_{k−1}$  
for $k$ from 2 to $n$  
&nbsp;&nbsp;&nbsp;&nbsp; for $j$ from $k$ to $n$  
&nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp; $T_j\gets (j −k)T_{j−1} + (j −k+2)T_j$  
`return` $T_1,\ldots,T_n$.  

The source can be examined for specific techniques, but the basic trick is that a MathJax dollar-delimiter can follow a closing back-tick code delimiter, but an opening back-tick should be preceded by a space when following the (closing) dollar-sign delimiter.

Here is a version using `\phantom` rather than code monospacing to produce indents and tweaking the spacing between code and MathJax expressions with `\;`, so that the results appear clear on Android browsers:

**Input**: positive integer $n$  
**Output**: Tangent numbers $T_1,\ldots,T_n$  
$T_1\gets 1$  
for $k$ from 2 to $n$  
$\phantom{{}++{}}$ $T_k\gets (k−1)T_{k−1}$  
for $k$ from 2 to $n$  
$\phantom{{}++{}}$for $j$ from $k$ to $n$  
$\phantom{{}++{}}$ $\phantom{{}++{}}$ $T_j\gets (j −k)T_{j−1} + (j −k+2)T_j$  
`return` $T_1,\ldots,T_n$.  
