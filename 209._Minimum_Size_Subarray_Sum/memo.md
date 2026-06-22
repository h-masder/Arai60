# 問題文
- https://leetcode.com/problems/minimum-size-subarray-sum/description/
- Given an array of positive integers nums and a positive integer target, return the minimal length of a subarray whose sum is greater than or equal to target. If there is no such subarray, return 0 instead.
- Example 1:
- Input: target = 7, nums = [2,3,1,2,4,3]
- Output: 2
- Explanation: The subarray [4,3] has the minimal length under the problem constraint.

- Example 2:
- Input: target = 4, nums = [1,4,4]
- Output: 1

- Example 3:
- Input: target = 11, nums = [1,1,1,1,1,1,1,1]
- Output: 0

- Constraints:
- 1 <= target <= 10^9
- 1 <= nums.length <= 10^5
- 1 <= nums[i] <= 10^4

# Approach

- 前から順に、和が `target` 以上となる部分配列を探す。
- まず右端を伸ばしながら要素を加算し、部分配列の和が `target` 以上になるまで進める。
- 条件を満たしたら、その長さを候補として記録する。
- その後、左端を右へ動かして部分配列を短くしていく。和が依然として `target` 以上であれば、より短い部分配列が得られるため、最小長を更新する。
- 和が `target` 未満になったら再び右端を伸ばし、同じ操作を繰り返す。

# 実行時間の見積もり
- リストの各要素には高々2回ずつしかメモリアクセスしない(2 * 10^5程度)
- 各メモリアクセスでは、最小値の算出や、加減算を行う数行のコードが実行されるため、それらを数十ステップとすると、10^6程度
- Pythonの実行速度を10^7ステップ/秒とすると、数百msくらい

```py
class Solution:
    def minSubArrayLen(self, target: int, nums: List[int]) -> int:
        min_length = float("inf")
        substring_start = 0
        length = 0
        total = 0
        for num in nums:
            total += num
            length += 1
            if total < target:
                continue
            
            while target <= total:
                min_length = min(min_length, length)
                total -= nums[substring_start]
                substring_start += 1
                length -= 1
        
        return 0 if min_length == float("inf") else min_length
```


# 他の人のコードを見る
- https://github.com/kitano-kazuki/leetcode/pull/50
  - numsに負の値があったときに対応していた。
  - フォローアップとしてやってみる

- 累積和を使ってtargetより大きい区間を導く
  - prefix_sum_{i}をnums[0]からnums[i]までの合計値とする。このとき、prefix_sum{i} - nums[j] をすれば、その区間の合計が分かる(0 <= j < i)。これがtargetより大きく、かつ区間が一番短い区間を導く

**実行時間の見積もり**
- numsの各要素i ごとに、prefix_sum_{i}を計算した後、nums[0] ~ nums[i - 1]までを見るので、10^10くらいのメモリアクセスがかかる。
- Pythonの実行時間を10^7ステップ/秒とすると1000秒くらいかかる。遅い
```py
class Solution:
    def minSubArrayLen(self, target: int, nums: List[int]) -> int:
        nums_length = len(nums)
        prefix_sum = [0] * (nums_length + 1)

        min_length = float("inf")
        for i in range(1, len(prefix_sum)):
            prefix_sum[i] = prefix_sum[i - 1] + nums[i - 1]
            for j in range(i):
                if target <= prefix_sum[i] - prefix_sum[j]:
                    min_length = min(min_length, i - j)
                    
        return 0 if min_length == float("inf") else min_length
```

- さすがに、1000秒はつかいものにならないので、2重ループを取り除きたい。が思いつかず
- 生成AIと相談
  - 方針は、候補にならないものはもう見なくてよいということ
    - 1) prefix[j] - prefix[i] >= targetを満たしたら、その i は一度使ったので削除（i が左端のとき最小の長さはj一択）
    - 2) ある2つの候補 i1, i2 があってprefix[i1] >= prefix[i2] かつ i1 < i2なら i1 は不要。i2が最小になることはあってもi1が最小になることはもうない
    
```py
class Solution:
    def minSubArrayLen(self, target: int, nums: List[int]) -> int:
        n = len(nums)

        prefix_sum = [0] * (n + 1)

        for i in range(n):
            prefix_sum[i + 1] = prefix_sum[i] + nums[i]

        min_length = float("inf")
        left_candidates = deque()
        for right in range(n + 1):
            while left_candidates and target <= prefix_sum[right] - prefix_sum[left_candidates[0]]:
                left = left_candidates.popleft()
                min_length = min(min_length, right - left)

            while left_candidates and prefix_sum[right] <= prefix_sum[left_candidates[-1]]:
                left_candidates.pop()

            left_candidates.append(right)

        return 0 if min_length == float("inf") else min_length
```
