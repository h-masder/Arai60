# 問題文
- https://leetcode.com/problems/longest-substring-without-repeating-characters/description/

- Given a string s, find the length of the longest substring without duplicate characters.

- Example 1:
- Input: s = "abcabcbb"
- Output: 3
- Explanation: The answer is "abc", with the length of 3. Note that "bca" and "cab" are also correct answers.

- Example 2:
- Input: s = "bbbbb"
- Output: 1
- Explanation: The answer is "b", with the length of 1.

- Example 3:
- Input: s = "pwwkew"
- Output: 3
- Explanation: The answer is "wke", with the length of 3.
- Notice that the answer must be a substring, "pwke" is a subsequence and not a substring.

- Constraints:
- 0 <= s.length <= 5 * 10^4
- s consists of English letters, digits, symbols and spaces.


# アプローチ
- 重複しないsubstringの左端と右端を管理するポインタを用意して、string sを前から順にみていく。最終的に最も長かったsubstringの長さを返す。
  - ポインタの更新は以下の通り
    - 重複がない場合、右端のポインタを1つだけ右にずらす。文字列の長さを1増やす。
    - 重複を見つけた場合、左端のポインタを重複した文字列が出てくるまで左にずらす

  - 重複の管理はsetを使う

**実行時間の見積もり**
- strの各要素に高々2回アクセスするので、メモリアクセスは10^5くらい。
- 各メモリアクセスではsetの追加削除文字列の長さやポイントの更新のみ。それを数十ステップとするとそうステップ数は10^6程度
- Pythonの実行速度を10^7ステップ/秒とすると、数百ms。

```py
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        seen = set()
        max_length = 0

        left = 0
        right = 0
        length = 0
        for symbol in s:
            while symbol in seen:
                seen.remove(s[left])
                left += 1
                length -= 1
            
            seen.add(symbol)
            right += 1
            length += 1
            max_length = max(max_length, length)

        return max_length
```


# 他の人のコードを読む
- https://github.com/kitano-kazuki/leetcode/pull/49
  - うえと似た解法
  
- https://github.com/naoto-iwase/leetcode/pull/49
  - findをつかった方法
```py
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        first = 0
        max_length = 0
        for last in range(1, len(s)):
            found = s.find(s[last], first, last)
            if found == -1:
                continue
            # substring is from first to last - 1
            max_length = max(max_length, last - first)
            first = found + 1
        return max(max_length, len(s) - first)
```
- `return max(max_length, len(s) - first)`が好みではない。
- `return max_length` 返してほしいと感じる。

```py
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        if not s:
            return 0
        first = 0
        max_length = 1

        for last in range(1, len(s)):
            found = s.find(s[last], first, last)

            if found != -1:
                first = found + 1

            max_length = max(max_length, last - first + 1)

        return max_length
```


- https://github.com/Manato110/LeetCode-arai60/pull/49
  - 辞書で文字列を管理する方法。
