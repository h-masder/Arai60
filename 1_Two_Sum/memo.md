## リンク
https://leetcode.com/problems/two-sum/description/

# 進め方

- 自分で考える。エラーをはかずに3回解くようになるまで書いてみる。
- 他の人のコードを見て、自分のコードと比較して修正する。
- 時間計算量を見積もる。
- https://github.com/Yuto729/LeetCode_arai60/pull/16#discussion_r2602118324

## 考え方

- nums[0]+nums[1], nums[0]+nums[1], ..., nums[0]+nums[len(nums)-1], nums[1]+nums[2],...のように順番にみていく。

**実行ステップ数と処理時間**
- `nums.length<=10^4`
- 二重ループを回すので実行ステップは 10^8 回くらい。
- Python（10^7 ステップ/秒くらい）だと数秒かかる


```py
class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        for i in range(len(nums)):
            for j in range(i + 1, len(nums)):
                if nums[i] + nums[j] == target:
                    return [i, j]
        return None
```
出題意図とは違うだろう。
ソートしてあれば、もう少し簡単な方法があるかもしれない。思いつかず。

## 他の人の解答も見る。

- (1)HashMapを使う方法
- 他の人の解答をざっと見たときに、HashMapを使う、、、という文章を見た。、自分の解答と近い考え方でもっと早くする方法は、線形探索をやめることだと気づいたので、それで書いてみる。

- 配列を先頭から順に見ていく
- 各要素 num に対して、target - numを計算する
- その値がこれまでに見た要素の中にあれば、対応するインデックスと一緒に返す
- なければ、現在の要素を記録して次に進む

**ポイント**

- やりたいこと自体は、自分の解法と同じ。
- 「その値がこれまでに見た要素の中にあれば」を線形探索ではなく、HasMapを使って、O(1)で確認する点が実行ステップ数を削減するポイント


**実行ステップ数と処理時間**
- `nums.length<=10^4`
- `nums`を一度だけ最初から最後までみるので、実行ステップは 10^4 回くらい。
- Python（10^7ステップ/秒くらい）だと1ミリ秒くらいかかる。

```py
class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        visited = {}
        for i, num in enumerate(nums):
            complement = target - num
            if complement in visited:
                return [visited[complement], i]
            visited[num] = i
        
        return []

```


- (2)ソートする方法
- https://github.com/dorxyxki/arai60/pull/11/changes

- この方のPRはいつも読みやすいし、勉強になる。ソートにする方法については、以下のようなことを引用していた。これを書いてみる。

> - https://discord.com/channels/1084280443945353267/1183683738635346001/1187326805015810089
> - 私は紙と鉛筆でやるんだったら、カードをソートして、頭と尻から辿っていくと思いますね。
> - はじめに、一番初めと一番最後に着目します。着目しているものを足します。目標よりも小さかったら、前の方の着目しているのを一つ後ろにずらします。目標よりも大きかったら、後ろの方の着目しているのを一つ前にずらします。繰り返したら見つかるはずです。

**実行ステップ数と処理時間**

- `nums.length<=10^4`
- ソートはO(nlogn)とすると、1.4×10^5 ステップくらい。
- 探索は、10ステップくらいを1ループとして、最大 10^4 回くらいのループくらい回すから10^5 くらい。全部で 2.4×10^5 ステップくらい。
- Python（10^7 ステップ/秒くらい）だと数十ミリ秒くらい。

```py
class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        sorted_num_index_pairs = sorted([(num, i) for i, num in enumerate(nums)])

        smaller_candidate_index = 0
        larger_candidate_index = len(sorted_num_index_pairs) - 1

        while smaller_candidate_index < larger_candidate_index:
            smaller_num, smaller_original_index = sorted_num_index_pairs[smaller_candidate_index]
            larger_num, larger_original_index = sorted_num_index_pairs[larger_candidate_index]

            if smaller_num + larger_num == target:
                return [smaller_original_index, larger_original_index]
            elif smaller_num + larger_num < target:
                smaller_candidate_index += 1
            else:
                larger_candidate_index -= 1
        return []
```

- (3)ペアがなかった時の返り値
- ペアがなかったときに`return []`ではなく`raise ValueError`を返していた。私自身エラーよりも空リストが返るほうが適切かと思い、今回は`return []`にしたが、一応`raise ValueError`の使い方ももう一度確認した。

- 公式ドキュメント(https://docs.python.org/3/library/exceptions.html#ValueError)は
> - Raised when an operation or function receives an argument that has the right type but an inappropriate value, and the situation is not described by a more precise exception such as IndexError.

とのこと。ポイントはan inappropriate valueで

- inappropriate: unsuitable (https://dictionary.cambridge.org/dictionary/english/inappropriate#google_vignette)
- unsuitable: not acceptable or right for someone or something; not suitable(https://dictionary.cambridge.org/dictionary/english/unsuitable)

とのこと。とのこと。not acceptable は、関数のメイン処理を行うのに適さない値のイメージなので、処理した結果として解がない場合は `return []` でもいいかなと思う。
