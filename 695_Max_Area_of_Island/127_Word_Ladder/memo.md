## 問題
https://leetcode.com/problems/word-ladder/description/

A transformation sequence from word beginWord to word endWord using a dictionary wordList is a sequence of words beginWord -> s1 -> s2 -> ... -> sk such that:

Every adjacent pair of words differs by a single letter.
Every si for 1 <= i <= k is in wordList. Note that beginWord does not need to be in wordList.
sk == endWord
Given two words, beginWord and endWord, and a dictionary wordList, return the number of words in the shortest transformation sequence from beginWord to endWord, or 0 if no such sequence exists.

Constraints:

- 1 <= beginWord.length <= 10
- endWord.length == beginWord.length
- 1 <= wordList.length <= 5000
- wordList[i].length == beginWord.length
- beginWord, endWord, and wordList[i] consist of lowercase English letters.
- beginWord != endWord
- All the words in wordList are unique.

## 進め方

- 自分で考える。書く前に時間計算量を見積もる(https://github.com/Yuto729/LeetCode_arai60/pull/16#discussion_r2602118324)。
- エラーをはかずに3回解くようになるまで書いてみる。
- 他の人のコードを見て、自分のコードと比較して修正する。

## 考え方

一文字違いを見ながら、進める。
これは、深さ優先ではなく、幅優先のほうが相性がよさそう。
幅優先なら、1文字違い -> 2文字違い -> ・・・のように、順にみていくので最短経路を保証しながら探索できる。

一方、深さ優先は、出現した経路が文字の長さを超えた場合、それが最短経路である保証はないので調べ続ける必要がある。


**実行時間の見積もり**
- 1 <= beginWord.length <= 10
- 1 <= wordList.length <= 5000
wordの長さだけ幅優先探索をするため、最大で10回程度の層を処理する。
幅優先探索の各wordに対してwordListを全探索しているため、(5×10^3)^2回程度の比較が発生する。
さらに、1文字違いかどうかを調べるのにwordの長さだけ比較する(最大10回)。
トータルで約2.5×10^8回程度の計算量になる。
Pythonの実行ステップを10^7回/秒と仮定すると、数十秒かかる。
かなり遅いが、ひとまずこの方針で実装する。

```py
class Solution:
    def ladderLength(self, beginWord: str, endWord: str, wordList: List[str]) -> int:
        def is_one_letter_different(string1: str, string2: str) -> bool:
            count = 0
            for s1, s2 in zip(string1, string2):
                if s1 != s2:
                    count += 1
                    if count > 1:
                        return False
            
            return count == 1
        

        frontier = deque([beginWord])
        visited = set([beginWord])
        num_words = 1
        while frontier:
            num_frontiers = len(frontier)
            for _ in range(num_frontiers):
                word = frontier.popleft()

                if word == endWord:
                    return num_words
                
                for candidate in wordList:
                    if is_one_letter_different(word, candidate) and candidate not in visited:
                        visited.add(candidate)
                        frontier.append(candidate)
            
            num_words += 1
        
        return 0
```

同じwordを何度も探索しないようにするため、一度使用したwordを再利用しなければよいと考えた。
forループ中に wordList を直接変更（要素の削除）できないかと考えたが、forループ中にリストを変更するとバグの温床になりそうだと思い、手が止まった。
他の人の解答を見てみる。



### 他の人のコードを読む
1) https://github.com/rimokem/arai60/pull/20
- たくさん参考にさせてもらいました。ありがとうございます。
- 1-1) list(wordList) でコピーを作成し、そのコピーを走査すれば、リストを変更しても問題ないことが分かった。
- 自分で書いたコードを変更するなら

```py
                for candidate in list(wordList):
                    if is_one_letter_different(word, candidate) and candidate not in visited:
                        visited.add(candidate)
                        frontier.append(candidate)
                        wordList.remove(candidate)
``` 
- になる。
- ただし、実行時間はwordListの内容に依存するため、実行時間の遅さが解消されたとは言い難い。
    - 極端な例として、beginWordと近いword（1文字違いのword）が多い場合、wordListへのアクセスはwordListの長さくらいで済む。
    - 一方で、beginWordから少ない変換回数では到達できないword（異なる文字が多いword）が多い場合、wordListへのアクセス回数は修正前のコードに近づく。

- 1-2) 別の方法を読んだ。wordListを走査する代わりに、一文字違いがわかるハッシュテーブルを作成し、それを参照する方式で行っていた。これはよさそう。
- ハッシュテーブルの作成方法：各文字列のi文字目を除去したパターンをキーにして、同じパターンを持つ文字列をグループ化する。
- 例: 
- `beginWord = "hit", wordLsit = ["hot","dot","dog","lot","log","cog"]`とする。

- hotをハッシュテーブルに追加すると
```text
{
"*ot": ["hot"],
"h*t": ["hot"],
"ho*": ["hot"]
}
```

- dotをハッシュテーブルに追加すると
```text
{
"*ot": ["hot", "dot"],
"h*t": ["hot"],
"ho*": ["hot"],
"d*t": ["dot"],
"do*": ["dot"]
}
```
- (以下同様に作成する)

- 探索時には、現在のwordから同様にパターンを生成し、それをkeyとしてハッシュテーブルを参照する。
- 例えば、beginWordであるhitに対して、 `"*it", "h*t", "hi*"`のkeyを引くと一文字違いのものが出てくる。
- 頭いい...。

- とりあえず、このアイデアさえあれば、解けそうなのであとは自力で書いてみる。
- 重複探索を避けるために二つの工夫をいれる。
- 一つ目は同じwordを再度探索しないこと、二つ目は一度参照したパターンに対応するハッシュテーブルの値を空にすることである。

重複を避けない場合、以下のような挙動になる。
- `beginWord = "hit", wordLsit = ["hot","dit", "hid", "did"], endWord = "did"`を入力する。そのとき、以下のハッシュテーブルが生成される。
```text
{
"*ot": ["hot"],
"h*t": ["hot"],
"ho*": ["hot"],
"*it": ["dit"],
"d*t": ["dit"],
"di*": ["dit", "did"],
"*id": ["hid", "did"],
"h*d": ["hid"],
"hi*": ["hid"]
"d*t": ["dot"],
"d*d": ["did"]
}
```
このハッシュテーブルを用いて探索を行う。

【hitの探索】
"*it" -> "dit"
"h*t" -> "hot"
"hi*" -> "hid"


【dit, hot, hidの探索】
"*it" -> "dit" (同じハッシュテーブルを参照している。また、次の探索候補にditが再度入る。)
"d*t" -> "dit"
...

これに対して、hitの探索時に、ハッシュテーブルを空にしておくと、ハッシュテーブルは以下のようになる。

```text
{
"*ot": ["hot"],
"h*t": [],
"ho*": ["hot"],
"*it": [],
"d*t": ["dit"],
"di*": ["dit", "did"],
"*id": ["hid", "did"],
"h*d": ["hid"],
"hi*": []
"d*t": ["dot"],
"d*d": ["did"]
}
```
また、探索したwordは探索済の印をつけておく。そうすれば、次の探索は以下のようになる。

【dit, hot, hidの探索】
"*it" -> [] 
"d*t" -> "dit" (こちらはいったんditが候補に入るが、次の探索では除外される。)
...

**実行時間の見積もり**
M - beginWord.length
L = wordList.length
- 1 <= L <= 10
- 1 <= N <= 5000
ハッシュテーブルの構築時間: wordListを前から走査しながら、wordの文字列長だけkey-valueを作成するので、5*10^4くらい(L * N)
探索は最大で N 回で書く操作でwordも文字列長だけkey-value検索をするから5*10^4くらい(L * N)
トータルで10^5くらい
Pythonの実行ステップを10^7回/秒と仮定すると、数十ミリ秒かかる。

```py
class Solution:
    def ladderLength(self, beginWord: str, endWord: str, wordList: List[str]) -> int:
        if endWord not in wordList:
            return 0

        def generate_pattern(word: str, i: int) -> str:
            return word[ : i] + "*" + word[i + 1 : ]
            
        pattern_to_words = defaultdict(list)
        for word in wordList:
            for i in range(len(word)):
                pattern = generate_pattern(word, i)
                pattern_to_words[pattern].append(word)
        
        distance = 1
        frontier = deque([(beginWord, distance)])
        visited = set([beginWord])
        while frontier:
            word, distance = frontier.popleft()
            if word == endWord:
                return distance
            
            for i in range(len(word)):
                pattern = generate_pattern(word, i)
                neighbors = pattern_to_words.pop(pattern, [])
                for neighbor in neighbors:
                    if neighbor in visited:
                        continue
                    visited.add(neighbor)
                    frontier.append((neighbor, distance + 1))
        return 0
```
-上記のコードを書くときに気を付けた細かい点は以下のとおり。 
 - wordListにendWordがなければ早期リターンする。
 - frontierにditanceをいれる。
 - スライスのスペースのとりかたはhttps://peps.python.org/pep-0008/#whitespace-in-expressions-and-statementsを参考にした。これを見たくなったのはいい傾向。



- 1-3) rimokenさんのstep3のコードと比較
- おおむね同じだが、patternの生成方法がスマート。書き方がスマートなのと、"*"を使わない、patternのkeyの表現方法が良いと思った。
```py
def generate_patterns(word: str) -> Iterator[tuple[str, str]]:
            for i in range(len(word)):
                yield (word[:i], word[i + 1 :])
```
- と書いておいて、
```py
for pattern in generate_patterns(word):
```
- のように呼び出す。自分で書いたコードにいれるなら、こんな感じ（pattern の keyの表現方法は変えていない）
```py
class Solution:
    def ladderLength(self, beginWord: str, endWord: str, wordList: List[str]) -> int:
        def generate_patterns(word: str) -> Iterator[tuple[str, str]]:
            for i in range(len(word)):
                yield (word[:i] + "*" + word[i + 1 :])

        pattern_to_words = defaultdict(list)
        for word in wordList:
            for pattern in generate_patterns(word):
                pattern_to_words[pattern].append(word)
        
        distance = 1
        frontier = deque([(beginWord, distance)])
        visited = set([beginWord])
        while frontier:
            word, distance = frontier.popleft()
            if word == endWord:
                return distance
            
            for pattern in generate_patterns(word):
                neighbors = pattern_to_words.pop(pattern, [])
                for neighbor in neighbors:
                    if neighbor in visited:
                        continue
                    visited.add(neighbor)
                    frontier.append((neighbor, distance + 1))
        return 0
```

こんな書きかたができることは初めて知った。`Iterator`のような書き方は使いそうなので、慣れておいたほうがよさそう。

2) https://github.com/atmaxstar/coding_practice/pull/3
- 上記のPRのstep2では、wordListを走査する代わりに、あり得る文字列の候補を列挙する方法を採用した。
- なるほど。文字列の長さが短い場合はこちらのほうが速くなりそう。今回は文字列の最大長が10で、アルファベット（小文字）の種類が26なので、最大でも260通りの候補を確認すればよい。wordListの長さは最大5000なので早くなる。

3) https://github.com/yumyum116/LeetCode_Arai60/pull/17
- f文字列を使えば、文字列をつなぐ処理はすっきり書けると思った（以前も同じコメントをもらったのを思いだした）。
- `f"{word[ : i]}*{word[i + 1 : ]}"`と書く。


4) コメント集
- `pattern = word[ : i] + "*" + word[i + 1 : ]`が二か所あるのが、気になるというコメント。
- https://discord.com/channels/1084280443945353267/1303605021597761649/1306562757315002389
> うーん、上のコードが二箇所あってあまり好みではないです。
> WordNeighbors クラスを定義して、add_word(word) と get_neighbors(word) を定義し、get_neighbors が generator を返すとかにしたいですね。

> Python ならば、ペアをキーにする (word[:i], word[i+1:]) ほうがいいかもしれません。

一文字違いの文字列を生成する、という関数はWord Ladder特有の処理ではなさそうなので、クラスで定義するのも自然な気がしてきた。
この辺りを参考に書いてみる。

https://discord.com/channels/1084280443945353267/1303605021597761649/1306631474065309728

```py
class WordNeighbors:
    def __init__(self) -> None:
        self.pattern_to_neighbors = defaultdict(list)
    
    def generate_pattern(self, word: str) -> Iterator[Tuple[str, str]]:
        for i in range(len(word)):
            yield (word[ : i], word[i + 1 : ])
    
    def add(self, word: str) -> None:
        for pattern in self.generate_pattern(word):
            self.pattern_to_neighbors[pattern].append(word)
    
    def get_neighbors(self, word: str) -> Iterator[str]:
        for pattern in self.generate_pattern(word):
            for neighbor in self.pattern_to_neighbors[pattern]:
                yield neighbor

class Solution:
    def ladderLength(self, beginWord: str, endWord: str, wordList: List[str]) -> int:
        if endWord not in wordList:
            return 0
        
        neighbors = WordNeighbors()
        for word in wordList:
            neighbors.add(word)
        
        distance = 1
        frontier = ([(beginWord, distance)])
        visited = set([beginWord])
        while frontier:
            next_frontier = []
            for word, distance in frontier:
                if word == endWord:
                    return distance
                
                for neighbor in neighbors.get_neighbors(word):
                    if neighbor in visited:
                        continue
                    visited.add(neighbor)
                    next_frontier.append((neighbor, distance + 1))
            frontier = next_frontier

        return 0
```
