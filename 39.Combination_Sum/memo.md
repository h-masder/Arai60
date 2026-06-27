# 問題文
- https://leetcode.com/problems/combination-sum/

- Given an array of distinct integers candidates and a target integer target, return a list of all unique combinations of candidates where the chosen numbers sum to target. You may return the combinations in any order.
- The same number may be chosen from candidates an unlimited number of times. Two combinations are unique if the frequency of at least one of the chosen numbers is different.
- The test cases are generated such that the number of unique combinations that sum up to target is less than 150 combinations for the given input.

- Example 1:
- Input: candidates = [2,3,6,7], target = 7
- Output: [[2,2,3],[7]]
- Explanation:2 and 3 are candidates, and 2 + 2 + 3 = 7. Note that 2 can be used multiple times. 7 is a candidate, and 7 = 7. These are the only two combinations.

- Example 2:
- Input: candidates = [2,3,5], target = 8
- Output: [[2,2,2,2],[2,3,3],[3,5]]

- Example 3:
- Input: candidates = [2], target = 1
- Output: []
 

- Constraints:
- 1 <= candidates.length <= 30
- 2 <= candidates[i] <= 40
- All elements of candidates are distinct.
- 1 <= target <= 40


# アプローチ
- 与えられた候補（candidates）から、同じ数を何回使ってもよい条件で、合計が target になる組み合わせをすべて探す。
- 以下のように調査していく。(target = 7, candidates = [2,3, 6, 7]を使って説明)
- [] から開始
- 1個選ぶ → [2], [3], [6], [7]
- そこからさらに同じ or 後ろの要素だけ選ぶ
- 合計が target を超えたら打ち切り（×）
 -ちょうど target になったら解（〇）

- 注意事項としては、最初にcandidatesをソートすること、

[]
├── [2]
│   ├── [2,2]
│   │   ├── [2,2,2]
│   │   │   ├── [2,2,2,2] ×
│   │   │ 
│   │   ├── [2,2,3] 〇
│   │   
│   │    
│   │  
│   │
│   ├── [2,3]
│   │   ├── [2,3,3] ×
│   │   
│   │   
│   │
│   └── [2,6] ×
│
├── [3]
│   ├── [3,3]
│   │   ├── [3,3,3] ×
│   │
│   └── [3,6] ×
│
├── [6]
│   ├── [6,6]×
│  
│   
│
└── [7] 〇

- (木が横に長かったので、縦にしました)

**実行時間の見積もり**
- `m` を `candidates` の長さとする。
- 木の深さは高々 `target / min(candidates)`。
  - `target <= 40`、`min(candidates) >= 2` より、高々 `20`。
- 各ノードでは、高々 `m` 個の候補を試す。
  - `m <= 30`。
- よって探索木のノード数は高々 `30^20` 個となる。
- 各ノードでは、組み合わせのコピーに高々 `20` 要素コピーする。
- よって実行時間は高々 `20 × 30^20` ステップ程度となる。
- `30^20` はかなり緩い上界であり、実際にはここまで探索することはほとんどない。より正確な見積もりは難しいため、一つの方法は実際に測定すること。
- 問題文によると、テストケース全体で解の個数は高々 150 個である。その程度の探索で済むと考えると、リストのコピー（高々 20 要素）を含めても、およそ `20 × 150 = 3000` ステップ程度。
- Python の実行速度を `10^7` ステップ/秒とすると、実行時間は約300 μs程度。

```py
class Solution:
    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:
        sorted_candidates = sorted(candidates)
        all_combinations = []

        #   states are a set of (current_combination, total, index).
        #   current_combination: list of the elements selected in candidates
        #   total: sum of the current_combination
        #   index: index in candidates where next choice starts
        states = [([], 0, 0)]
        while states:
            current_combination, total, index = states.pop()
            if target == total:
                all_combinations.append(current_combination)
                continue
            if target < total:
                continue
            
            for i in range(index, len(sorted_candidates)):
                new_combination = current_combination + [sorted_candidates[i]]
                new_total = total + sorted_candidates[i]
                states.append((new_combination, new_total, i))
        
        return all_combinations
```

- 再帰
```py
class Solution:
    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:
        sorted_candidates = sorted(candidates)
        all_combinations = []

        def search_combination_sum(current_combination, total, index):
            if target == total:
                all_combinations.append(current_combination)
                return
            if target < total:
                return
            
            for i in range(index, len(sorted_candidates)):
                new_combination = current_combination + [sorted_candidates[i]]
                new_total = total + sorted_candidates[i]
                search_combination_sum(new_combination, new_total, i)
        
        search_combination_sum([], 0, 0)
        return all_combinations
```

- backtracking
```py
class Solution:
    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:
        sorted_candidates = sorted(candidates)
        all_combinations = []

        def search_combination_sum(current_combination, total, index):
            if target == total:
                all_combinations.append(current_combination.copy())
                return
            if target < total:
                return
            
            for i in range(index, len(sorted_candidates)):
                current_combination.append(sorted_candidates[i])
                new_total = total + sorted_candidates[i]
                search_combination_sum(current_combination, new_total, i)
                current_combination.pop()
        
        search_combination_sum([], 0, 0)
        return all_combinations
```

# 他の人のコードを見る。
取りあえず、次の問題(Generate Parentheses)が同じような問題なので、それを解くことにする。
