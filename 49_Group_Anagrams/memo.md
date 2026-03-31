## リンク
https://leetcode.com/problems/group-anagrams/description/

# 進め方

- 自分で考える。エラーをはかずに3回解くようになるまで書いてみる。
- 他の人のコードを見て、自分のコードと比較して修正する。
- 時間計算量を見積もる。
- https://github.com/Yuto729/LeetCode_arai60/pull/16#discussion_r2602118324

## 考え方

手作業でやるならどうなるか考える。

前から見ていって、グループをつくっていく。イメージは
- `["eat","tea","tan","ate","nat","bat"]`
- `[["eat"]] ["tea","tan","ate","nat","bat"]`
- `[["eat","tea"]] [,"tan","ate","nat","bat"]`
- `[["eat","tea"], ["tan"]] ["ate","nat","bat"]`
- `[["eat","tea","ate"], ["tan"]] ["nat","bat"]`
- `[["eat","tea","ate"], ["tan","nat"]] ["bat"]`
- `[["eat","tea","ate"], ["tan","nat"], ["bat"]]`

- 後は、同じ文字から構成されていることを判定するのかを考える。
- 判定方法は、比較する二つの文字列の文字と出現回数をカウントしておいて、一致するかにみる。もしくは、文字列をソートして一致するかどうか見る。後者で書いてみる。

**実行ステップと処理時間の見積もり**

- n = 文字列の配列の大きさ（最大 10⁴）
- k = 各文字列の長さ（最大 10^2）

- すべての文字列を順番に処理する必要があるため、まず文字列の個数に比例した回数の処理が発生する。（約 10⁴ 回）
- 各文字列については、それをどのグループに入れるかを決めるために、既に存在しているすべてのグループと比較する必要がある。最悪の場合、すべての文字列が異なるグループに属するため、全体の比較回数は1 + 2 + 3 + … + 10^4 ≈ 5 × 10^7 回程度 となる。(一回ループあたりの平均は 5 × 10^3)
- さらに、各比較では2つの文字列が同じ文字から構成されているかを判定する必要があり、そのために文字の出現回数を数える処理が必要になる。この処理は文字列の長さに比例した時間がかかる。（1回の比較あたり 最大 10^2 回程度）
- これらを掛け合わせると、全体の実行ステップ数は最大で
5 × 10^7 × 10^2 =  5 × 10^9 回程度 になる。
- Pythonが10^7/秒くらいの実行ステップだとすると、約5 × 10^2秒くらい。

```py
class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        anagram_group = {}

        for s in strs:
            is_anagram_found = False
            for key in anagram_group:
                if sorted(key) == sorted(s):
                    anagram_group[key].append(s)
                    is_anagram_found = True
                    break
            if not is_anagram_found:
                anagram_group[s] = [s]
        
        return list(anagram_group.values())
```

- 書いて思ったが、sortする部分を見積もれていなかった。
- 以下のボトルネックを早くする方法を考える。
```py
            for key in anagram_group:
                if sorted(key) == sorted(s):
```

- sortの回数を減らす。もともとは、最大で 5 × 10^7 回程度sortしていたが、各文字列ごとに1回だけsortするようにすれば、sortの回数は約 10^4 回程度まで削減できる。10^3倍くらい早くなるので最大でも数百ミリ秒程度になる。
やり方は、文字列をsortした結果を辞書のキーとして用い、そのキーに対応するリストに元の文字列を追加する。。

```py
class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        anagram_group = {}

        for original_string in strs:
            sorted_string = "".join(sorted(original_string))
            if sorted_string in anagram_group:
                anagram_group[sorted_string].append(original_string)
            else:
                anagram_group[sorted_string] = [original_string]
                
        return list(anagram_group.values())
```


## 他の方の解答を見てみる。

https://github.com/Kazuuuuuuu-u/arai60/pull/15/changes

defaultdictを使うとシンプルに書ける。
確かにそう。

```py
class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        anagrams_group = defaultdict(list)

        for original_string in strs:
            sorted_string = "".join(sorted(original_string))
            anagrams_group[sorted_string].append(original_string)
        
        return list(anagrams_group.values())
```


https://discord.com/channels/1084280443945353267/1337642831824814192/1344303950257721365
> また、入力が、小文字アルファベットでないものが来たときに、どのような振る舞いをするか、どのような振る舞いをするべきかは追加質問が来てもおかしくないでしょう。

この辺りは、常に意識しつつ、[over-engineering](https://google.github.io/eng-practices/review/reviewer/looking-for.html#complexity)には気を付ける。
