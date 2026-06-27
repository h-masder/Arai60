# 問題文
- https://leetcode.com/problems/generate-parentheses/description/

- Given n pairs of parentheses, write a function to generate all combinations of well-formed parentheses.
- Example 1:
- Input: n = 3
- Output: ["((()))","(()())","(())()","()(())","()()()"]

- Example 2:
- Input: n = 1
- Output: ["()"]
 
 - Constraints:
- 1 <= n <= 8


# アプローチ
- 以下のような木を構築して、葉を全部まとめてリターンすればよい。

```text
                                      (
                         ┌────────────┴────────────┐
                         │                         │
                        ()                        ((
                         │                  ┌─────┴─────┐
                        ()(               (()         (((
                  ┌──────┴──────┐     ┌────┴────┐        │
                  │             │     │         │        │
               ()()          ()((   (())     (()(      ((()
                  │             │      │         │         │
                  │             │      │         │         │
               ()()(        ()(()   (())(    (()()     ((())
                  │             │      │         │         │
                  │             │      │         │         │
              ()()()       ()(())  (())()   (()())    ((()))
```

- 木の構築方法
  - "(" と ")" の残りの使用回数を保持しながら、かっこを追加していく。
    - remaining_open_parentheses: 使用可能な "(" の残り回数
    - remaining_close_parentheses: 使用可能な ")" の残り回数

  - "(" と ")" の両方を追加できる場合は、現在のノードから
    - "(" を追加した子ノード
    - ")" を追加した子ノード
    の2通りに分岐する。

  - どちらか一方しか追加できない場合は、そのかっこのみを追加した子ノードへ進む。

  - `remaining_open_parentheses` と `remaining_close_parentheses` の両方が 0 になったら葉ノードに到達しており、その時点で完成したかっこ列となる。

**実行時間の見積もり**
- 木の高さは `2n`。各ノードから最大2通りに分岐する。
- そのため、探索するノード数は最大で `O(2^(2n)) = O(4^n)` となる。 
  - 実際には1通りしか分岐しないノードもあるため、探索するノード数はこれより少ない。
- この問題では `n <= 8` なので、`4^8 = 65,536` である。
- 葉に到達するたびに文字列を構築する。文字列の長さは高々 `2n = 16` なので、文字列構築にかかる処理は多く見積もっても 65,536 × 16 = 1,048,576
- トータルで65,536 + 65,536 × 16くらいで、Python は1秒あたり約 10^7 ステップ実行できるとすると、約100msくらい。

```py
class Solution:
    def generateParenthesis(self, n: int) -> List[str]:
        parentheses = []
        # state: (parentheses_sequence, remaining_open_parentheses, remaining_close_parentheses)
        states = [(['('], n - 1, 1)]
        while states:
            parentheses_sequence, remaining_open_parentheses, remaining_close_parentheses = states.pop()
            if remaining_open_parentheses == 0 and remaining_close_parentheses == 0:
                parentheses.append("".join(parentheses_sequence))
                continue
            
            if remaining_open_parentheses > 0:
                new_parentheses_sequence = parentheses_sequence + ['(']
                states.append((new_parentheses_sequence, remaining_open_parentheses - 1, remaining_close_parentheses + 1))

            if remaining_close_parentheses > 0:
                new_parentheses_sequence = parentheses_sequence + [')']
                states.append((new_parentheses_sequence, remaining_open_parentheses, remaining_close_parentheses - 1))
            
        return parentheses
```
- 再帰
```py
class Solution:
    def generateParenthesis(self, n: int) -> List[str]:
        parentheses = []
        
        def generate_parentheses(parentheses_sequence, remaining_open_parentheses, remaining_close_parentheses):
            if remaining_open_parentheses == 0 and remaining_close_parentheses == 0:
                parentheses.append("".join(parentheses_sequence))
                return
            
            if remaining_open_parentheses > 0:
                new_parentheses_sequence = parentheses_sequence + ['(']
                generate_parentheses(new_parentheses_sequence, remaining_open_parentheses - 1, remaining_close_parentheses + 1)

            if remaining_close_parentheses > 0:
                new_parentheses_sequence = parentheses_sequence + [')']
                generate_parentheses(new_parentheses_sequence, remaining_open_parentheses, remaining_close_parentheses - 1)
        
        generate_parentheses(['('], n - 1, 1)
            
        return parentheses
```

# 他の人のコードを見てコメントする。
