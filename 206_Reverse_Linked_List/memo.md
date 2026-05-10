## リンク
(https://leetcode.com/problems/reverse-linked-list/)

## 考え方

**[大まかな方針]**

ループで解く。
各ループでは次の処理を行う。

・末尾のnodeを取り出す。

・取り出したnodeを、reverse linked listの末尾に追加する。

・元リストからそのnodeを削除する（次のループでは、その一つ前が末尾になるようにする）。


**[実現方法]**

・「末尾のノードを取り出す」ためには、リストの最後までたどればよい

・「reverse linkde list に追加する」は、そのまま実装すればよい

・「元リストからそのnodeを削除する」には、最後から2番目のノードの next を None にする

**[懸念点]**

この実装の懸念点は、

・入力を書き換えてしまっていること

・変数名が適切かどうか（これにはいつも悩む）

時間計算量はO(N^2)だが、コードに落とし込む練習として書いてみる。

```py
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if head is None or head.next is None:
            return head
        
        dummy = ListNode()
        reverse = dummy

        while head.next is not None:
            node = head
            prev = None
            while node.next is not None:
                prev = node
                node = node.next
            reverse.next = ListNode(val=node.val)
            reverse = reverse.next
            prev.next = None #入力を書き換えている部分

        reverse.next = ListNode(head.val)
        return dummy.next
```

**[入力を書き換えない方法1]**

入力をコピーしてから処理することで、元のリストを保持できる。
例えば以下のように書ける。

```py
class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if head is None or head.next is None:
            return head
        
        #copy
        copy_head = ListNode(val=head.val)
        copy = copy_head
        node = head
        while node.next is not None:
            copy.next = ListNode(val=node.next.val)
            copy = copy.next
            node = node.next
        
        #create reverse linked list
        dummy = ListNode()
        reverse = dummy
        while copy_head.next is not None:
            prev = None
            node = copy_head
            while node.next is not None:
                prev = node
                node = node.next
            reverse.next = ListNode(val=node.val)
            reverse = reverse.next
            prev.next = None
        
        reverse.next = ListNode(val=copy_head.val)
        return dummy.next
```

ただし、この方法でも変数名の難しさはむしろ強く感じた。
後から処理を追加・変更しやすい名前を意識したいが、なかなか難しい。


**[入力を書き換えない方法2]**

再帰でも書いてみる。直感的にも入力を更新しなくて済む点がよい。

**[再帰での解き方]**

・素直にnodeごとに分割する。
`(node1)-(node2)-(node3)`のような問題は
`(node1)`, `(node2)`, `(node3)`の問題に分割。

・最小の問題（base case）は、末尾の `node` をそのまま返せばよい

・組み合わせでは、
「後ろの部分で作った reverse linked list」に現在の`node`を追加する
ただし、先頭ノードを失わないように、先頭と末尾の両方を戻り値として扱う

> 自分は、再帰の問題は次の三つのことを考える問題だと思っています。
> 1) どうやって問題を小さくするのか。（問題の分割）
> 2) 最小の問題（これ以上分割できない問題）をどう解くのか。
> 3) 分割した問題の答えをどう組み合わせるか

```py
class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        def helperReverseList(node: Optional[ListNode]) -> Tuple[Optional[ListNode], Optional[ListNode]]:
            if node.next is None:
                reverse = ListNode(val=node.val)
                return reverse, reverse

            reverse_head, reverse_tail = helperReverseList(node.next)
            reverse_tail.next = ListNode(val=node.val)
            return reverse_head, reverse_tail.next

        if head is None:
            return None
        reverse_head, _ = helperReverseList(head)
        return reverse_head
```

変数名はしっくりこないが、自分で解くのはひとまずこれくらいにして、他の人の解答を見る。

**[他の人の解法]**

1) https://github.com/Manato110/LeetCode-arai60/pull/7

・Stackで解くと見通しがよさそう。
（実際は、この方はstackでは解いていないようだが、直感的でわかりやすいと思った。）

リストの値を全部pushする。
最後まで行ったらpopしながらつなぎ合わせる。

```py
class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if head is None or head.next is None:
            return head
        
        stack = []
        node = head
        while node is not None:
            stack.append(node.val)
            node = node.next
        
        dummy = ListNode()
        reverse = dummy
        while stack:
            v = stack.pop()
            reverse.next = ListNode(v)
            reverse = reverse.next
        return dummy.next
```
見通しもよく一番好みかもしれない。



**[逆向きにreverse linked listをのばす]**

・これは、なんとなく選択肢から外していた。自分の思考の癖とはちょっと離れているのかも。とはいえ見通しは良いのかな。
```py
class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if head is None or head.next is None:
            return head
        
        reverse = None
        node = head
        while node is not None:
            new_node = ListNode(val=node.val)
            new_node.next = reverse
            reverse = new_node
            node = node.next
        return reverse
```

結局これが一番素直なのかな。
ただ、どのコードもすらすらかけるので、どの解法も特別に無理のある発想ではなく、いずれも自然に導ける範囲にあると感じた。

**[気づき]**

1) 出題意図は「リンクのつなぎ替えを正しく扱えるか」にある。

https://github.com/tom4649/Coding/pull/6

https://github.com/tom4649/Coding/pull/6#discussion_r2923258917

> 私はこの問題の意図は、リンクの繋ぎ変えをできるか、混乱せずにお手玉ができるかであろうと判断しました。出題者によっては違うかもしれません。

- たしかにそれはそう。


2) 再帰は整理すると理解しやすいが、メモリ消費には注意が必要

 https://github.com/dorxyxki/arai60/pull/7/changes
