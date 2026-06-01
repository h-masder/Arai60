
## リンク
https://leetcode.com/problems/find-k-pairs-with-smallest-sums/description/

# 進め方

- 自分で考える。エラーをはかずに3回解くようになるまで書いてみる。
- 他の人のコードを見て、自分のコードと比較して修正する。


> この問題は、LeetCodeを始めたときに、kitano-kazukiさんのPRを眺めたことがある。
. https://github.com/kitano-kazuki/leetcode/pull/10

#### 自分で考える

**方針**
-(1)以下のような表を考える。

| (0,0) | (0,1) | (0,2) |
| (1,0) | (1,1) | (1,2) |
| (2,0) | (2,1) | (2,2) |

- 最小は`(0, 0)`
- 次に小さい可能性（候補）があるのは、`(0, 1)`と`(1, 0)`の二つ。どちらかをいれる。
- この考え方を一般化すればよい。候補の中から最小の要素`(i, j)`を取り出し、`(i + 1, j)`と`(i, j + 1)`を候補にあげる。を繰り返す。


- この方法では、その時点では実際に選ばれない候補も含まれる
- （例：2回目の時点で `(1, 1)` が候補に入る）
- ただし、候補が漏れていなければ問題ないため、これは許容する
- 注意点：同じ `(i, j)` が重複して候補に入らないようにする

```py

class Solution:
    def kSmallestPairs(self, nums1: List[int], nums2: List[int], k: int) -> List[List[int]]:
        if nums1 is None or nums2 is None:
            return []
        if len(nums1) * len(nums2) < k:
            raise ValueError("k is out of range")
        
        k_smallest_pairs = []
        visited_pairs = set()
        candidate_pairs_ordered_by_sum = []

        heapq.heappush(candidate_pairs_ordered_by_sum, (nums1[0] + nums2[0], (0, 0)))
        visited_pairs.add((0, 0))

        for _ in range(k):
            _, (i, j) = heapq.heappop(candidate_pairs_ordered_by_sum)
            k_smallest_pairs.append((nums1[i], nums2[j]))

            if (i + 1, j) not in visited_pairs and i + 1 < len(nums1):
                heapq.heappush(candidate_pairs_ordered_by_sum, (nums1[i + 1] + nums2[j], (i + 1, j)))
                visited_pairs.add((i + 1, j))
            if (i, j + 1) not in visited_pairs and j + 1 < len(nums2):
                heapq.heappush(candidate_pairs_ordered_by_sum, (nums1[i] + nums2[j + 1], (i, j + 1)))
                visited_pairs.add((i, j + 1))

        return k_smallest_pairs
```
(結構書き間違えた。括弧のつけわすれが多い。)

-(2)重複チェックをなくすことで、コードをシンプルにする。
- `nums1` の各要素に対して、`nums2[0]` とのペア `(i, 0)` をすべて候補に入れる（各行の先頭を候補にする）
- 候補の中から最小の `(i, j)` を取り出し、次の候補には、`(i, j + 1)`を追加する。

```py
class Solution:
    def kSmallestPairs(self, nums1: List[int], nums2: List[int], k: int) -> List[List[int]]:
        if nums1 is None or nums2 is None:
            return []
        if len(nums1) * len(nums2) < k:
            raise ValueError("k is out of range")

        k_smallest_pairs = []
        candidate_pairs_ordered_by_sum = []
        for i in range(len(nums1)):
            heapq.heappush(candidate_pairs_ordered_by_sum, (nums1[i] + nums2[0], (i, 0)))
        
        for _ in range(k):
            _, (i, j) = heapq.heappop(candidate_pairs_ordered_by_sum)
            k_smallest_pairs.append((nums1[i], nums2[j]))

            if j + 1 < len(nums2):
                heapq.heappush(candidate_pairs_ordered_by_sum, (nums1[i] + nums2[j + 1], (i, j + 1)))

        return k_smallest_pairs
```


## 他の人のコメントや解答を見てみる。

https://discord.com/channels/1084280443945353267/1201211204547383386/1206515949579145216

> - 問題設定では、必ず k あるはずなんでしたっけ、でも、なかったときに
> - IndexError is raised.
> - https://docs.python.org/3/library/heapq.html#heapq.heappop
> - するわけです。
> - これ、使っている方は、びっくりしますよね。そこで、「約束にない間違った使い方をしているのだから、そいつが悪い。驚くような動作をして、デバッグで苦労していても、私の問題ではない。」というのは好まれる態度ではないでしょう。

> - 一方で、ペアが K 個なかったら、あるだけ全部小さい順に返すというのは許されたフォールバックでしょう。(たとえば、ウェブページで、項目を100件表示のときにはうまく表示されていたのに、1000件表示とした途端に全部なくなったりするのは気持ちの悪い動作です。)

> - 別に、これはこういうふうに、面接の場でコードを書かなくてはいけないというよりは、書き終わった後に、こうした方が親切な気がするというお話ができればいいと思います。

> - ああ、あと、こういうふうに息を吐くようにリファレンスを引いているというのは認識しておいてください。

- 確かにそう。そこまで頭は回っていなかった。まだまだ入出力の一致が目標になっている感じがする。書き直すなら
引数のチェックを
```py
        if k < 0:
            raise ValueError("k is out of range")
```
にして、forループの中で
```py
        if not candidate_pairs_ordered_by_sum:
            break
```
をいれるかな。もしくは、while文にして条件式にいれるとか。


(2)https://github.com/TORUS0818/leetcode/pull/12



> - まず、意図と操作の距離が遠すぎるんですね。こういうときは関数を間に挟むと意図と操作が分離できます。

うん、確かに。関数名は達成したいこと、中身は手順を書く。今回は、意図と操作の距離は遠くないと感じるのでので、分けなくてもよさそうだが、関数の使い方は意識しておく。このPRの中身は勉強になった。


## 感想

https://github.com/TORUS0818/leetcode/pull/12

を読んでいて思ったことを書いておきます。

> うーん、いや、また別の側面から話しますが、なんか旅行でも文化祭でも仕事でも道案内でも、なんでもいいんですが複数人で何かをするときに、自然言語ではどう説明してますか。
大きな目的や全体像は伝えて、それから個々の部分は局所的に分かるようにしますよね。これを足がかりに追加情報を小出しにしていって全体像を伝えます。
最終的には各部分の操作と全体の意図が噛み合った状態に見えるようになると、理解したと感じますね。

- これはただの感想ですが、「まず大きな目的や全体像を伝え、そのあとに個々の部分を順に説明する」ということが苦手な、もしくはできない人は一定数いるように思います。（もっと言えば、説明方法についてまるで意識していない人もいると思います。私自身もその一人でした。）目的を飛ばして、細かい手順から話し始めてしまいがちです。
- 私は大学院にいたときに感じたのは、こう言う説明は、当たり前のようにやってきた人ははじめからできることで、なぜできないのか不思議に思っているということです。体感ではできない人のほうが多いです（できる人2~3割くらいでしょうか）。私は全くできていませんでした。
- 大学院の5年間で何度も指導を受け、この点はかなり改善されましたが、まだ完全に身についているとは言えません。意識していないとすぐに元に戻ってしまうため、継続的に注意が必要です。
- 自分がようやく改善されてきたと感じたのは、ジャーナル論文がアクセプトされたときでした。論文を書き始めたときはどう説明すればよいかまったく見当がつきませんでした。何度も論文を書き直す過程で基礎から見直す必要を感じ、小・中学生向けの国語の本をたくさん買って読み書きを勉強しなおしました。こうしてようやく説明の仕方が分かってきて、それについて意識し始めたとき、これまでの自分がどのように物事を説明していたのか不思議に感じるようになりました。
