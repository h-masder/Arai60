# 問題文
- https://leetcode.com/problems/powx-n/description/

- Implement pow(x, n), which calculates x raised to the power n (i.e., x^n).

- Example 1:
- Input: x = 2.00000, n = 10
- Output: 1024.00000

- Example 2:
- Input: x = 2.10000, n = 3
- Output: 9.26100

- Example 3:
- Input: x = 2.00000, n = -2
- Output: 0.25000
- Explanation: 2-2 = 1/22 = 1/4 = 0.25
 

- Constraints:
- -100.0 < x < 100.0
- -2^31 <= n <= 2^31-1
- n is an integer.
- Either x is not zero or n > 0.

# アプローチ
- Exponentiation_by_squaringでやればよい。むかし調べて実装したのでよく覚えている。
  - https://en.wikipedia.org/wiki/Exponentiation_by_squaring 

**実行時間**
- myPow関数が呼ばれるのは、log((nの絶対値))回くらい。最大の呼び出し回数は32回(n = -2^31のとき)
- 関数の中は、いくつかの四則演算と比較だけで構成されており、数十ステップとすると、総ステップは10^3くらいで実行できる。
- Pythonの実行時間を10^7ステップ/秒とすると、100μs程度。

```py
class Solution:
    def myPow(self, x: float, n: int) -> float:
        if n < 0:
            return self.myPow(1 / x, -n)
        
        if n == 0:
            return 1

        if n % 2 == 0:
            return self.myPow(x * x, n // 2)
        else:
            return x * self.myPow(x * x, (n - 1) // 2)
```

- 一応whileでも書く。
```py
class Solution:
    def myPow(self, x: float, n: int) -> float:
        if n < 0:
            x = 1 / x
            n = -n
        
        if n == 0:
            return 1
        
        base = x
        exponent = n
        power = 1.0
        while exponent > 0:
            if exponent % 2 == 1:
                power *= base
            
            base *= base
            exponent //= 2
            
        return power
```


- 気になったことを調べた。

- **Pythonのfloatの取り扱い。**
- PythonのfloatはIEEE 754（double precision）に基づく浮動小数点数である。
  - https://docs.python.org/3/tutorial/floatingpoint.html
  - almost all machines use IEEE 754 binary floating-point arithmetic, and almost all platforms map Python floats to IEEE 754 binary64 “double precision” values.
  
- CPUの浮動小数点演算ユニット（FPU）がIEEE 754規格に準拠していることによってこの挙動が実現されている。
- Intel Software Developer’s Manual
  - https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html
  - Intel® 64 and IA-32 Architectures Software Developer's Manual Volume 1: Basic Architectureに以下の記述。
  - The IA-32 architecture defines and operates on four floating-point data types: half precision floating-point, single 
precision floating-point, double precision floating-point, and double-extended precision floating-point (see 
Figure 4-3). The data formats for these data types correspond directly to formats specified in the IEEE Standard 
754 for Floating-Point Arithmetic. 

- **baseがfloat型のときのpow実行において、どういうときにinfが出力されるか、どういうときにoverflowエラーになるか**
- 生成AIを使いながら調べ、以下のように結論付けた。間違っていたらコメントお願いします。
    - exponentがint型のときfloat型に変換するが、float型で表現できる範囲をこえた場合は Overflowエラー
    - pow関数を無事に実行できたとして、出力がfloatで表現できる範囲をこえた場合はinf
```py
print(pow(2.0, 1023)) # -> 8.98846567431158e+307 
print(pow(2.0, 1023) * 2) # -> inf
print(pow(2.0, 1024)) # overflowエラー

# overflowになるのは、演算結果のよるものか、引数によるものかチェック。以下の結果から引数によるものと推測。
print(pow(2.0, 1023) * 4) # -> inf
print(pow(2.0, 1023) * 8) # -> inf

# 以下の結果からint -> float処理で失敗するのではと推測
print(float(pow(2, 1023))) # -> 8.98846567431158e+307
print(float(pow(2, 1024))) # -> overflowエラー
```

- https://github.com/python/cpython/blob/main/Objects/floatobject.c#L687 をみると、floatのpowはCONVERT_TO_DOUBLEでfloatに変換しているように見える
  - ただ、本当にここでoverflowするのかはわからない。


# 他の人のコードを見る。
- 別の解法としては、ビットシフト
  - https://github.com/Yuto729/leetcode/pull/50/changes
  - https://github.com/Manato110/LeetCode-arai60/pull/46

指数 `n` を2進数で表現すると、`n` は 2 の冪の和として表せる。したがって、
$$
n = \sum_k b_k 2^k
$$
と書けるので、
$$
x^n=x^{\sum_k b_k 2^k}=\prod_k x^{b_k 2^k}
$$
となる。ここで $b_k \in \{0, 1\}$ は2進数の各ビットである。したがって、`x^n` は対応する `x^(2^k)` のうち、ビットが1であるものの積として表せる。この性質を利用して累乗を計算する。
例えば、
$$
13 = 1101_2 = 2^3 + 2^2 + 2^0
$$
なので、
$$
x^{13}=x^{2^3 + 2^2 + 2^0}=x^8 \times x^4 \times x
$$
となる。
実際の計算では、
$$
x,\ x^2,\ x^4,\ x^8,\ \dots
$$
を順に計算し、指数の2進数表現でビットが1になっている項だけを掛け合わせることで `x^n` を求める。

```py
class Solution:
    def myPow(self, x: float, n: int) -> float:
        if n < 0:
            x = 1 / x
            n = -n
        
        if n == 0:
            return 1
        
        base = x
        exponent = n
        power = 1.0
        while exponent > 0:
            if exponent & 1:
                power *= base
            
            base *= base
            exponent >>= 1

        return power
        
```


- 参考コメント
  -  return self.myPow(1 / x, -n)について
  - > 引数を変更するために再帰的に呼び出すのは、やりすぎかもしれません。 step 2 のほうが個人的には好きです。
    -   - https://github.com/yumyum116/LeetCode_Arai60/pull/11/changes#r3027117050
  - 入力の破壊
    - https://github.com/TORUS0818/leetcode/pull/47#discussion_r2031692691

- 上記二つには、同意。


  - sliding windowによる解法
    - https://github.com/mamo3gr/arai60/pull/43
    - 後でまた見ることにする。
