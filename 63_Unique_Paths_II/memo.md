## 問題
https://leetcode.com/problems/unique-paths-ii/

You are given an m x n integer array grid. There is a robot initially located at the top-left corner (i.e., grid[0][0]). The robot tries to move to the bottom-right corner (i.e., grid[m - 1][n - 1]). The robot can only move either down or right at any point in time.

An obstacle and space are marked as 1 or 0 respectively in grid. A path that the robot takes cannot include any square that is an obstacle.

Return the number of possible unique paths that the robot can take to reach the bottom-right corner.

The testcases are generated so that the answer will be less than or equal to 2 * 10^9.


Constraints:

m == obstacleGrid.length
n == obstacleGrid[i].length
1 <= m, n <= 100
obstacleGrid[i][j] is 0 or 1.


## 進め方
- (step1)問題を見た際に、考えられるアプローチを列挙し、それぞれの計算量を検討する。思いついた方法でコードで表現する。さくっと書けない場合は、他者のコードや生成AIを参考にし、なぜ書けなかったのかを分析して次に活かす。それぞれのコードで3回エラーを出さずに書く。
- 計算量の見積もりについてのコメント: https://github.com/Yuto729/LeetCode_arai60/pull/16#discussion_r2602118324
- (step2)他の人のコードや生成AIを参照し、他のアプローチをコードで表現する。それぞれのコードで3回エラーを出さずに書く。
- (step3)その後、他の人のPRをコードレビューする(PRにコメントを残す)。ここで確認したいのは、この問題の練習会を開き講師としてふるまえるか。
- レビューの仕方: https://google.github.io/eng-practices/review/reviewer/looking-for.html
    - コードレビューは、デザイン、実装、テスト、コーディングスタイルの順に重要。
    - 最終的には、どのPRを見ても他者のコードを素早く理解し、頭の中で実行して妥当性を判断し、必要に応じて修正提案ができる状態を目指す。

## アプローチ
- 前問(62. Unique Paths)と考え方は同じ。
- obstacleは避ける


**実行時間の見積もり**
- 行×列のメモリアクセス。各メモリアクセスでは、足し算などの数十ステップ程度が実行される。1 <= m, n <= 100より、総ステップ数は最大で10^4~10^5くらい。
- Pythonの実行時間を10^7ステップ/秒とすると、数ms~数十ms。

- **code1**
```py
class Solution:
    def uniquePathsWithObstacles(self, obstacles: List[List[int]]) -> int:
        OBSTACLE = 1
        num_rows = len(obstacles)
        num_cols = len(obstacles[0])
        num_paths = [[0] * num_cols for _ in range(num_rows)]

        for i in range(num_rows):
            for j in range(num_cols):
                if obstacles[i][j] == OBSTACLE:
                    continue
                
                if i == 0 and j == 0:
                    num_paths[i][j] = 1
                    continue
                
                paths_from_up = 0
                if i > 0:
                    paths_from_up = num_paths[i - 1][j]
                paths_from_left = 0
                if j > 0:
                    paths_from_left = num_paths[i][j - 1]
                num_paths[i][j] = paths_from_up + paths_from_left
        
        return num_paths[num_rows - 1][num_cols - 1]
```


- 前回同様、num_pathsは一次元配列で書けば、メモリ消費量は削減できる(O(mn)からO(n))。
- ただし、障害物の更新には注意
- とりあえず、上記のコードをベースに修正した。

- **code2**
```py
class Solution:
    def uniquePathsWithObstacles(self, obstacles: List[List[int]]) -> int:
        OBSTACLE = 1
        num_rows = len(obstacles)
        num_cols = len(obstacles[0])
        path_counts = [0] * num_cols
        path_counts[0] = 1

        for i in range(num_rows):
            for j in range(num_cols):
                if obstacles[i][j] == OBSTACLE:
                    path_counts[j] = 0
                    continue

                if j > 0:
                    path_counts[j] += path_counts[j - 1]
        
        return path_counts[num_cols - 1]
```

- コードの行数的にはすっきりとはする。
- 初期化をforループの外で行い、forループの処理を減らしてみた。


- 前回とりあえず書いた経路を列挙する方法も練習がてら書いておく。

- **code3**
```py
class Solution:
    def uniquePathsWithObstacles(self, obstacles: List[List[int]]) -> int:
        OBSTACLE = 1
        num_rows = len(obstacles)
        num_cols = len(obstacles[0])


        if obstacles[0][0] == OBSTACLE or obstacles[num_rows - 1][num_cols - 1] == OBSTACLE:
            return 0

        paths = []
        partial_paths = [[(0, 0)]]
        while partial_paths:
            path = partial_paths.pop()
            row, col = path[-1]
            if row == num_rows - 1 and col == num_cols - 1:
                paths.append(path)
                continue
            if row < num_rows - 1 and obstacles[row + 1][col] != OBSTACLE:
                partial_paths.append(path + [(row + 1, col)])

            if col < num_cols - 1 and obstacles[row][col + 1] != OBSTACLE:
                partial_paths.append(path + [(row, col + 1)])
            
        return len(paths)
```


- メモ化再帰の方法も
- **code4**
```py
import functools
class Solution:
    def uniquePathsWithObstacles(self, obstacles: List[List[int]]) -> int:
        OBSTACLE = 1
        num_rows = len(obstacles)
        num_cols = len(obstacles[0])

        @functools.cache
        def get_unique_paths_helper(row, col):
            if obstacles[row][col] == OBSTACLE:
                return 0
            if row == 0 and col == 0:
                return 1
            if row == 0:
                return get_unique_paths_helper(row, col - 1)
            if col == 0:
                return get_unique_paths_helper(row - 1, col)

            return get_unique_paths_helper(row - 1, col) + get_unique_paths_helper(row, col - 1)
        return get_unique_paths_helper(num_rows - 1, num_cols - 1)
```


- 前回の解法のうち、Combinationを使った方法をこの方法に適用するのは無理かなと思った。他の人の解法を見る。

**他の人の解答をみる**

- code1とアイデアは同じ、num_pathsの1列目の初期化と1行目の初期化を先に行う。
  - https://github.com/hiro111208/leetcode/pull/31
  - こっちのほうが forループの中の処理は簡単に書けそう。
  - code1で気に食わなかった部分も解消できる。

```py
class Solution:
    def uniquePathsWithObstacles(self, obstacles: List[List[int]]) -> int:
        OBSTACLE = 1
        num_rows = len(obstacles)
        num_cols = len(obstacles[0])

        num_paths = [[0] * num_cols for _ in range(num_rows)]
        # 1列目の初期化
        for i in range(num_rows):
            if obstacles[i][0] == OBSTACLE:
                break
            num_paths[i][0] = 1
        
        # 1行目の初期化
        for j in range(num_cols):
            if obstacles[0][j] == OBSTACLE:
                break
            num_paths[0][j] = 1
        
        for i in range(1, num_rows):
            for j in range(1, num_cols):
                if obstacles[i][j] == OBSTACLE:
                    continue
                num_paths[i][j] = num_paths[i - 1][j] + num_paths[i][j - 1]
        
        return num_paths[num_rows - 1][num_cols - 1]

```


- 上記のPRに加え他の人のコードをもみたが、だいたい想定の範囲内だった。
  - https://github.com/Manato110/LeetCode-arai60/pull/35
  - https://github.com/attractal/leetcode/pull/23
  - https://github.com/kitano-kazuki/leetcode/pull/34
  - https://github.com/mamo3gr/arai60/pull/32
