# 問題へのリンク
https://leetcode.com/problems/intersection-of-two-arrays/description/

# 進め方

- 自分で考える。エラーをはかずに3回解くようになるまで書いてみる。
- 他の人のコードを見て、自分のコードと比較して修正する。
- 時間計算量を見積もる。
- https://github.com/Yuto729/LeetCode_arai60/pull/16#discussion_r2602118324

## 自分で考える

### 考え方

- `nums2` を順番に見ていき、`nums1` に含まれている要素を取り出す。
- ただし、取り出した要素はスキップする。

### 実装
- `nums1` の要素をキーとする HashMap を作る。HashMapの値は `bool`を用いる（初期値は`False`にする）。これは、その要素をすでに取り出したかどうかを判定するために使う。
- `nums2` の各要素に対して、HashMapに存在するか確認し、かつ対応する値が`False`なら取り出す。その後値は`True`に更新する。
- 最後に取り出した要素のリストを返す。

### 実行ステップと処理時間

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

1) 変数名をいろいろ見た。`nums1_lookup`は、`nums1_without_duplicates`のほうがよさそう。

2) https://github.com/katataku/leetcode/pull/12/changes/a8657bcaa0080b9d079e3cd3c23df41f3cbc87fc#diff-801d96f7c65ed1087c93c1615e70fa43096cfbb3478152533d182c4f72933a40R11-R12
- 以下のようにも書くことができる。
```py
class Solution:
    def intersection(self, nums1: List[int], nums2: List[int]) -> List[int]:
        return list(set(nums1) & set(nums2))
```
- (CPython: https://github.com/python/cpython/blob/39e69a7cd54d44c9061db89bb15c460d30fba7a6/Objects/setobject.c#L1354-L1355)

3) https://github.com/katataku/leetcode/pull/12/changes/a8657bcaa0080b9d079e3cd3c23df41f3cbc87fc#r1893968021

> これは、まあ、これでいいんですが、もう少し書き方にバリエーションがあるように思います。挙げてみますか?
> たとえば、追加質問で考えられるのは、「片方がとても大きくて、片方がとても小さいときには、大きい方を set にするのは大変じゃないでしょうか、特に大きいほうが sort 済みのときにはどうしますか。」とかです。

- メモリサイズに厳しい制約があるときは、確保するメモリサイズを抑えるため、HashTableを使いたくない。また、in-placeで処理することもあるかもしれない。
- 上記の追加質問を少しアレンジした問題を考えてみる。




### 問題設定

- `nums1`と`nums2`がソートされているとする。
- `nums1`と`nums2`は非常に大きく、これらと同等のサイズの追加メモリを確保したくないという制約があるとする。

### 解き方
- `nums2`を書き換えながら、`intersection`を構築する。
- `nums2`を先頭から順に走査する。重複はスキップする。
- 各要素が`nums1`に含まれているか判定する。判定には二分探索を用いる。含まれている値は先頭側に詰めていく。


```py
class Solution:
    def intersection(self, nums1: List[int], nums2: List[int]) -> List[int]:
        #nums1とnums2がソートされているとする。
        #nums1とnums2がとても大きく、これらと同等のサイズの追加メモリを確保したくないという要求があったとする。
        nums1.sort()
        nums2.sort()

        #実装はここから
        def _binary_search(value, array):
            left = 0
            right = len(array) - 1
            while left <= right:
                middle = (left + right) // 2
                if array[middle] == value:
                    return True
                elif array[middle] < value:
                    left = middle + 1
                else:
                    right = middle - 1
            return False
        
        intersection_index = 0
        candidate_index = 0
        while candidate_index < len(nums2):
            candidate_value = nums2[candidate_index]

            if _binary_search(candidate_value, nums1):
                nums2[intersection_index] = candidate_value
                intersection_index += 1
            
            while candidate_index < len(nums2) and nums2[candidate_index] == candidate_value:
                candidate_index += 1
        
        del nums2[intersection_index:]
        return nums2
```

- 打ち間違いなどが多く、エラーを3回ださずに書くのに結構リトライした。この分量のコードだとだいたい4分弱かかる。


### これを考える際に調べたこと

#### `list`がどの程度のサイズまで扱えるのか。

> - CPython implementation detail: len raises OverflowError on lengths larger than sys.maxsize, such as range(2 ** 100) (https://docs.python.org/3/library/functions.html#len）
> - sys. maxsize: An integer giving the maximum value a variable of type Py_ssize_t can take. It’s usually 2^(31 - 1) on a 32-bit platform and 2^(63 - 1) on a 64-bit platform.(https://docs.python.org/3/library/sys.html#sys.maxsize)
- とのことだが、`sys.maxsize`に到達する前にメモリが足らなくなるだろう。



#### `len()`の計算量

- `list`の長さを知ってから、入力の長さをNとしたときにO(N)以上の処理を減らしたくなった。`len()`がO(N)で動作していないか気になったので実装を見た。
- https://github.com/python/cpython/blob/36e4ffc1/Python/bltinmodule.c#L1983
- https://github.com/python/cpython/blob/main/Objects/abstract.c#L57
- https://github.com/python/cpython/blob/main/Include/cpython/listobject.h#L25
- https://github.com/python/cpython/blob/db5936c5b89aa19e04d63120e0cf5bbc73bf2420/Include/object.h#L318
- このあたりを追っかけた結果、`ob_size`というものを返しているだけであり、O(1)だとわかった。


#### `del`はin-placeで処理をするのか。
- https://docs.python.org/3/reference/simple_stmts.html#the-del-statement
. deletion of a slicing is in general equivalent to assignment of an empty slice of the right type (but even this is determined by the sliced object).

- とのこと。試しにjupyter notebookで実行してみるとin-placeで変更されていることが分かった（Python3.13(XPython)で実行）。

```py
a = [1,2,3]
print(id(a)) # 47839472
a[1:] = []
print(a)     # [1]
print(id(a)) # 47839472
```
