# 問題文
- https://leetcode.com/problems/word-break/description/
- Given a string s and a dictionary of strings wordDict, return true if s can be segmented into a space-separated sequence of one or more dictionary words.
- Note that the same word in the dictionary may be reused multiple times in the segmentation.

- Example 1:
- Input: s = "leetcode", wordDict = ["leet","code"]
- Output: true
- Explanation: Return true because "leetcode" can be segmented as "leet code".

- Example 2:
- Input: s = "applepenapple", wordDict = ["apple","pen"]
- Output: true
- Explanation: Return true because "applepenapple" can be segmented as "apple pen apple".
- Note that you are allowed to reuse a dictionary word.

- Example 3:
- Input: s = "catsandog", wordDict = ["cats","dog","sand","and","cat"]
- Output: false

- Constraints:
- 1 <= s.length <= 300
- 1 <= wordDict.length <= 1000
- 1 <= wordDict[i].length <= 20
- s and wordDict[i] consist of only lowercase English letters.
- All the strings of wordDict are unique.

# アプローチ
- 入力文字列 s の prefix が wordDict に含まれているかどうかをチェックする。
- もし含まれていれば、s からその prefix を取り除いた文字列 suffix を生成し、次はその suffix に対して同様の処理を行う。
- これを繰り返し、最終的に空文字列へ到達できれば True を返し、到達できなければ False を返す。
- 例えば、s = "applepenapple"、wordDict = ["apple", "pen"] の場合、suffix は "applepenapple" → "penapple" → "apple" → "" のように遷移できるため、True を返す。
- 空文字列には到達可能とみなし、True を返す。
- wordDict に含まれる複数の単語が prefix になる場合もあるため、探索候補の suffix はリストで管理する。
- 計算量を削減するため、一度探索した suffix は再度探索しないようにする。


**実行時間の見積もり**
- 正確な見積もりは難しいため、かなりラフに概算する。
- 探索対象となる suffix の種類数は高々 len(s) + 1 個。 (+1 は空文字列を含むため)
  - 例えば、s = "catsandog" の場合、候補となる suffix は "catsandog", "atsandog", "tsandog", "sandog", "andog", "ndog", "dog", "og", "g", "" の10個。
- 各 suffix に対して、wordDict 内の全単語について prefix かどうかを確認するため、len(wordDict) 回のチェックが必要。
- また、新しい suffix を生成する際には文字列コピーが発生するため、文字列長に比例したコストがかかる。
- 文字列長を高々 len(s) とすると、全体の計算量はおおよそ O(len(s) * len(wordDict) * len(s))。
- 制約は s.length <= 300、wordDict.length <= 1000 なので、総ステップ数はおおよそ 300 * 1000 * 300 = 9 * 10^7 程度。
- Python の実行速度を 10^7 ステップ/秒程度と仮定すると、9秒程度かかる概算になる。

```py
class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        suffixes = [s]
        checked_suffixes = set()
        while suffixes:
            suffix = suffixes.pop()
            if suffix == "":
                return True

            if suffix in checked_suffixes:
                continue

            for word in wordDict:
                if suffix.startswith(word):
                    new_suffix = suffix[len(word):]
                    suffixes.append(new_suffix)
                    
            checked_suffixes.add(suffix)

        return False
```


- 上記のコードのうち、文字列を比較する関数がないか調べて`startswith` を採用した。
  - 以下の調査を行い、文字列をコピーせずに比較を行うことができることが分かった。
    - startswith の CPython 実装を見ると、memcmp を用いて比較しており、文字列コピーは行われていないように見える。
      - 関係する関数
        - unicode_startswith_impl 関数: https://github.com/python/cpython/blob/main/Objects/unicodeobject.c#L13320
        - tailmatch 関数: https://github.com/python/cpython/blob/main/Objects/unicodeobject.c#L9651
    - 念のため簡単なコードを書き、startswith が文字列コピーをしていないか確認した。入力文字列を長くしていっても実行時間がほぼ一定であることを確認した。（一方、startswith をスライスに変更すると、実行時間は入力長に対して線形に増加した。）


- LeetCode上では3msで動いているので、実行時間の見積もりの精度がかなり悪い。
- テストの入出力が分からないので何とも言えないが、文字列のコピーが相当ラフな気がする。


- 文字列のコピーはなくてもできると思ったので修正。
- suffixを文字列の形式で管理する代わりに入力文字列 s のインデックスで管理する。
- 実行ステップは300 * 1000で3 * 10^5程度。Pythonの実行速度を10^7ステップ/秒とすると、30msくらいかかる。（これでもまだ精度は悪い）

```py
class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        suffix_indices = [0]
        checked = set()
        while suffix_indices:
            suffix_index = suffix_indices.pop()
            if suffix_index == len(s):
                return True
            
            if suffix_index in checked:
                continue
            
            for word in wordDict:
                if s.startswith(word, suffix_index):
                    suffix_indices.append(suffix_index + len(word))
            
            checked.add(suffix_index)
        return False
```

# 他の人のコードを見る。

- https://github.com/hiro111208/leetcode/pull/32
  - 末尾から見て「ここから先を辞書の語で切れるか」を`boolean_list[i]`と呼ばれるbool値のリストに記録する方法
    - これでもいいが、自分ならこう書かないかもという感想。
- https://github.com/Manato110/LeetCode-arai60/pull/40
  - 発想は同じ
  - https://github.com/Manato110/LeetCode-arai60/pull/40/changes#r3212901863
    - > visitedに入れるタイミングをstart_positionsに入れるタイミングにすると、Queueに重複した値が入ることを防げると思うので、個人的にはそちらが好みです

- 上記のコメントをもとに修正してみた。

```py
class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        suffix_indices = [0]
        checked = set()
        while suffix_indices:
            suffix_index = suffix_indices.pop()
            if suffix_index == len(s):
                return True
            
            for word in wordDict:
                if s.startswith(word, suffix_index):
                    if suffix_index not in checked:
                        suffix_indices.append(suffix_index + len(word))
            
            checked.add(suffix_index)
        return False
```

- https://github.com/attractal/leetcode/pull/28
  - 再帰で解いている。
- 自分のコードを変形させるなら、以下のような感じ
```py
class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        @lru_cache(None)
        def word_check(index):
            if index == len(s):
                return True

            for word in wordDict:
                if s.startswith(word, index):
                    if word_check(index + len(word)):
                        return True

            return False
        
        return word_check(0)
```

- https://github.com/kitano-kazuki/leetcode/pull/39
- https://github.com/tom4649/Coding/pull/37
  - Trie木による実装
  - Vitabi のアルゴリズム(https://ja.wikipedia.org/wiki/%E3%83%93%E3%82%BF%E3%83%93%E3%82%A2%E3%83%AB%E3%82%B4%E3%83%AA%E3%82%BA%E3%83%A0)
  - このあたりはいったん後回し。週末に調べる。
