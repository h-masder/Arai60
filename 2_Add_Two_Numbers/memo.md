## 問題へのリンク
(https://leetcode.com/problems/add-two-numbers/)

使用言語：Python

## 進め方
以下の通りに進めてみました。
- Step 0: 答えを見ずに5分以内に解く。わからなかったら答えを見る。
- Step 1: 本協会メンバーやLeetCodeの過去解答を参考にしつつ、開始から答えを見ないで5分以内に正解になるところまで行う。
- Step 2: 本協会メンバーやLeetCodeの過去解答を参考にしつつ、コードを見やすくする形で整える。
- Step 3: 全部消して、10分以内にエラーを一度も出さずに正解するのを3回続けて行う。
- Step 4: コメントをいただき、コードを修正する。


## Step0

解き方は以下のとおり。

・2つの連結リストを先頭から順に走査しながら足し算を行う。
・足し算の結果が10以上になった場合は、1を桁上がり（carry）として次の計算に持ち越す。

片方のリストが先に終わった場合は、
残っているリストの値と桁上がりだけを計算して処理を続ける。


ここまで理解して書いて実装した後、LeetCodeのexampleがちゃんと動くのか自分の頭でテストを実行してからSubmitした。
自分の頭では、問題ないとおもていたが、末尾で桁上がりする場合を考慮していなかったため、エラーが出た。自分の頭でテスト漏れがあった。
`l1 = [9,9,9,9,9,9,9]`
`l2 = [9,9,9,9]`
期待される結果：`[8,9,9,9,0,0,0,1]`
コードの実行結果：`[8,9,9,9,0,0,0]`

自分の頭によるテストでは、最後の詰めがあまいことがわかった。気を付けていきたい。
このエラーにどうすればよいか少し考えて、桁上がりがあればリストの末尾に`1`を追加すればよいと考え、実装した。

全体としてコードとして表現できるかどうかという観点で悩むことはなかった。
コードはcode1.pyです。

## Step1, Step2

書き方で気になる点は以下の通り。

**似たような処理（足し算する部分）を可読性を低下させずにコード量を減らせないか。**

(1)再帰を使った方法
https://discord.com/channels/1084280443945353267/1235829049511903273/1238087350995779674
前回の問題でもそうだったが、再帰で書くととても見通しが良くなることもある。他の人が書いたコードを理解して、実装してみた。この辺りは滑らかに書くことができた。
```py
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        def addTwoNumbersHelper(node: Optional[ListNode], l1: Optional[ListNode], l2: Optional[ListNode], carry: int) -> None:
            if l1 is None and l2 is None:
                #連結リストを末尾まで走査したあと、桁上がりがあれば1を末尾に追加（後始末）
                if carry == 1:
                    node.next = ListNode(1)
                return None
            total = carry
            carry = 0
            if l1 is not None:
                total += l1.val
                l1 = l1.next
            if l2 is not None:
                total += l2.val
                l2 = l2.next
            if total >= 10:
                carry = 1
            node.next = ListNode(total % 10)
            addTwoNumbersHelper(node.next, l1, l2, carry)
        dummy = ListNode()
        carry = 0
        addTwoNumbersHelper(dummy, l1, l2, carry)
        return dummy.next
```

(2)上の再帰はループっぽいので、似たような処理はwhileでもかけそう。ためしに書いてみた。
```py
class Solution:
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        if l1 is None and l2 is None:
            return None        
        if l1 is not None and l2 is None:
            return l1
        if l1 is None and l2 is not None:
            return l2
        
        dummy = ListNode()
        node = dummy
        carry = 0
        while l1 is not None or l2 is not None:
            total = carry
            carry = 0
            if l1 is not None:
                total += l1.val
                l1 = l1.next
            if l2 is not None:
                total += l2.val
                l2 = l2.next
            
            if total >= 10:
                carry = 1
            node.next = ListNode(total % 10)
            node = node.next

        if carry == 1:
            node.next = ListNode(1)
        return dummy.next

```

かなり見通しが良くなった気がする。

https://discord.com/channels/1084280443945353267/1195700948786491403/1197114717001502822
このあたりは、似たような考えで書かれているが「`node`がないときは0として足す」という書き方はあまり好みではないかもしれない。
私の場合、通常の足し算ではそういう計算をしないので。


dummyを使わなくても書けるらしいので、再帰で考えてみた。
加えて、carryの桁上がりも表現を変えた。

```py
class Solution:
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        def addTwoNumbersHelper(l1: Optional[ListNode], l2: Optional[ListNode], carry=0) -> Optional[ListNode]:
            if l1 is None and l2 is None:
                #連結リストを末尾まで走査したあと、桁上がりがあれば1を末尾に追加（後始末）
                if carry == 1:
                    node = ListNode(1)
                    return node
                return None

            total = carry
            carry = 0
            
            if l1 is not None:
                total += l1.val
                l1 = l1.next
            if l2 is not None:
                total += l2.val
                l2 = l2.next

            carry = total // 10       
            node = ListNode(total % 10)

            node.next = addTwoNumbersHelper(l1, l2, carry) 
            return node
        
        return addTwoNumbersHelper(l1, l2)
```

変更はこれくらいにして、残りはコメントで気になったことについて書いてみる。

1) carry は bool か int か。
https://discord.com/channels/1084280443945353267/1251052599294296114/1252296540366835823
将来3つ以上のListNodeの足し算をする可能性を考えると、桁上がりの計算は`carry = total // 10`がいい気がする。
2) a, b が変更されたらそれなりに驚く
https://discord.com/channels/1084280443945353267/1297920116025065533/1324497366748889150
・なるほど、考えたことなかった。確かに渡した引数がこちらが想定していないのに変更されたら怖い。自分自身も一度「長い方の連結リストに total を格納する」実装を考えた。しかしその方法では入力の連結リストを書き換えることになる。
```py
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def f(node):
    node.val = 1000

l1 = ListNode(next=None)

print(id(l1))
print(l1.val)
f(l1)
print(id(l1))
print(l1.val)

#==print結果==
#69284720
#0
#69284720
#1000
#=============

```
・今回のコードは l1 = l1.next や l2 = l2.next のようにnodeを走査しているだけなので、連結リストの内容は変更されていない。

3) 変数名をどうするか。
・https://github.com/Shunii85/arai60/pull/5
これまで`result`という変数名に違和感はなかったが、このレビューを見て違和感が少し理解できた気がする。
`result`と書くと、最終的に`return result`になることを連想するが、`return`自体が「結果を返す」という意味を持っているため、やや冗長に感じてきた。
```py
total = a + b
return total
```
のほうが
```py
result = a + b
return result
```
より直観的だと認識した。
また、`result`という単語は意味が広いため、何の計算結果なのかを読み違える可能性もある。実装では（引数と）戻り値は特に重要なので、そこでの理解の妨げになることは避けたい。
