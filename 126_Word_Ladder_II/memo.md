## 問題
https://leetcode.com/problems/word-ladder-ii/description/

A transformation sequence from word beginWord to word endWord using a dictionary wordList is a sequence of words beginWord -> s1 -> s2 -> ... -> sk such that:

Every adjacent pair of words differs by a single letter.
Every si for 1 <= i <= k is in wordList. Note that beginWord does not need to be in wordList.
sk == endWord
Given two words, beginWord and endWord, and a dictionary wordList, return all the shortest transformation sequences from beginWord to endWord, or an empty list if no such sequence exists. Each sequence should be returned as a list of the words [beginWord, s1, s2, ..., sk].

Constraints:
- 1 <= beginWord.length <= 5
- endWord.length == beginWord.length
- 1 <= wordList.length <= 500
- wordList[i].length == beginWord.length
- beginWord, endWord, and wordList[i] consist of lowercase English letters.
- beginWord != endWord
- All the words in wordList are unique.
- The sum of all shortest transformation sequences does not exceed 10^5.

## 進め方

- 自分で考える。書く前に時間計算量を見積もる(https://github.com/Yuto729/LeetCode_arai60/pull/16#discussion_r2602118324)。
- エラーをはかずに3回解くようになるまで書いてみる。

## 考え方

- 最短経路の長さを求める [126. Word Ladder I](https://github.com/h-masder/Arai60/pull/21) をベースに考える。幅優先探索を用いる。
- 本問題の難しさは、最短経路をすべて列挙すること。
- 最初はすべての経路を前方から保持しようとしたが、メモリ量が膨大になるため非現実的だった。
- 通勤中しばらく考えて、各Wordに対し、一文字違い(Neighbor)が子、Wordが親の関係を保持する方法が良いと考えた。例えば"hot" のNeighborが "dot"のとき、dotの親(parent)はhotであることを保持する。
- 注意点として、すべての最短経路を列挙するためには、重複排除の扱いを Word Ladder I と変える必要がある。
- 幅優先探索では、同じレベル（beginWordからの距離が同じ）にあるノードはすべて同じ最短距離なので、そのレベル内では重複を許す必要がある。
- 一方で、次のレベルに進む前にそのレベルで初めて到達したノードをまとめて visited に追加することで、重複を再探索を防ぐ。
- 経路の復元は、各ノードの parent を辿ることで行う。
- この復元方法の設計がすぐには思いつかず、ヒントを参考にした。実装方法としては、スタックを用いれば実装できそうであることがわかった。
- 具体的には、(word, path) のようなタプルをスタックに積み、親ノードを辿りながら path を拡張していく。
- (「複数の情報（ノードと経路）を同時に持つ構造」を扱うのが苦手であることが分かった)


**実行時間の見積もり**

- L: wordの長さ(- 1 <= L <= 5)
- N: wordListの長さ(1 <= N <= 500)
- ハッシュテーブル(pattern_to_neighbors)の構築時間: wordListを前から走査しながら、wordの文字列長だけkey-valueを作成するので、2.5*10^3くらい(L * N)
- 探索は最大で N 回のwordListアクセスが発生する。各アクセスでwordの長さハッシュテーブルの検索をするので、2.5*10^3くらい(L * N)
- 経路の構築は最大で N 回のwordListアクセスが発生するので、5*10^2くらい。
- トータルで5.5*10^3くらい。
Pythonの実行ステップを10^7回/秒と仮定すると、遅くても数ミリ秒くらい。

```py
class WordNeighbors:
    def __init__(self, words: List[str]) -> None:
        self.pattern_to_neighbors = defaultdict(list)
        for word in words:
            for pattern in self.generate_pattern(word):
                self.pattern_to_neighbors[pattern].append(word)
    
    def generate_pattern(self, word: str) -> Iterator[Tuple[str, str]]:
        for i in range(len(word)):
            yield (word[ : i], word[i + 1 : ])
    
    def get_neighbors(self, word: str) -> Iterator[str]:
        for pattern in self.generate_pattern(word):
            for neighbor in self.pattern_to_neighbors[pattern]:
                yield neighbor
    
    def neighbors_clear(self, word: str) -> None:
        for pattern in self.generate_pattern(word):
            self.pattern_to_neighbors[pattern].clear()

class Solution:
    def findLadders(self, beginWord: str, endWord: str, wordList: List[str]) -> List[List[str]]:
        if endWord not in wordList:
            return []
        
        neighbors = WordNeighbors(wordList)
        frontier = [beginWord]
        visited = {beginWord}
        parents = defaultdict(list)
        endWord_found = False
        while frontier and not endWord_found:
            next_frontier = []
            current_level_visited = set()
            for word in frontier:
                for neighbor in neighbors.get_neighbors(word):
                    if neighbor in visited:
                        continue
                    if neighbor == endWord:
                        endWord_found = True
                    parents[neighbor].append(word)
                    if neighbor in current_level_visited:
                        continue
                    current_level_visited.add(neighbor)
                    next_frontier.append(neighbor)
            for word in frontier:
                neighbors.neighbors_clear(word)
            visited |= current_level_visited
            frontier = next_frontier
        
        if not endWord_found:
            return []

        sequences = []
        word_and_path = [(endWord, [endWord])]
        while word_and_path:
            word, path = word_and_path.pop()
            
            if word == beginWord:
                sequences.append(path)
                continue
            
            for parent in parents[word]:
                word_and_path.append((parent, [parent] + path))
        
        return sequences

```

## 修正

```py
    def neighbors_clear(self, word: str) -> None:
        for pattern in self.generate_pattern(word):
            self.pattern_to_neighbors[pattern].clear()
```
はないほうがよさそう。
- 入力がそんなに大きくないので、実行時間の短縮のメリットは多くない一方で、
- clearすることで最短経路の漏れがないか読み手に確認させる負荷が圧倒的に高い。

```py
class WordNeighbors:
    def __init__(self, words: List[str]) -> None:
        self.pattern_to_neighbors = defaultdict(list)
        for word in words:
            for pattern in self.generate_pattern(word):
                self.pattern_to_neighbors[pattern].append(word)
        
    def generate_pattern(self, word: str) -> Iterator[Tuple[str, str]]:
        for i in range(len(word)):
            yield (word[ : i], word[i + 1 : ])
    
    def get_neighbors(self, word: str) -> Iterator[str]:
        for pattern in self.generate_pattern(word):
            for neighbor in self.pattern_to_neighbors[pattern]:
                yield neighbor

class Solution:
    def findLadders(self, beginWord: str, endWord: str, wordList: List[str]) -> List[List[str]]:
        if endWord not in wordList:
            return []
        
        neighbors = WordNeighbors(wordList)
        frontier = [beginWord]
        visited = {beginWord}
        parents = defaultdict(list)
        endWord_found = False
        while frontier and not endWord_found:
            next_frontier = []
            current_level_visited = set()
            for word in frontier:
                for neighbor in neighbors.get_neighbors(word):
                    if neighbor in visited:
                        continue
                    if neighbor == endWord:
                        endWord_found = True
                    parents[neighbor].append(word)
                    if neighbor in current_level_visited:
                        continue
                    current_level_visited.add(neighbor)
                    next_frontier.append(neighbor)
            visited |= current_level_visited
            frontier = next_frontier
        
        if not endWord_found:
            return []
        
        sequences = []
        word_and_path = [(endWord, [endWord])]
        while word_and_path:
            word, path = word_and_path.pop()
            if word == beginWord:
                sequences.append(path)
            for parent in parents[word]:
                word_and_path.append((parent, [parent] + path))
        return sequences


```
