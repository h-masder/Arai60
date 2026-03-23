## リンク
(https://leetcode.com/problems/kth-largest-element-in-a-stream/description/)
ストリームとして与えられるスコアに対して、常に「K番目に大きい値」を返す。

# 進め方

・自分で考える。エラーをはかずに3回解くようになるまで書いてみる。
・他の人のコードを見て、自分のコードと比較して修正する。


#### 自分で考える


**[大まかな方針]**

・上位K個のスコアのみを保持する

・その中で最小の値を返すことで、K番目に大きい値を取得する


**[実現方法]**
サイズKのmin-heapを使用する。

**初期化（Kth largest）**

・各要素をmin-heapにpushする。要素数がKを超えた場合、最小値をpopする。

**追加時(add)**

・新しい値をmin-heapにpushする。

・要素数がKを超えた場合、最小値をpopする。

・heapの最小値を返す。

**使用ライブラリ**

min-heapの実装には、heapqライブラリを使用する。

heapqライブラリの中身をちょっとみてみた。
・listで実現されている(https://github.com/python/cpython/blob/3.14/Lib/heapq.py)。割と直感的な実装。

-maxheapは3.14からなので互換性に注意。max-heapを使いたいときは、値を負にして min-heap を使うのも選択肢の一つ。


```py
import heapq
class KthLargest:

    def __init__(self, k: int, nums: List[int]):
        self.k = k
        self.heap = []

        for i in nums:
            heapq.heappush(self.heap, i)
            if len(self.heap) > self.k:
                heapq.heappop(self.heap)


    def add(self, val: int) -> int:
        heapq.heappush(self.heap, val)
        if len(self.heap) > self.k:
            heapq.heappop(self.heap)
        return self.heap[0]
```

#### 他の人のコードと比較する

https://github.com/tom4649/Coding/pull/8/
- 私が、heapとしている変数名に、top_k_valuesとしている。
heapという名前より、何をしているのかわかる名前を付けたほうが良い（前回もstackという変数を使っていた）。heapq ライブラリのように、min-heap を構築すること自体が目的である場合には、heap という名前でも問題なさそう。
- __init__でaddを呼ぶ。



https://github.com/dorxyxki/arai60/pull/8/changes/fca7ffa25234e70bac027e16db51e6fd2e03605a
heapqを自作している。
CPython のライブラリを見てみると、コード行数は少なく、ロジックも比較的分かりやすいため、自分で書けそうだと感じた。この程度は理解しておいてもよいかもしれない。

クラスで書くべきか、関数のまま書くべきかについては、現時点では明確な判断軸を持ち合わせていない。  
ひとまず今回は、ライブラリを自分で実装することを目的としているため、関数として実装する。




```py
class KthLargest:

    def __init__(self, k, nums):
        self._k = k
        self._topk_largest = []
        for i in nums:
            self.add(i)


    def add(self, val):
        heappush(self._topk_largest, val)
        if len(self._topk_largest) > self._k:
            heappop(self._topk_largest)
        return self._topk_largest[0]



def heappush(heap, item):
    heap.append(item)
    _siftdown(heap, 0, len(heap)-1)

def heappop(heap):
    lastelt = heap.pop()
    if heap:
        rootelt = heap[0]
        heap[0] = lastelt
        _siftup(heap, 0)
        return rootelt
    return lastelt

#-末尾に追加された要素をmin-heap条件を満たす位置までroot方向に移動させる。
def _siftdown(heap, startpos, pos):
    item = heap[pos]

    while startpos < pos:
        parentpos = (pos - 1) // 2
        parent = heap[parentpos]
        if item < parent:
            heap[pos] = heap[parentpos]
            pos = parentpos
        else:
            break
    heap[pos] = item

#rootの要素を一度leafまで移動する。そこから_siftdownする。
def _siftup(heap, pos):
    item = heap[pos]
    endpos = len(heap)
    childpos = 2*pos + 1
    while childpos < endpos:
        rightpos = childpos + 1
        if rightpos < endpos and not heap[childpos] < heap[rightpos]:
            childpos = rightpos
        heap[pos] = heap[childpos]
        pos = childpos
        childpos = 2*pos + 1
    
    heap[pos] = item
    _siftdown(heap, 0, pos)
```
