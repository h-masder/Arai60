## 問題へのリンク
https://leetcode.com/problems/first-unique-character-in-a-string/description/

## 進め方

- 自分で考える。書く前に時間計算量を見積もる(https://github.com/Yuto729/LeetCode_arai60/pull/16#discussion_r2602118324)。
- エラーをはかずに3回解くようになるまで書いてみる。
- 他の人のコードを見て、自分のコードと比較して修正する。

## 自分で考える

### 考え方

- 1回しか出現していない文字を識別するために、まず文字列を走査し、各文字の出現回数を記録する。
- その後、再度文字列を走査し、出現回数が1回の文字のうち最初に現れるものを返す。

一回の走査でもできそうだが、実行時間にさほど影響しないので、ひとまずこれで書いてみる。

### 実行時間

- 文字列の長さは最大で 10^5 程度であり、全体で最大 2 * 10^5 回程度のメモリアクセスとなる。
- Python の実行速度を 10^7 ステップ/秒とすると、実行時間は数十ミリ秒程度。

```py
class Solution:
    def firstUniqChar(self, s: str) -> int:
        character_to_count = defaultdict(int)
        for c in s:
            character_to_count[c] += 1
        for i, c in enumerate(s):
            if character_to_count[c] == 1:
                return i
        return -1
        
```


- 文字の種類は a〜z の26種類に限られているため、2回目の走査では文字列ではなく辞書を走査する方法も考えられる。
- 実行時間はほとんど変わらないが、書く練習をする。
```py
class Solution:
    def firstUniqChar(self, s: str) -> int:
        character_to_count = {}
        character_to_index = {}
        for i, c in enumerate(s):
            if c in character_to_count:
                character_to_count[c] += 1
            else:
                character_to_count[c] = 1
                character_to_index[c] = i
        
        first_index = len(s) # len(s) means "No Found"
        for character, count in character_to_count.items():
            index = character_to_index[character]
            if count == 1 and index < first_index:
                first_index = index

        return -1 if first_index == len(s) else first_index 
```


## 他の人のコードを見る


1) non-repeating characterがない場合の返り値は、NOT_FOUND = -1 などで定義したほうがよさそう
- https://github.com/aki235/Arai60/pull/15/changes#r2781603266



2) 出現回数のカウントはCounterを使えばシンプル
- https://github.com/Kazuuuuuuu-u/arai60/pull/18/changes#r2999973600
- https://github.com/Kazuuuuuuu-u/arai60/pull/18/changes#r3000599334

確かにそう。ただ、二回走査していることがわかるようにfor文をなんとなく使いたくなる。



3) いろいろ漁っているときに一回の走査で書く方法を思いついたので、方針を考えて実装してみる。
- 一回みた文字と、二回以上見た文字をそれぞれ記録する。
- 文字列の各要素に対して、
  - 二回以上見たものはスキップ
  - 一回見たものは、二回見たものとして記録しなおす
  - これまで見ていないものは一回みたものとして記録する。
- 最終的に、一回見たものの中から最初に出現したものを返す。
- 出現順を保持するためにOrderedDictを使い、先頭の要素を取り出す。

実行時間的に大差ない（走査が二回から一回に減るので半分くらいになる）が、書く練習をする。

```py
from collections import OrderedDict

class Solution:
    def firstUniqChar(self, s: str) -> int:
        NOT_FOUND = -1
        candidates = OrderedDict()
        duplicates = set()

        for i, c in enumerate(s):
            if c in duplicates:
                continue
            
            if c in candidates:
                del candidates[c]
                duplicates.add(c)
            else:
                candidates[c] = i

        return next(iter(candidates.values())) if candidates else NOT_FOUND
```
4) OrderedDictについて

- https://github.com/python/cpython/blob/3.14/Lib/collections/__init__.py#L119 をざっと見ると、双方向のリンクリスト（Doubly Linked List）でkey-valueを格納した順序を記録しているようだ。
- `del candidates[c]`のときに対象の位置をどのように特定しているのか気になってみたところ、キーからリンクノードへの参照を `dict` で管理しているため、O(1)でリンクノードへアクセスできる。これを書いてみる。書いてみる。
- OrderedDictを実装している人もいる(https://github.com/tom4649/Coding/pull/14/changes)


**考え方**
- 順序を保持する部分をリンクリストで管理。それ以外（例えばキー(key)に対する値(value)の参照）は親クラスの`dict` を利用する。

- 初期化：
  - 空の双方向リンクリストを構築するために、ダミーのリンクノード（`root`）を作成する。
  - また、キーからリンクノードへ O(1) でアクセスするための辞書（`key_to_link`）を用意する。
- 値の追加：
  - 新しいキーの場合、リンクリストの末尾の直後に新しいリンクノードを挿入する。
  - 同時に、キーからリンクノードへの対応を`key_to_link`に登録する。
- 値の削除：
  - キーに対応するリンクノードを`key_to_link`から取り出す。
  - 取得したリンクノードの前後のリンクをつなぎ替えてリンクリストから取り除く。

```py
class Link:
    def __init__(self, prev=None, next=None, key=None):
        self.prev = prev
        self.next = next
        self.key = key

class CustomOrderedDict(dict):
    def __init__(self):
        super().__init__()
        self.key_to_link = {}
        self.root = Link()
        self.root.prev = self.root.next = self.root

    def __getitem__(self, key):
        return super().__getitem__(key)
    
    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        if key not in self.key_to_link:
            new_link = Link(prev=self.root.prev, next=self.root, key=key)
            self.root.prev.next = self.root.prev = new_link
            self.key_to_link[key] = new_link
    
    def __delitem__(self, key):
        super().__delitem__(key)
        delete_link = self.key_to_link.pop(key)
        delete_link.prev.next = delete_link.next
        delete_link.next.prev = delete_link.prev
        delete_link.prev = delete_link.next = delete_link.key = None
    
    def __iter__(self):
        link = self.root.next
        while link is not self.root:
            yield link.key
            link = link.next

class Solution:
    def firstUniqChar(self, s: str) -> int:
        NOT_FOUND = -1
        candidates = CustomOrderedDict()
        duplicates = set()

        for i, c in enumerate(s):
            if c in duplicates:
                continue
            if c in candidates:
                del candidates[c]
                duplicates.add(c)
            else:
                candidates[c] = i
        
        return next(iter(candidates.values())) if candidates else NOT_FOUND
```
- このコード量だと8分弱かかる。


- Python 3.7 から辞書の追加順序が保存されたらしいので、`Ordereddictを使わなくても動く。
- https://discord.com/channels/1084280443945353267/1195700948786491403/1231538588529852426
- https://discord.com/channels/1084280443945353267/1201211204547383386/1211166072552816680
- https://discord.com/channels/1084280443945353267/1192736784354918470/1192805202684805120
