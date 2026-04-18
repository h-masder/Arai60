## 問題
https://neetcode.io/problems/count-connected-components/question

You have a graph of n nodes. You are given an integer n and an array edges where edges[i] = [aᵢ, bᵢ] indicates that there is an edge between aᵢ and bᵢ in the graph.
Return the number of connected components in the graph.

Constraints:
`1 <= n <= 2000`
`1 <= edges.length <= 5000`
`edges[i].length == 2`
`0 <= aᵢ <= bᵢ < n`
`aᵢ != bᵢ`
There are no repeated edges.

## 進め方

- 自分で考える。書く前に時間計算量を見積もる(https://github.com/Yuto729/LeetCode_arai60/pull/16#discussion_r2602118324)。
- エラーをはかずに3回解くようになるまで書いてみる。
- 他の人のコードを見て、自分のコードと比較して修正する。

### 考え方

- `edges[i]` を前から順番に見ていく。各`[aᵢ, bᵢ]`について、`aᵢ` と `bᵢ` を同じグループとしてまとめていく。最終的にグループ数をconnected component数として返す。

- まとめるときはconnected component数を以下のように数える：
- `aᵢ` と `bᵢ` の両方がどのグループにも属していない場合、新しいグループが1つ増えるのでconnected component数を1増やす。
- どちらか一方のみがすでにグループに属している場合、グループ数は変わらないのでconnected component数はそのまま
- `aᵢ` と `bᵢ` がそれぞれ異なるグループに属している場合、その2つのグループが統合されるため、グループ数は1つ減る。つまり、connected component数を1減らす。

- グループの管理はUnionFindで行う。

**実行時間の見積もり**
- `1 <= edges.length <= 5000`
- edgesへのアクセスが(5*10^3)回
- グループにする処理は数ステップ。トータルで10^4~10^5程度
- Pythonの実行ステップが10^7/秒くらいだとすると、数～数十ミリ秒くらい

```py
class UnionFind:
    def __init__(self, number: int) -> None:
        self.parent = list(range(number))
        self.size = [1] * number
    
    def find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: int, y: int, count: int) -> int:
        CONNECTED = 2
        root_x = self.find(x)
        root_y = self.find(y)

        if root_x == root_y:
            return count
        
        if self.size[root_x] >= CONNECTED and self.size[root_y] >= CONNECTED:
            count -= 1
        if self.size[root_x] < CONNECTED and self.size[root_y] < CONNECTED:
            count += 1

        if self.size[root_x] < self.size[root_y]:
            root_x, root_y = root_y, root_x
        self.parent[root_y] = root_x
        self.size[root_x] += self.size[root_y]

        return count

class Solution:
    def countComponents(self, n: int, edges: List[List[int]]) -> int:
        nodes = UnionFind(n)
        count = 0
        
        for index in range(len(edges)):
            i, j = edges[index]
            count = nodes.union(i , j, count)

        return count
```

- 上記のコードをSubmitしたとき、以下の入力でエラーが出た。

Input:
- `n=4, edges=[[2,3],[1,2],[1,3]]`

Your Output: `1`
Expected Output: `2`

node4はどこにもつながっていない(disconnected nodeである)が、それもconnected componentsとしてcountするらしい。disconnected nodeはcountにいれる想定はしていなかった。
書く前に想定できるとよいと思う。
以下のように書けばdisconnected nodeもcountできる。

```py
class UnionFind:
    def __init__(self, number: int) -> None:
        self.parent = list(range(number))
        self.size = [1] * number
    
    def find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: int, y: int, num_connected_components: int, num_disconnected_nodes: int) -> int:
        CONNECTED = 2
        root_x = self.find(x)
        root_y = self.find(y)

        if root_x == root_y:
            return num_connected_components, num_disconnected_nodes
        
        if self.size[root_x] >= CONNECTED and self.size[root_y] >= CONNECTED:
            num_connected_components -= 1
        elif self.size[root_x] < CONNECTED and self.size[root_y] < CONNECTED:
            num_connected_components += 1
            num_disconnected_nodes -= 2
        else:
            num_disconnected_nodes -= 1

        if self.size[root_x] < self.size[root_y]:
            root_x, root_y = root_y, root_x
        self.parent[root_y] = root_x
        self.size[root_x] += self.size[root_y]

        return num_connected_components, num_disconnected_nodes

class Solution:
    def countComponents(self, n: int, edges: List[List[int]]) -> int:
        nodes = UnionFind(n)
        num_connected_components = 0
        num_disconnected_nodes = n
        
        for index in range(len(edges)):
            i, j = edges[index]
            num_connected_components, num_disconnected_nodes = nodes.union(i , j, num_connected_components, num_disconnected_nodes)

        return num_connected_components + num_disconnected_nodes

```

これでは、見づらいのでシンプルにできないか考えた。
disconnected nodeはcountにいれる想定なら、unionするときにcountを一つ減らすだけで良い。
加えて、edgesのループもシンプルにした。

```py
class UnionFind:
    def __init__(self, number: int) -> None:
        self.parent = list(range(number))
        self.size = [1] * number
    
    def find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x: int, y: int, count: int) -> int:
        root_x = self.find(x)
        root_y = self.find(y)

        if root_x == root_y:
            return count
        
        if self.size[root_x] < self.size[root_y]:
            root_x, root_y = root_y, root_x
        self.parent[root_y] = root_x
        self.size[root_x] += self.size[root_y]

        return count - 1


class Solution:
    def countComponents(self, n: int, edges: List[List[int]]) -> int:
        nodes = UnionFind(n)
        # disconnected nodes are counted as connected components.
        count = n

        for node1, node2 in edges:
            count = nodes.union(node1, node2, count)
        
        return count
```

こんな感じでよさそう。

`dict`でできそうだと考えていたので、それも書いて残しておく。
```py
class Solution:
    def countComponents(self, n: int, edges: List[List[int]]) -> int:
        node_to_group = {}
        groups = []

        for node1, node2 in edges:
            if node1 not in node_to_group and node2 not in node_to_group:
                group = {node1, node2}
                groups.append(group)
                node_to_group[node1] = group
                node_to_group[node2] = group
            elif node1 in node_to_group and node2 not in node_to_group:
                node1_group = node_to_group[node1]
                node1_group.add(node2)
                node_to_group[node2] = node1_group
            elif node1 not in node_to_group and node2 in node_to_group:
                node2_group = node_to_group[node2]
                node2_group.add(node1)
                node_to_group[node1] = node2_group
            else:
                node1_group = node_to_group[node1]
                node2_group = node_to_group[node2]

                if node1_group == node2_group:
                    continue
                
                node1_group |= node2_group
                for node in node2_group:
                    node_to_group[node] = node1_group
                groups.remove(node2_group)
        
        return len(groups) + (n - len(node_to_group))
```

深さ優先や幅優先でやる方法は思いつかず。
探索するイメージがわかなかった。


### 他の人のコードを見る。

深さ優先や幅優先でやっている人のコードをちら見して、ヒントをもらって自分で書いてみる。
https://github.com/rimokem/arai60/pull/19/changes
何やら隣接リストを作成しているのを見つけた。この情報でできるか考えてみる。

- 例えば1、`[[0, 1], [0, 2], [1, 2]]`のとき
- {
- 0: [1, 2]
- 1: [0]
- 2: [0, 1]
- }
- のような隣接リストを作る。

- こうしておけば、幅優先の場合は
- 0の処理をし、
- （0の隣接である）1と2を処理し、
- （1, 2 の隣接である）0と1を処理して、、、と続く。

- 深さ優先の場合は
- 0の処理をし、
- （0の隣接である）1の処理をし、
- （1の隣接である）0の処理をして、、、と続く。

- 探索が終わると一つのconnected nodeができる。

- これでできそう。隣接リストを作るというアイデアがなかったので解けなかったようだ。

- 深さ優先
```py
class Solution:
    def countComponents(self, n: int, edges: List[List[int]]) -> int:
        neighbors = {i: [] for i in range(n)}
        for node1, node2 in edges:
            neighbors[node1].append(node2)
            neighbors[node2].append(node1)

        visited = set()
        def explore_nodes(node: int) -> None:
            #深さ優先, 再帰
            if node in visited:
                return
            visited.add(node)
            for neighbor in neighbors[node]:
                explore_nodes(neighbor)

        count = 0
        for node in range(n):
            if node not in visited:
                explore_nodes(node)
                count += 1
        
        return count
```

- 幅優先
```py
class Solution:
    def countComponents(self, n: int, edges: List[List[int]]) -> int:
        neighbors = {i: [] for i in range(n)}
        for node1, node2 in edges:
            neighbors[node1].append(node2)
            neighbors[node2].append(node1)

        visited = set()
        def explore_nodes(nodes: List[int]) -> None:
            if not nodes:
                return
            next_nodes = []
            for node in nodes:
                visited.add(node)
                for neighbor in neighbors[node]:
                    if neighbor not in visited:
                        next_nodes.append(neighbor)
            return explore_nodes(next_nodes)

        count = 0
        for node in range(n):
            if node not in visited:
                explore_nodes([node])
                count += 1
        
        return count
```
他の方のコードを見たが、解く方針は同じ
https://github.com/Manato110/LeetCode-arai60/pull/20
https://github.com/yumyum116/LeetCode_Arai60/pull/16
https://github.com/dorxyxki/arai60/pull/19
など
