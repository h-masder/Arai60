## 問題へのリンク
(https://leetcode.com/problems/valid-parentheses/)

使用言語：Python3

## 進め方
以下の通りに進めてみました。
- Step 0: 答えを見ずに5分以内に解く。わからなかったら答えを見る。
- Step 1: 本協会メンバーやLeetCodeの過去解答を参考にしつつ、開始から答えを見ないで5分以内に正解になるところまで行う。
- Step 2: 本協会メンバーやLeetCodeの過去解答を参考にしつつ、コードを見やすくする形で整える。
- Step 3: 全部消して、10分以内にエラーを一度も出さずに正解するのを3回続けて行う。
- Step 4: コメントをいただき、コードを修正する。


## Step0
・条件1(Open brackets must be closed by the same type of brackets.)を満たすには、開き括弧と対応する閉じ括弧の数が一致するかを確認する。

・条件2(Open brackets must be closed in the correct order.)を満たすには、最後に出現した開き括弧から閉じられているか確認する。


・条件3(Every close bracket has a corresponding open bracket of the same type.)を満たすには、閉じ括弧が出現する前に、対応する開き括弧が存在するかを確認する（これは問題文そのまま）。

**実装方法**
stackを使う。
開き括弧 `(`, `[`, `{` が出現したときは、それぞれ対応する閉じ括弧`)`, `]`, `}`をstackに積む。
閉じ括弧`)`, `]`, `}`が出現したときは stackから取り出す。
・文字列を最後まで走査したときに stack が空になっていれば、条件1が満たされる。
・pop するときに取り出した括弧と現在の閉じ括弧が常に一致していれば条件2が満たされる。
・また、stack が空の状態で pop しなければ、条件3が満たされる。


特に問題なく実装できた。
見通しもそんなに悪くないと感じる。
コードはcode1.pyです。
