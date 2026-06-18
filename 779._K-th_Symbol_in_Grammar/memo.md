# 問題文
- We build a table of n rows (1-indexed). We start by writing 0 in the 1st row. Now in every subsequent row, we look at the previous row and replace each occurrence of 0 with 01, and each occurrence of 1 with 10.
- For example, for n = 3, the 1st row is 0, the 2nd row is 01, and the 3rd row is 0110.
- Given two integer n and k, return the kth (1-indexed) symbol in the nth row of a table of n rows.

- Example 1:
- Input: n = 1, k = 1
- Output: 0
- Explanation: row 1: 0

- Example 2:
- Input: n = 2, k = 1
- Output: 0
- Explanation: 
  - row 1: 0
  - row 2: 01

- Example 3:
- Input: n = 2, k = 2
- Output: 1
- Explanation: 
- row 1: 0
- row 2: 01


- Constraints:
- 1 <= n <= 30
- 1 <= k <= 2^(n - 1)


# アプローチ
- やりたいことはシンプル。n 行目のsymbolを作って、k番目の値を返す。
- （指定された k が n 行目の symbolの全体の長さより大きいときは、例外を出すことにする。）
- 0を01に, 1を10に変換する性質上、i 列目のsymbolsは i + 1列目の前半になる。
- なので、n 行目にたどりつかなくても k の位置の値がわかったらsymbolをreturnできる。

**実行時間**
- symbolの列を作る方針なので、最大2^32 -1 くらい作る。10^9くらい。
- Pythonの実行時間を10^7ステップ/秒とすると、100秒くらいかかる。これはだめそう。だが一旦書く。

```py
class Solution:
    def kthGrammar(self, n: int, k: int) -> int:
        if k > 2 ** (n - 1):
            raise ValueError("k is out of range")

        if k == 1:
            return 0
        if k == 2:
            return 1
        symbols = [0, 1]
        for _ in range(2, n + 1):
            for i in range(len(symbols) // 2, len(symbols)):
                if symbols[i] == 0:
                    symbols.extend([0, 1])
                else:
                    symbols.extend([1, 0])
            if k <= len(symbols):
                return symbols[k - 1]
```

- 全部のsymbolを列挙しなくてもk番目はわかりそうだが、システマチックに導く方法がわからないので、他の人の解答を見る。


- https://github.com/mamo3gr/arai60/pull/44
  - 木構造で書いている。

```
           0
        /     \
      0        1
    /   \     /   \
  0     1     1     0
 / \   / \   / \   / \
0   1 1   0 1   0 0   1
```


  - returnするのは深さnの左から数えて、k番目の箇所。
  - 再帰で書く場合、ルートに向かって再帰して、親の値をとりながらさがってくればよい。

* 再帰の方法

  - n 行目の k 番目の symbol を 1 つのノードと考える。
  - 再帰呼び出しでは、自分の親ノードの値を問い合わせる。
  - 最初の呼び出し元は n 行目の k 番目のノードであり、再帰を繰り返すことでルートノード（1 行目 1 番目のノード）まで遡る。
  - ルートノードは値が 0 であるため、その値を報告する。
  - 報告を受けた各ノードは、以下の手順で自分の値を決定して上司（呼び出し元）に報告する。
    1. 親ノードの値を受け取る。
    2. 自分が親ノードの左の子か右の子かを判定する。
    3. 親ノードの値と、自分が左の子か右の子かから自分の値を決定する。
       - 親が 0 で、自分が左の子：0
       - 親が 0 で、自分が右の子：1
       - 親が 1 で、自分が左の子：1
       - 親が 1 で、自分が右の子：0
    4. 決定した値を上司に報告する（return する）。


```py
class Solution:
    def kthGrammar(self, n: int, k: int) -> int:
        if k > 2 ** (n - 1):
            raise ValueError("k is out of range")
        
        # Treat the grammar as a binary tree:
        #
        #           0
        #         /   \
        #        0     1
        #       / \   / \
        #      0  1 1   0
        #
        # A left child inherits its parent's value.
        # A right child flips its parent's value.
        
        if n == 1:
            return 0
        
        parent_depth = n - 1
        parent_position = (k + 1) // 2
        parent_symbol = self.kthGrammar(parent_depth, parent_position)
        left_child = (k % 2 == 1)
        if parent_symbol == 0:
            if left_child:
                return 0
            else:
                return 1
        else:
            if left_child:
                return 1
            else:
                return 0


```


- whileでも書いてみる。
```py
class Solution:
    def kthGrammar(self, n: int, k: int) -> int:
        if k > 2 ** (n - 1):
            raise ValueError("k is out of range")
        
        depth = n 
        position = k
        path = []
        while depth > 1:
            path.append((depth, position))
            depth -= 1
            position = (position + 1) // 2

        symbol = 0
        while path:
            _, position = path.pop()
            left_child = (position % 2 == 1)
            if symbol == 0:
                if left_child:
                    symbol = 0
                else:
                    symbol = 1
            else:
                if left_child:
                    symbol = 1
                else:
                    symbol = 0
        
        return symbol
```
- 少し冗長だが、素直に変換するとこんな感じ。

- もっとシンプルに書く方法はいくつかある。
  - https://github.com/h1rosaka/arai60/pull/48
  - 親からみて、左の子は親と同じsymbol, 右の子は親とは違うsymbolという性質を使うといかのようにシンプルにできる。
```py
class Solution:
    def kthGrammar(self, n: int, k: int) -> int:
        if k > 2 ** (n - 1):
            raise ValueError("k is out of range")
        if n == 1:
            return 0
        parent_depth = n - 1
        parent_position = (k + 1) // 2
        parent_symbol = self.kthGrammar(parent_depth, parent_position)
        if k % 2 == 1:
            return parent_symbol
        else:
            return 1 - parent_symbol


```

- k-1 を2進数で表すと、そのビット列がそのまま root から k までの左右の選択（0=左,1=右）に対応する。
- (右に進んだ回数)＝(ビット列中の1の数)として計算できる。
- つまるところ、root(0) から k までの経路で「右に進んだ回数（＝k-1の1の数）」の偶奇だけで値が決まる。
```py
class Solution:
    def kthGrammar(self, n: int, k: int) -> int:
        return bin(k - 1).count("1") % 2
```

- 0, 1のどちらを返せばよいかだけを保持しながら処理を進める方法
  - https://github.com/Manato110/LeetCode-arai60/pull/47 の書いたコード3
