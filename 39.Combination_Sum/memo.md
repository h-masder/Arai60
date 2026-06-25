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

**実行時間の見積もり**
- 木の深さは20。なぜなら、targetは最大40でcandidates[i]の最小値が2だから。
- ただし、同じ木の深さで何回処理をするかは、targetやcandidates次第。最悪は木が深くなるごとにlen(candidates)倍ずつ増えていくので、30^20くらい。これは到底動かないが、実際は、毎回全部場合分けしないので、少なくなる。概算はちょっとわからなかったので、他の人のコードを見てみる。

```py
class Solution:
    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:
        all_combinations = []

        # state: (current_combination, total, start)
        #   current_combination: list of the elements selected in candidates
        #   total: sum of the current_combination
        #   start: index in candidates where next choice starts
        state = [([], 0, 0)]
        while state:
            current_combination, total, start = state.pop()
            for i in range(start, len(candidates)):
                new_total = total + candidates[i]
                if target < new_total:
                    continue

                new_combination = current_combination + [candidates[i]]
                if target == new_total:
                    all_combinations.append(new_combination)
                    continue

                state.append((new_combination, new_total, i))

        return all_combinations
```

# 他の人のコードを見る。
