## 問題へのリンク
(https://leetcode.com/problems/remove-duplicates-from-sorted-list/description/)



使用言語：Python3

## 進め方
以下の通りに進めてみました。
- Step 0: 答えを見ずに5分以内に解く。
- Step 1: 本協会メンバーやLeetCodeの過去解答を参考にしつつ、開始から答えを見ないで5分以内に正解になるところまで行う。
- Step 2: 本協会メンバーやLeetCodeの過去解答を参考にしつつ、コードを見やすくする形で整える。
- Step 3: 全部消して、10分以内にエラーを一度も出さずに正解するのを3回続けて行う。
- Step 4: コメントをいただき、コードを修正する。




## step0
以下のどちらかを繰り返せばよいと考えた。
1) 今のノードと次のノードを比較して同じならば、次のノードを消して、そのノードにとどまる。
2) 今のノードと次のノードを比較して違っていたら、次のノードに進む。

そのまま実装してみた。はじめは文法ミスによるエラーを何度かはいたが、数回練習するとエラーなく書くことができた。
コードははcode1.pyです。

## step1

他の解答をいくつか見た。いろいろなコメントをさらいつつ、思いついた方法でいくつか書いてみた。
特に時間計算量も空間計算量も同じだが、書き方は変えられそう。

#### #1
例えば
```
class Solution:
    def deleteDuplicates(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if head is None:
            return None
        node = head

        while node.next is not None:
            if node.val == node.next.val:
                node.next = node.next.next
            else:
                node = node.next
        
        return head
```

のようにはじめにhead is Noneのチェックをすることで、while文の処理の見通しが若干よくなる気がした。



#### #2 
他にも、処理の表現方法の変更として、いかのようなものもあった
(https://discord.com/channels/1084280443945353267/1195700948786491403/1196388760275910747)

```
class Solution:
    def deleteDuplicates(self, head: Optional[ListNode]) -> Optional[ListNode]:
        node = head
        while node is not None:
            while node.next is not None and node.val == node.next.val:
                node.next = node.next.next
            node = node.next
        
        return head
```
なるほどと思った。


#### #3
他には再帰で解いているものもあった。
(https://github.com/dorxyxki/arai60/pull/3)
このPRで気になったのは以下のコメント。
```
確かに仕事の引き継ぎだと考えるとシンプルに考えられそうですね。
特に引き継ぎの仕方の具体例がとてもわかりやすく、腑に落ちました。

以下、コメントに対する自分なりの理解ですが、

上司、自分、部下を設定して考える

前提として

上司からは不完成品がくる
上司は完成品を期待してる
部下に不完成品を渡すと完成品を返してくれる
```
再帰はあまり詳しくないのもあるが、理解するのが難しい。自分がなぜ再帰を理解できないのか考えてみた。
一つの結論として、処理の流れが双方向になっていることが原因だと思った。つまり、


・再帰呼び出しによって下に処理が進んでいく方向 （上司->自分->部下の方向）
・return によって結果が上に戻ってくる方向（部下->自分->上司の方向）


の二つがあり、両方について同時に考えるときつくなる（これは、分散プロトコルの双方向メッセージの流れの理解の難しさと少し似ている）。

ではどうすれば自分が再帰を使いこなせるか考えたところ、一つ思いついたのは、それぞれの方向で何をしたいのかを明確にイメージしてから実装することが重要と考えた。例えば、分割統治法を再帰で表現する場合、

・再帰が深くなる方向では問題を分割
・returnしていく方向では結果をマージ

といったイメージ。

今回の問題では、

・再帰が深くなる方向では、nodeを末尾までたどる
・returnの方向では、headをそのまま返す（or headが保持されていれば return Noneでもよい）

という形になるように実装した。
コードはcode2.pyです。

