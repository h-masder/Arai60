## 背景
- 5/24にソフトウェアエンジニアリング勉強会が開催されるということで、過去どんなことをやっているのか興味を持ち、ログを漁っていた。
- 2024年に外資it入社試験勉強会というチャンネルに動画がアップロードされていたので、見てみた(Nodeさんのyoutubeアカウントにアップロードされているもの)。
- https://www.youtube.com/watch?v=X17uNCdMVz8
- 動画の内容は、なにやら面接をしているようだった（声が遠くて聞こえず。。。）。一人の問題の出題者と一人の解答者で面接らしきものが行われていた。
- 46:00ごろからぷよぷよの問題があり、なんとなく問題を聞いていたが、どうやら最近やっている深さ優先探索や幅優先探索を使った問題に見えてきた。
- 問題の説明が終わったあたりで、自分自身が解答者になりきり緊張感がでてきたので、そのまま問題を解くことにした。

## ぷよぷよの問題設定
- 縦12マス、横6マスの長方形がある。
- 各マスは、4色のうち、どれかが入っているとする。色はR(赤)、Y(黄)、G(緑)、B(青)
- 同色が4つ隣り合っていれば、それは消えるものとしてカウントされる。隣り合っているとは、あるマスに対して上下左右の4マスのこと。斜めは隣り合っていない。
- 出題者の要求は「どこが消えるか」を出力してほしいとのことだった。

- 
- 動画にはなかった（と思う）が追加の設定として、ぷよぷよのようにマスが動いているわけではなく、すべてのマスは何らかの色で埋め尽くされていること、を仮定した。
- もしかしたら、他にも問題の設定はあったのかもしれないが、これで解くことにした。



### (step1) まず、入出力を聞いた（脳内で）。
- 今回は、「どこを消すか」は「消すエリアを返す」という要求だったとして、以下のように書いた。

```py
class Solution:
    def deleteArea(self, table: List[List[str]]) -> List[Tuple[int, int]]:
        deleteArea = []
        return deleteArea
```

### (step2)次に入力が6*12でない場合も想定するか聞いた。
- 6*12ではない入力ははじくという要求だったとして、以下を書いた。
```py
class Solution:
    def deleteArea(self, table: List[List[str]]) -> List[Tuple[int, int]]:
        num_rows = len(table)
        num_cols = len(table[0])
        if len(table) == 6 and len(table[0]):
            raise.ValueError("6*12のtableではありません")
        
        deleteArea = []
        return deleteArea
```

### (step3)その次に、大枠を書いた。以下のような感じ
```py
class Solution:
    def deleteArea(self, table: List[List[str]]) -> List[Tuple[int, int]]:
        num_rows = len(table)
        num_cols = len(table[0])
        if len(table) == 6 and len(table[0]):
            raise.ValueError("6*12のtableではありません")

        visited = set()
        def explore_table_and_is_delete_area(row: int, col: int) -> None:
             #4つ以上つながっていたら、delelte箇所としてカウントする。
        for row in range(num_rows):
            for col in range(num_cols):
                if (row, col) in visited:
                    continue
                
                explore_table_and_is_delete_area(row, col)
        
        
        deleteArea = []
        return deleteArea
```

### (step4)最後に以下のように書いた。
```py
class Solution:
    def deleteArea(self, table: List[List[str]]) -> List[Tuple[int, int]]:
        num_rows = len(table)
        num_cols = len(table[0])
        if len(table) == 6 and len(table[0]):
            raise.ValueError("6*12のtableではありません")

        visited = set()
        def explore_table_and_is_delete_area(row: int, col: int) -> None:
            #4つ以上つながっていたら、delelte箇所としてカウントする。
            visited.add((row, col))
            count = 1
            color = table[row][col]
            frontier = [(row,col)]
            visited_area = [(row, col)]
            while frontier:
                next_frontier = []
                for row, col in frontier:
                    for neighbor_row, neighbor_col in [(row + 1, col), (row, col + 1), (row - 1, col), (row, col - 1)]:
                        if table[neighbor_row][neighbor_col] == color:
                            count += 1
                            visited.add((neighbor_row, neighbor_col))
                            next_frontier.append((neighbor_row, neighbor_col))
                            visited_area.append((neighbor_ros, neighbors_col))
            if count < 4:
                return
            for ((delete_row, delete_col)) in visited_area:
                deleteArea.appen((delete_row, delete_col))

        deleteArea = []
        for row in range(num_rows):
            for col in range(num_cols):
                if (row, col) in visited:
                    continue
                
                explore_table_and_is_delete_area(row, col)

        
        return deleteArea
```

### (step5)「もう一度正しい処理かどうか確認させてください」と依頼して確認した。
- 最初からコードをみた。いろいろとおかしなことになっていたので、直した。
```py
class Solution:
    def deleteArea(self, table: List[List[str]]) -> List[Tuple[int, int]]:
        num_rows = len(table)
        num_cols = len(table[0])
        if num_rows == 6 and num_cols == 12: # (これは逆です。見直しのときには気づきませんでした。)
            raise.ValueError("6*12のtableではありません") # (ここも、間違っています。 raise と ValueErrorの間はスペースであることに見直しのときには気づきませんでした。)

        visited = set()
        def explore_table_and_is_delete_area(row: int, col: int) -> None:
            # 4つ以上つながっていたら、delelte箇所としてカウントする。
            count = 1
            color = table[row][col]
            frontier = [(row,col)]
            visited_area = [(row, col)]
            while frontier:
                next_frontier = []
                for row, col in frontier:
                    for neighbor_row, neighbor_col in [(row + 1, col), (row, col + 1), (row - 1, col), (row, col - 1)]:
                        if table[neighbor_row][neighbor_col] != color or (neighbor_row, neighbor_col) in visited: # 条件を修正した
                            continue
                        count += 1
                        visited.add((neighbor_row, neighbor_col))
                        next_frontier.append((neighbor_row, neighbor_col))
                        visited_area.append((neighbor_row, neighbor_col)) # 変数名を修正した
                frontier = next_frontier # 追記した
            
            if count < 4:
                return
            for ((delete_row, delete_col)) in visited_area:
                deleteArea.append((delete_row, delete_col))

        deleteArea = []
        for row in range(num_rows):
            for col in range(num_cols):
                if (row, col) in visited:
                    continue
                visited.add((row, col)) # explore_table_and_is_delete_area関数から移動してきた。ここはやらなくてもいい。
                explore_table_and_is_delete_area(row, col)

        
        return deleteArea
```
- おそらく、「これでいったん完成です」と宣言すると思う。
- あとは、質問にしたがって変形させる感じかな。

### メモ
- ここまでで大体20分くらいかかった。正確に測っておけばよかった。
- (step1)(step2)で7~8分くらい。入出力があいまいであることや書き出しに戸惑って、すごく時間をくった。
- (step3)(step4)で7~8分くらい。この辺りはちょっとつまりながら書いた。いいのかよくわからないけど、面接を意識して、何をしているのか声に出して書いた。
- (step5)で3分くらい（気づいていない間違いもあったが）。これも、面接を意識して、何をしているのか声に出して検証した。


## 所感
- とても緊張した。似たような問題をここ一週間くらいずっと似たような問題を解いていたのでそれっぽいコードがでてきたが、知らない問題だったらたぶん何も書けなかったと思う。
- 解答の選択肢を考える余裕があまりない。実行時間の見積もりは、「幅優先でやっても深さ優先でやっても大して差がないです。今回は幅優先で解きます」と宣言した程度。
- 最後に検証して、いろいろ間違っているのが分かった。この辺りは自然言語で整理する前に、焦ってコードを書いたことが原因かもしれない。
- 最終版の関数名も変数名も改善の余地あり。例えば、関数名が`explore_table_and_is_delete_area`となっているのは、最初はboolを返していたが後で変更した形跡が残っていた。
- 入出力があいまいであることに、自分がびっくりして、思考が止まった。普段の問題がどれだけきっちりと要求が定められているのかよくわかった。
- 面接では、気になったことは確認しながらやったほうが良い気がする。その際は、「どういう想定ですか」と聞くのではなく、こちらから選択肢を提案するとよさそう。実際の仕事でもそのほうが相手が助かるはず。「〇〇について相談があります。〇〇をケアするなら、××したり△△したりすることが考えられます。××がいいと思いますが、いかがでしょうか？」のような感じ。面接官から「別のものがいい」と言われたらそれに対応する。
- コーディング面接が、雑談する感じになるまで練習する必要があると思った。
