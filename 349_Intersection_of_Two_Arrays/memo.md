## リンク
https://leetcode.com/problems/intersection-of-two-arrays/description/

# 進め方

- 自分で考える。エラーをはかずに3回解くようになるまで書いてみる。
- 他の人のコードを見て、自分のコードと比較して修正する。
- 時間計算量を見積もる。
- https://github.com/Yuto729/LeetCode_arai60/pull/16#discussion_r2602118324

## 考え方

- `nums2` を順番に見ていき、`nums1` に含まれている要素を取り出す。
- ただし、取り出した要素はスキップする。

## 実装
- `nums1` の要素をキーとする HashMap を作る。HashMapの値は `bool`を用いる（初期値は`False`にする）。これは、その要素をすでに取り出したかどうかを判定するために使う。
- `nums2` の各要素に対して、HashMapに存在するか確認し、かつ対応する値が`False`なら取り出す。その後値は`True`に更新する。
- 最後に取り出した要素のリストを返す。

**実行ステップと処理時間**
- `len(nums1)`と`len(nums2)`は両方とも最大で`10^3`
- HashMapの構築では、`nums1`の要素を一つずつ処理するため、実行ステップは10^3程度
- `nums2`を走査しながら共通要素を取り出す処理も実行ステップは10^3程度
- 合計で`2×10^3`程度
Pythonの実行を(10^7ステップ/秒)くらいとすると、数ミリ秒くらいかかる


```py
class Solution:
    def intersection(self, nums1: List[int], nums2: List[int]) -> List[int]:
        intersection = []
        num_to_found = {num: False for num in nums1}
        for num in nums2:
            if num in num_to_found and not num_to_found[num]:
                num_to_found[num] = True
                intersection.append(num)
        
        return intersection
```

- setで書いたほうが`bool`が不要なのできれいかもしれない。

```py
class Solution:
    def intersection(self, nums1: List[int], nums2: List[int]) -> List[int]:
        intersection = set()
        nums1_lookup = set(nums1)

        for num in nums2:
            if num in nums1_lookup:
                intersection.add(num)
        
        return list(intersection)
```


## 他の人のコードをみる。

1) https://github.com/katataku/leetcode/pull/12/changes/a8657bcaa0080b9d079e3cd3c23df41f3cbc87fc#diff-801d96f7c65ed1087c93c1615e70fa43096cfbb3478152533d182c4f72933a40R11-R12
- 以下のようにも書くことができる。
```py
class Solution:
    def intersection(self, nums1: List[int], nums2: List[int]) -> List[int]:
        return list(set(nums1) & set(nums2))
```
- (CPython: https://github.com/python/cpython/blob/39e69a7cd54d44c9061db89bb15c460d30fba7a6/Objects/setobject.c#L1354-L1355)

2) https://github.com/katataku/leetcode/pull/12/changes/a8657bcaa0080b9d079e3cd3c23df41f3cbc87fc#r1893968021

- 入力の条件を一歩踏み込んで考えて、その場合にどのような方法が適しているかを検討している。
- 私は普段、探索の計算量を削減するために HashTable を用いているが、HashTable の利用が適さないケースはなんだろうか。メモリサイズに厳しい制約があるとき？
- というわけで、`nums1`と`nums2`がメモリサイズがめちゃくちゃでかい場合を考えてみる。

- ちょっと問題の設定を考えてみる。
- `list`がどれくらいの大きさをとれるのか調べてみる。
> - CPython implementation detail: len raises OverflowError on lengths larger than sys.maxsize, such as range(2 ** 100) (https://docs.python.org/3/library/functions.html#len）
> - sys. maxsize: An integer giving the maximum value a variable of type Py_ssize_t can take. It’s usually 2**31 - 1 on a 32-bit platform and 2**63 - 1 on a 64-bit platform.(https://docs.python.org/3/library/sys.html#sys.maxsize)
- とのことだが、`sys.maxsize`に到達する前にメモリが足らなくなる。どれぐらいが適切かわからないが問題設定は以下のようにしてみる。

#### 問題設定
- 達成したいことは問題文と同じ。
- 前提として、`nums1`と`nums2`は昇順にソートされているとする。
- 入力のケースは二通りで考え、それぞれ適切な解法はあるかどうか考える。
- (1)`nums1`の要素数と`nums2`の要素数が両方とも大きい。
- (2)片方の要素数はは大きいが、もう片方は小さい(`len(nums1) << len(nums2)` もしくはその逆)
- 要件として、要素数が大きいほうの入力と同等のメモリを新たに確保してはならないとする。

（なんとなく、N: を入力の長さとして、O(N)以上の処理を減らす実装にしたくなる）


(1)の解法
- 二つのポインタを用意して前から順にみていく

(To be provided)

(2)
- 小さいほうのリストの各要素に対して、大きいほうのリストを二分探索しながら一致するものがあるかどうか探す。
- どちらのリストが大きいか小さいかを判定するために`len`をつかうが、Nを入力の長さとして、O(N)で動いたりしないか心配になったので、実装を見る。
- https://github.com/python/cpython/blob/36e4ffc1/Python/bltinmodule.c#L1983
- https://github.com/python/cpython/blob/main/Objects/abstract.c#L57
- https://github.com/python/cpython/blob/main/Include/cpython/listobject.h#L25
- https://github.com/python/cpython/blob/db5936c5b89aa19e04d63120e0cf5bbc73bf2420/Include/object.h#L318
- この辺りをみていくと、`ob_size`というものをreturnしているだけだった（O(1)）。

(To be provided)
