
## リンク
(https://leetcode.com/problems/top-k-frequent-elements/description/)

# 進め方

- 自分で考える。エラーをはかずに3回解くようになるまで書いてみる。
- 他の人のコードを見て、自分のコードと比較して修正する。


#### 自分で考える

**方針**<br>

- (1)`nums` を走査し、各要素（数字）の出現回数を集計する。
- (2)出現回数が上位`k`個の数字の要素を抽出して返す。
<br>

**実装**

(1)について：
- 要素を`key`、出現回数を`value`とする辞書を用意する。
- `nums`の各要素（数字）を先頭から順に走査し、各要素に対して対応する`value`をインクリメントする。

(2)について：
- 辞書の要素(`(key, value)`のペア)を、`value`に基づいて降順でソートする。ソートは、ライブラリはあると思うが、辞書の片方（`value`）だけをみてソートする方法はこれまで考えたことないので自分で実装してみる。計算は重たいが、直感的なバブルソートで書いてみる。
- 上位`k`個の`key`を取り出し、リストとして返す。


>- 「出現回数が同じ要素が複数ある場合にどう扱うか」については少し迷ったが、今回は問題文に "It is guaranteed that the answer is unique." とあるため、今回は考慮しなくても問題ない。とはいえ、今後同様の問題に対応できるように、同数の場合の扱いも意識した設計にしておきたい。

何度か書いた後、変数名を修正した。

- これまで変数名は短くしたほうがいいのかなとおもっていた。なんとなく長いと読みづらいと感じていた。
- 以下のコメントやコードをみて、何が入っているかが変数名にかいてあると、コードがすんなり頭に入ってくることがわかった。
- 「変数名は過不足ないならなるべく短く、情報がなくなるくらいなら多少長くてもよい。」という気持ちになった。
- (https://github.com/hemispherium/LeetCode_Arai60/pull/10#discussion_r2618518592)
- (https://github.com/dorxyxki/arai60/pull/9/changes)


```py
class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        number_to_frequency = {}
        for num in nums:
            if num in number_to_frequency:
                number_to_frequency[num] += 1
            else:
                number_to_frequency[num] = 1

        sorted_by_frequency = []
        for number, frequency in number_to_frequency.items():
            sorted_by_frequency.append((number, frequency))
        
        for i in range(len(sorted_by_frequency)):
            for j in range(len(sorted_by_frequency) - i - 1):
                if sorted_by_frequency[j][1] < sorted_by_frequency[j + 1][1]:
                    sorted_by_frequency[j], sorted_by_frequency[j + 1] = sorted_by_frequency[j + 1], sorted_by_frequency[j]
        
        top_k_frequency = []
        for i in range(k):
            top_k_frequency.append(sorted_by_frequency[i][0])

        return top_k_frequency            
```

- バブルソートは計算が重たいので変更。list の sort や sorted が使えそう。
- (https://docs.python.org/3/library/stdtypes.html#list.sort)
- (https://docs.python.org/3/howto/sorting.html)


- また、以下を見る限り計算量はO(nlogn) (nは入力の長さ)とある。
- (https://wiki.python.org/moin/TimeComplexity)
- とりあえずこれを用いるが、実装の中身を知らないライブラリを使うのになんだか抵抗が出てきた。



```py
class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        number_to_frequency = {}
        for num in nums:
            if num in number_to_frequency:
                number_to_frequency[num] += 1
            else:
                number_to_frequency[num] = 1
        
        sorted_by_frequency = []
        for number, frequency in number_to_frequency.items():
            sorted_by_frequency.append((number, frequency))
        
        sorted_by_frequency.sort(key=lambda pair: pair[1], reverse=True)

        top_k = []
        for i in range(k):
            top_k.append(sorted_by_frequency[i][0])
        
        return top_k
```


## 他の人の解答を見る

(1) (https://github.com/Manato110/LeetCode-arai60/pull/9#discussion_r2973863403)

> defaultdict や Counter を使うと、よりシンプルに書けると思います。
なお Counter には most_common() という、そのままの関数があります。

- まず、defaultdictライブラリを見てみる。
- (https://docs.python.org/3.14/library/collections.html#collections.defaultdict)
- 個人的にかなり読みづらい。

> - class collections.defaultdict(default_factory=None, /[, ...])
> - The first argument provides the initial value for the default_factory attribute...
> - If default_factory is not None, it is called without arguments to provide a default value for the given key, this value is inserted in the dictionary for the key, and returned.

をみると、例えば`defaultdict(int)`でkeyがなければ`int()`が呼ばれるよう。

- 次にmost_commonをみてみる
- (https://docs.python.org/ja/3.14/library/collections.html#collections.Counter) 
> - most_common(n)：Return a list of the n most common elements and their counts from the most common to the least. If n is omitted or `None`, most_common() returns all elements in the counter.

- [CPython](https://github.com/python/cpython/blob/main/Lib/collections/__init__.py)を見ると`n`が`None`のときは`sorted(self.items(), key=_itemgetter(1), reverse=True)`が呼ばれ、そうでなければheapqの`_nlargest(n, self.items(), key=_itemgetter(1))`関数が呼ばれる。それぞれの実装をざっと見たところ、コード行数が多く理解に時間がかかりそうだったので、後日詳しく見てみる。

(2)https://github.com/Manato110/LeetCode-arai60/pull/9#discussion_r2973865722

- リストを返すときはないほう表記でシンプルに書けることを知った。

- この辺りを使って、書くだけでとてもシンプルになるので書いてみることにした。(ソートはsortedを使うことにした。)

```py
class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        number_to_frequency = defaultdict(int)
        for num in nums:
            number_to_frequency[num] += 1

        sorted_by_frequency = sorted(number_to_frequency.items(), key=lambda pair:pair[1])

        return [number for number, frequency in sorted_by_frequency[-k:]]
```


(3)(https://github.com/dorxyxki/arai60/pull/9/changes)

- 変数の使い方がうまいと感じる。参考にしたい。

###感想
- この問題は、数字や出現回数を保持するデータの構造やsortの方法はいろいろありそうなので、時間があるときに他の人の解答をもう少し調べてみるとよさそう。
