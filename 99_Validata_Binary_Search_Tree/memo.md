## 問題
https://leetcode.com/problems/validate-binary-search-tree/description/

Given the root of a binary tree, determine if it is a valid binary search tree (BST).

A valid BST is defined as follows:

The left subtree of a node contains only nodes with keys strictly less than the node's key.
The right subtree of a node contains only nodes with keys strictly greater than the node's key.
Both the left and right subtrees must also be binary search trees.

Constraints:
The number of nodes in the tree is in the range [1, 104].
-231 <= Node.val <= 231 - 1

## 進め方
- 最近いろいろなやり方を模索しています。かなり迷走していますが、ひとまずこれでやります。
  - (step1)問題を見た際に、考えられるアプローチを列挙し、それぞれの計算量を検討する。思いついた方法でコードで表現する。さくっと書けない場合は、他者のコードや生成AIを参考にし、なぜ書けなかったのかを分析して次に活かす。それぞれのコードで3回エラーを出さずに書く。
    - 計算量の見積もりについてのコメント: https://github.com/Yuto729/LeetCode_arai60/pull/16#discussion_r2602118324
  - (step2)他の人のコードや生成AIを参照し、他のアプローチをコードで表現する。それぞれのコードで3回エラーを出さずに書く。
  - (step3)その後、他の人のPRをコードレビューする(PRにコメントを残す)。ここで確認したいのは、この問題の練習会を開き講師としてふるまえるか。
    - レビューの仕方: https://google.github.io/eng-practices/review/reviewer/looking-for.html
      - コードレビューは、デザイン、実装、テスト、コーディングスタイルの順に重要。
      - 最終的には、どのPRを見ても他者のコードを素早く理解し、頭の中で実行して妥当性を判断し、必要に応じて修正提案ができる状態を目指す。liquo-riceさんによくコードの修正をしてもらっているがそれができるようになることを目標とする。


## step1
- 前提
  - 入力はroot (TreeNode), 出力はvalidかどうか(bool)
  - 入力が None の場合は、True を返すとする。
    - None を「空木」とみなす。空木は binary search tree（二分探索木）の条件に違反するノードを持たないため、binary search tree であると考える。
      - In computer science, a binary search tree (BST), also called an ordered or sorted binary tree, is a rooted binary tree data structure with the key of each internal node being greater than all the keys in the respective node's left subtree and less than the ones in its right subtree. (https://en.wikipedia.org/wiki/Binary_search_tree)
- アプローチ
1) 各node p に対して以下のチェックを行えばよい
  - 方針
    - p の左部分木をすべて探索して、その最大値が p の値よりも小さくことをチェック
    - p の右部分木をすべて探索して、その最小値が p の値よりも大きいことをチェック
  - 実行時間
    - すべてのnodeに高々一回アクセスすればよい(アクセス数は10^4くらい)。各アクセスは定数ステップ
    - Pythonの実行時間を10^7/秒くらいとすると数ミリ秒かかる。

- 他の方法は思いつかず...
- 実装も20分過ぎたところで書き方が思いつかず断念。関数の返り値などをどうすればよいか考えられず。
  - こんなに考えるより、詰まってしまうようなら5分で切り上げて、コードでの表現はどうすればいいか見たほうがよさそう。とにかく、まだまだコードを書くのに慣れていないので場数が必要だと思う。

- 他の方法もありそうだが、ひとまずはこれの実装をする。
- コードはidea1.mdです。

## step2

- (別のアプローチ1)今のnodeがどの範囲に収まっていればよいかをチェックするのは同じだが、範囲の取得方法が違う。
- 範囲は、わざわざ葉まで取りに行かなくても、親から得られる情報で判断可能。
- 全然気づかなかったけど、他の人はだいたいこれ。
  - https://github.com/kitano-kazuki/leetcode/pull/28/changes
  - https://github.com/Manato110/LeetCode-arai60/pull/28
  - https://github.com/Yuto729/LeetCode_arai60/pull/33/changes
  - https://github.com/tom4649/Coding/pull/27/changes

- コードはidea2.mdです。

- (別のアプローチ2)inorderで見ていけば、(直前に見たnodeの値) < (今見ているnodeの値)になっていれば、BSTである。
  -   - https://github.com/Manato110/LeetCode-arai60/pull/28
- コードはidea3.mdです。 


- ここで、idea1.md, idea2.md, idea3.mdのコードをエラーがでなくなるまで3回書く。だいぶかかった。


## 他の人のコードを見る。見たコードにはコメントをする。
- 以下のコードを見た
  - https://github.com/Manato110/LeetCode-arai60/pull/28
  - https://github.com/Yuto729/LeetCode_arai60/pull/33
  - https://github.com/kitano-kazuki/leetcode/pull/28
  - https://github.com/tom4649/Coding/pull/27
  - https://github.com/ksaito0629/leetcode_arai60/pull/20
　- https://github.com/mamo3gr/arai60/pull/26
  - https://github.com/huyfififi/coding-challenges/pull/39

- どれも読みはそれなりにでき、ちょっとイメージとは違うコードがあっても、すぐに理解できた。気になる部分はコメントしました。
- こういうやり方もありかもしれない。


#### メモ
- 知らなかった用語
- 木の巡回方法は3種類(アルゴリズムイントロダクション第三版より抜粋)
  - 中間順木巡回(inorder tree walk)：根のキーを、その左部分木に出現するキーを印刷した後、右部分木に出現するキーを印刷する前に印刷する
  - 先行順木巡回(preorder tree walk)：根のキーを左右両方の部分木に出現するキーより先に印刷する。
  - 後行順木巡回(postorder tree walk)：根のキーを左右両方の部分木に出現するキーを印刷した後で印刷する。
