## 問題へのリンク
https://leetcode.com/problems/max-area-of-island/description/

## 進め方

- 自分で考える。書く前に時間計算量を見積もる(https://github.com/Yuto729/LeetCode_arai60/pull/16#discussion_r2602118324)。
- エラーをはかずに3回解くようになるまで書いてみる。
- 他の人のコードを見て、自分のコードと比較して修正する。

### 考え方
前回のコードとほぼ同じ、島を探索しながら、島の大きさを調べる。

- 幅優先探索や深さ優先探索で解く場合：島を探索しながら、島の大きさを出す。一番大きい値を返す。
- UnionFindを使って解く場合：もっともsizeが大きい島を返す。

**実行時間の見積もり**
前回の処理に、島の大きさを加える処理が加わる。探索と並行してできるので、同じ大きさのgridに対する前回の実行時間と今回の実行時間は大差なし。

`m = len(grid) <= 5*10^1`,  `n = len(grid[0]) <= 5*10^1`
各要素は最大一回探索される（explore_island関数が呼ばれる。探索回数は最大`2.5*10^3`)
各探索は、概算数十ステップとすると、コード全体の処理は`10^5`くらい
実行ステップを`10^7/秒`とすると数十ミリ秒かかる

幅優先でかくなら、
```py
class Solution:
    def maxAreaOfIsland(self, grid: List[List[int]]) -> int:
        LAND = 1
        WATER = 0

        number_of_rows = len(grid)
        number_of_cols = len(grid[0])

        if number_of_rows == 0 or number_of_cols == 0:
            return 0
        
        visited = set()
        def get_island_size(row: int, col: int) -> int:
            frontier = deque([(row, col)])
            island_size = 1
            while frontier:
                row, col = frontier.popleft()
                for neighbor_row, neighbor_col in [(row + 1, col), (row, col + 1), (row - 1, col), (row, col - 1)]:
                    if not(0 <= neighbor_row < number_of_rows):
                        continue
                    if not(0 <= neighbor_col < number_of_cols):
                        continue
                    if not(grid[neighbor_row][neighbor_col] == LAND and (neighbor_row, neighbor_col) not in visited):
                        continue
                    
                    visited.add((neighbor_row, neighbor_col))
                    frontier.append((neighbor_row, neighbor_col))
                    island_size += 1
            return island_size

        max_island_size = 0
        for row in range(number_of_rows):
            for col in range(number_of_cols):
                if grid[row][col] == LAND and (row, col) not in visited:
                    visited.add((row, col))
                    island_size = get_island_size(row, col)
                    if max_island_size < island_size:
                        max_island_size = island_size
        return max_island_size

```


後は、`visited = set()`をつかわない、かつ、深さ優先（再帰で表現）なら以下のようにかける
```py
class Solution:
class Solution:
    def maxAreaOfIsland(self, grid: List[List[int]]) -> int:
        LAND = 1
        WATER = 0
        VISITED = 2

        number_of_rows = len(grid)
        number_of_cols = len(grid[0])
        if number_of_rows == 0 or number_of_cols == 0:
            return 0
        
        def get_island_size(row: int, col: int) -> int:
            if not(0 <= row < number_of_rows):
                return 0
            if not(0 <= col < number_of_cols):
                return 0
            if grid[row][col] != LAND:
                return 0
            
            grid[row][col] = VISITED
            island_size = 1
            for delta_row, delta_col in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                island_size  += get_island_size(row + delta_row, col + delta_col)
            
            return island_size
        
        max_island_size = 0
        for row in range(number_of_rows):
            for col in range(number_of_cols):
                if grid[row][col] != LAND:
                    continue
                
                island_size = get_island_size(row, col)
                if max_island_size < island_size:
                    max_island_size = island_size
        
        for row in range(number_of_rows):
            for col in range(number_of_cols):
                if grid[row][col] == VISITED:
                    grid[row][col] = LAND

        return max_island_size
```
島のおおきさを調べる方法としては、これが好みかもしれない


（`number_of_XXX`という変数名に関するコメントをいただき、ここからは`number_of_`は`num_`に変更することにした。）

UnionFindで書くなら
```py
class UnionFind:
    def __init__(self, number: int):
        self.parent = list(range(number))
        self.size = [1] * number
    
    def find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x: int, y: int) -> None:
        root_x = self.find(x)
        root_y = self.find(y)

        if root_x == root_y:
            return
        
        if self.size[root_x] < self.size[root_y]:
            root_x, root_y = root_y, root_x
        self.parent[root_y] = self.parent[root_x]
        self.size[root_x] += self.size[root_y]


class Solution:
    def maxAreaOfIsland(self, grid: List[List[int]]) -> int:
        LAND = 1
        WATER = 0

        num_rows = len(grid)
        num_cols = len(grid[0])
        if num_rows == 0 or num_cols == 0:
            return 0
        
        island_groups = UnionFind(num_rows * num_cols)
        max_island_size = 0
        for row in range(num_rows):
            for col in range(num_cols):
                if grid[row][col] != LAND:
                    continue
                
                max_island_size = max(max_island_size, 1)
                for delta_row, delta_col in [(1, 0), (0, 1)]:
                    neighbor_row, neighbor_col = row + delta_row, col + delta_col
                    if not(0 <= neighbor_row < num_rows):
                        continue
                    if not(0 <= neighbor_col < num_cols):
                        continue
                    if grid[neighbor_row][neighbor_col] != LAND:
                        continue
                    
                    original_position = row * num_cols + col
                    # union down(original_position + nums_cols) or left(original_position + 1)
                    island_groups.union(original_position, original_position + delta_row * num_cols + delta_col)
                    island_size = island_groups.size[island_groups.find(original_position)]
                    if max_island_size < island_size:
                        max_island_size = island_size
        
        return max_island_size
```


前回の問題で似たようなコードをたくさん書いたので、滑らかに書くことができた。


### 他の人のコードを読む

1) 再帰のLimitに注意する。（https://github.com/tNita/arai60/pull/18）
> 再帰の深さは最大50 * 50 = 2,500 > [recursion limit(1000)](https://docs.python.org/3/library/sys.html#sys.getrecursionlimit)なので再帰はやめておく
- 再帰があまりにも深い場合は避けたほうがよさそう。

2) Max_island_sizeの比較(https://github.com/hemispherium/LeetCode_Arai60/pull/18/changes)
- max関数で簡単に書ける。
3) 深さ優先探索（再帰なし）における、探索場所の追加方法
- 次の探索場所を最後に一気にいれる方法。深さ優先ならこれが読みやすいかな。
```py
class Solution:
    def maxAreaOfIsland(self, grid: List[List[int]]) -> int:
        LAND = 1
        WATER = 0

        num_rows = len(grid)
        num_cols = len(grid[0])

        if num_rows == 0 or num_cols == 0:
            return 0
        
        visited = set()
        def get_island_size(row: int, col: int) -> int:
            frontier = [(row, col)]
            island_size = 0
            while frontier:
                row, col = frontier.pop()
                if not(0 <= row < num_rows):
                    continue
                if not(0 <= col < num_cols):
                    continue
                if not(grid[row][col] == LAND and (row, col) not in visited):
                    continue
                
                visited.add((row, col))
                island_size += 1
                #次の探索場所を最後に一気にいれる
                frontier.extend([(row + 1, col), (row, col + 1), (row - 1, col), (row, col -1)])

            return island_size

        max_island_size = 0
        for row in range(num_rows):
            for col in range(num_cols):
                if grid[row][col] == LAND and (row, col) not in visited:
                    island_size = get_island_size(row, col)
                    max_island_size = max(max_island_size, island_size)
        return max_island_size
```

4) UnionFindのデータ構造
- メモリサイズの削減（https://github.com/tNita/arai60/pull/18）: 自分の実装ではparentのサイズはgridと同じだが、landの数にしている。
- データの保持方法: 自分の実装では一次元配列にしていたが、二次元配列にしている。こちらのほうが、 `original_position = row * num_cols + col`一次元配列に計算しなおす必要がないので読みやすいかもしれない。intからtupleにするので、若干遅くなる。ミリ秒以下の世界だとこのあたりもどちらを選択するか考えてもいいかも
```py
class UnionFind:
    def __init__(self, points: List[tuple[int, int]]) -> None:
        self.parent = {}
        self.size = {}
        for point in points:
            self.parent[point] = point
            self.size[point] = 1
    
    def find(self, x: tuple[int, int]) -> tuple[int, int]:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x: tuple[int, int], y: tuple[int, int]) -> None:
        root_x = self.find(x)
        root_y = self.find(y)

        if root_x == root_y:
            return
        
        if self.size[root_x] < self.size[root_y]:
            root_x, root_y = root_y, root_x
        self.parent[root_y] = self.parent[root_x]
        self.size[root_x] += self.size[root_y]


class Solution:
    def maxAreaOfIsland(self, grid: List[List[int]]) -> int:
        LAND = 1
        WATER = 0

        num_rows = len(grid)
        num_cols = len(grid[0])
        if num_rows == 0 or num_cols == 0:
            return 0
        
        lands = {}
        for row in range(num_rows):
            for col in range(num_cols):
                if grid[row][col] == LAND:
                    lands[(row, col)] = (row, col)
        
        island_groups = UnionFind(lands)
        max_island_size = 0
        for row in range(num_rows):
            for col in range(num_cols):
                if grid[row][col] != LAND:
                    continue
                
                max_island_size = max(max_island_size, 1)
                for neighbor_row, neighbor_col in [(row + 1, col), (row, col + 1)]:
                    if not(0 <= neighbor_row < num_rows):
                        continue
                    if not(0 <= neighbor_col < num_cols):
                        continue
                    if grid[neighbor_row][neighbor_col] != LAND:
                        continue
                    
                    island_groups.union((row, col), (neighbor_row, neighbor_col))
                    island_size = island_groups.size[island_groups.find((row, col))]
                    max_island_size = max(max_island_size, island_size)
        
        return max_island_size
```

- いろいろなバリエーションを練習したので、他の人のコードも読みやすかった。読めるようになるために、書く必要があるのだと改めて実感した。
