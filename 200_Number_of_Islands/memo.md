## 問題へのリンク
https://leetcode.com/problems/number-of-islands/description/

## 進め方

- 自分で考える。書く前に時間計算量を見積もる(https://github.com/Yuto729/LeetCode_arai60/pull/16#discussion_r2602118324)。
- エラーをはかずに3回解くようになるまで書いてみる。
- 他の人のコードを見て、自分のコードと比較して修正する。

### 考え方

・各要素を順番に見ていく
・（未探索の）陸地を発見したら、その陸地から探索（上下左右の隣接する陸地を再帰的にたどり、同じ島に属するすべての陸地を訪れる）を行い、訪問済みの印をつける。
・（探索済みの）島もしくは海ならスキップする。

**実行時間の見積もり**
`m = len(grid) <= 3*10^2`,  `n = len(grid[0]) <= 3*10^2`
各要素は最大一回探索される（explore_island関数が呼ばれる。探索回数は最大`9*10^4≒10^5`)
各探索は、概算数十ステップとすると、コード全体の処理は`10^6`くらい
実行ステップを`10^7/秒`とすると数百ミリ秒かかる

考慮したこと
・島（入力）を破壊しないこと。島の情報を渡して、数を数えてと依頼を出し、返ってきたときに島の情報が書き換わっていたらびっくりするだろう。

```py
class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        LAND = '1'
        WATER = '0'

        if not any(grid):
            return 0

        def explore_island(row: int, col: int) -> None:
            if row < 0 or row >= len(grid):
                return
            if col < 0 or col >= len(grid[row]):
                return
            if grid[row][col] == WATER or (row,col) in visited:
                return
            
            visited.add((row, col))

            explore_island(row + 1, col)
            explore_island(row, col + 1)
            explore_island(row - 1, col)
            explore_island(row, col - 1)

        visited = set()
        number_of_island = 0
        for row in range(len(grid)):
            for col in range(len(grid[row])):
                if grid[row][col] == LAND and (row, col) not in visited:
                    number_of_island += 1
                    explore_island(row, col)
        
        return number_of_island
```


他の選択肢は思いつかなかった。
まだまだ、広い選択肢から比較検討してよさそうなものを選べるだけのスキルはない。

## 他の人のコードを読む

### A) 解きかたのアプローチに関するもの
https://github.com/tNita/arai60/pull/17/changes#diff-aebad28eff850d7a6e1ef6430490e8350ba9ea923904cb57cfc959d63fbed767R31-R300

#### 幅優先探索
- 先ほどの解きかたは深さ優先探索だったことが分かった。他の解きかたは、幅優先探索がある。
- 幅優先探索では、未探索の陸地（LAND）を見つけたら、それと隣接する陸地を**すべて**探索し、同一の島として訪問済みにする（これを隣接に陸が見つからなくなるまで繰り返す）。
- コードを見てみると、gridの各要素を最大1回しか探索しないので、深さ優先探索と幅優先探索の実行時間はだいたい同じ。
- 幅優先探索を練習として書いてみる。1)深さ優先か幅優先か、2)再帰を使うか使わずに書くかの4パターンで書く。

- 深さ優先はdfs.pyに記載
- 幅優先はbfs.pyに記載

全パターンでエラーを吐かずにかけるようになるまで結構かかった。コードで表現する負荷を軽減するために書く練習をたくさんしたい。


#### UnionFindを使った解きかた

- 「島を探索していく」方法とは異なり、「すべての陸地（LAND）を先に把握し、つながっているものをまとめていく」というアプローチで解く。
- 島は「上下左右でつながっているLANDの集合」である。同じ島に属するLAND同士を同じグループとしてまとめ、最終的にグループ数が島の数となる。


**処理**
1) grid を全走査し、LAND を見つける。
- この時点では、各LANDはそれぞれ別の島としてカウントしておく。つまり、(LANDの数)=(島の数)とする。

2) 各 LAND について、右・下などの隣接セルを確認し、LANDであれば同じグループにまとめる（マージする）。
- すでに同じグループの場合は何もしない。
- 異なるグループだった場合のみマージする。そのときは島の数を1つ減らす。

- すべてのマージが終わったとき、(残っているグループの数) = (島の数)となる。

- 「同じ島かどうかの判定」と「異なる島のマージ」を行うために UnionFind を用いる。



**UnionFind**
- 参考: https://en.wikipedia.org/wiki/Disjoint-set_data_structure
- UnionFindは、「要素がどのグループに属するか」を管理するデータ構造である。
- 主な操作は以下の通り：
 1) find(x): xが属するグループの代表を返す
 2) union(x, y): xとyを同じグループにまとめる

- 今回の実装では以下の名前で対応している：
 1) find → find_root
 2) union → try_merge_cells

コードはunion_find.pyに記載


### B) コーディングスタイルに関するもの
- 変数名の定義位置
https://github.com/quinn-sasha/leetcode/pull/18/changes#r1997497393
- gridの形
最初のコードでは、gridの各行の長さが均等ではないようなものをイメージしていた（len(grid[i])≠len(grid[j])の可能性を考慮していた。）問題のgridは長方形なので、そうだとする場合に変更した。長方形でない場合は、最初に解いたようなコードになるだろう。
