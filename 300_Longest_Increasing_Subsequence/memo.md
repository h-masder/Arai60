## 問題
https://leetcode.com/problems/longest-increasing-subsequence/description/

Given an integer array nums, return the length of the longest strictly increasing subsequence.
Constraints:

1 <= nums.length <= 2500
-104 <= nums[i] <= 104

## 進め方
- 最近いろいろなやり方を模索しています。かなり迷走していますが、ひとまずこれでやります。
  - (step1)問題を見た際に、考えられるアプローチを列挙し、それぞれの計算量を検討する。思いついた方法でコードで表現する。さくっと書けない場合は、他者のコードや生成AIを参考にし、なぜ書けなかったのかを分析して次に活かす。それぞれのコードで3回エラーを出さずに書く。
    - 計算量の見積もりについてのコメント: https://github.com/Yuto729/LeetCode_arai60/pull/16#discussion_r2602118324
  - (step2)他の人のコードや生成AIを参照し、他のアプローチをコードで表現する。それぞれのコードで3回エラーを出さずに書く。
  - (step3)その後、他の人のPRをコードレビューする(PRにコメントを残す)。ここで確認したいのは、この問題の練習会を開き講師としてふるまえるか。
    - レビューの仕方: https://google.github.io/eng-practices/review/reviewer/looking-for.html
      - コードレビューは、デザイン、実装、テスト、コーディングスタイルの順に重要。
      - 最終的には、どのPRを見ても他者のコードを素早く理解し、頭の中で実行して妥当性を判断し、必要に応じて修正提案ができる状態を目指す。

## アプローチ

- 簡単な例をいくつか紙に書いた。候補を作り、最後に一番長いものを返す。
- 候補となる部分列のリストの更新をうまくコードに落とし込めなかった。入出力が一致しないような入力例が見つかる。
- 結局、全部持つ方法しか実装はできなかった。

```py
from typing import List
class Solution:
    def lengthOfLIS(self, nums: List[int]) -> int:
        candidates = []
        for num in nums:
            new_candidates = []
            for candidate in candidates:
                if candidate[-1] < num:
                    new_candidates.append(candidate + [num])
            new_candidates.append([num])
            candidates.extend(new_candidates)
        
        return max(len(candidate) for candidate in candidates)
```

- 実行時間
- 処理が一番かかるのはcandiatesのアクセス回数。これはappendの数だけ増える。
  - appendの総数が一番多いのはすべての i < j で nums[i] < nums[j]
    - (次のcandidateの数) = (前のcandidateの数) * 2 + 1
    - 1 <= nums.length <= 2500なのでcandidatesが大きくなりすぎて、とても処理できない。



- 生成AIに上記のリストの管理を簡単にできないか相談した。以下のようにするとよいようだ。
- リストの i 番目には、「長さ i+1 の増加部分列のうち、末尾が最も小さい値」を入れる
  - リストには実際の部分列そのものは記録しない、イメージは一番に長くなりそうな状態を記録している
- 新しい数 num が来たら、入れ替えられる場所を探して更新する
- 最終的にリストの長さをreturnする。

- 例えば、[5, 6, 7, 0, 1]を入力としたときを考える。
- 5を見た後、リストは[5]
- 6を見た後、リストは[5, 6] (これは、[5, 6]という部分列を保持しているわけではない)
- 7を見た後、リストは[5, 6, 7]
- 0を見た後、リストは[0, 6, 7]
- 1を見た後、リストは[0, 1, 7]
- 最終的にリストの長さである3をreturnする。

```py
from typing import List
class Solution:
    def lengthOfLIS(self, nums: List[int]) -> int:
        tails = []  # tails[i]: among all increasing subsequences of length i+1, the mininum last value(tail)
        for num in nums:
            is_inserted = False
            for i in range(len(tails)):
                if num <= tails[i]:
                    tails[i] = num
                    is_inserted = True
                    break
            if not is_inserted:
                tails.append(num)

        return len(tails)
```
- 変数名はどうしても思いつかず、コメントアウトで補うことにした。
- 他にいい方法はないかdiscordを調べていたところ、異なる解法に関するもので、以下のコメントを発見した

- > うーん、読みにくいと思ったんですが、理由がlengthsの意味がパズルになっているからだと思いました。
- > 日本語で長々と書くと、「lengths[i] とは、仮に nums[i] がシーケンスの最後であると仮定した場合に可能な、最も長いシーケンスの長さ」ですよね。まあ、「長さ(複数)」であることには間違いないですが、「長さ」とだけいわれて、ああ「仮に nums[i] がシーケンスの最後であると仮定した場合に可能な、最も長いシーケンスの長さ」ってことね、とならず、それを推測するパズルになっています。これを前提とすると、内側のループは、関数にすることができるはずで、「i よりも左で、nums[i] 未満で終わる最大のシーケンスの長さ」を返させればいいですね。

- 関数にする、変数名にしっかりと書く、もしくはコメントするかのどれかで対応する。あとは、他の人に相談する。

```py
from typing import List
class Solution:
    def lengthOfLIS(self, nums: List[int]) -> int:
        def try_to_replace_first_greater_or_equal_tail(num: int) -> bool:
            for i in range(len(minimum_tail_for_each_length)):
                if num <= minimum_tail_for_each_length[i]:
                    minimum_tail_for_each_length[i] = num
                    return True
            return False

        # minimum_tails_for_each_length[i]: among all increasing subsequences of length i + 1, the minimum tail value.
        # This list does not store the actual subsequences. It stores the most extendable tail for each length.
        minimum_tail_for_each_length = []

        for num in nums:
            # Try to replace an existing tail with num, to keep a smaller and more extendable tail.
            is_replaced = try_to_replace_first_greater_or_equal_tail(num)

            if not is_replaced:
                # num is larger than every existing tail, so a longer increasing subsequence can be created.
                minimum_tail_for_each_length.append(num)

        return len(minimum_tail_for_each_length)
```
- かなり悩みましたが、こんな感じにしました。

## 他の人のコードをみる。コメントも残す。
- https://github.com/Manato110/LeetCode-arai60/pull/32/ の"書いたコード1"
- numsを前から順に走査する。各nums[i]に対し、nums[i]を末尾とする最長増加部分列の長さ（ここでは仮に"A"とする）を記録すればよい。
- returnするのは、記録したものの中で数値が一番大きいもの。

- 例えば、nums = [5, 6, 7, 0, 1]を入力としたときを考える。
- Aの内容は以下のように更新される。
-  初期状態: [1, 1, 1, 1, 1]
- 5を見た後: [1, 1, 1, 1, 1]
- 6を見た後: [1, 2, 1, 1, 1]
- 7を見た後: [1, 2, 3, 1, 1]
- 0を見た後: [1, 2, 3, 1, 1]
- 1を見た後: [1, 2, 3, 1, 2]

- (引用したコメントはこの解法に関することのようだ。)
- これも考えてみる。

```py
from typing import List
class Solution:
    def lengthOfLIS(self, nums: List[int]) -> int:
        # maximum_lengths_ending_at_each_index[i]:
        # the length of the longest increasing subsequence ending at nums[i]
        maximum_lengths_ending_at_each_index = [1] * len(nums)

        def try_to_extend_previous_increasing_subsequences(i: index, num: int) -> None:
            for j in range(i):
                previous_num = nums[j]
                if previous_num < num:
                    maximum_lengths_ending_at_each_index[i] = max(
                        maximum_lengths_ending_at_each_index[i],
                        maximum_lengths_ending_at_each_index[j] + 1
                    )

        for i, num in enumerate(nums):
            try_to_extend_previous_increasing_subsequences(i, num)

        return max(maximum_lengths_ending_at_each_index)
```

- この問題をどうコードに落とし込むかはかなり悩んだので、一旦ここで区切って、コメントをいただいてからもう少し考えたいと思います。
- よろしくお願いいたします。
