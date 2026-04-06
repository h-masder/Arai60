## 問題へのリンク
https://leetcode.com/problems/intersection-of-two-arrays/description/

## 進め方

- 自分で考える。書く前に時間計算量を見積もる(https://github.com/Yuto729/LeetCode_arai60/pull/16#discussion_r2602118324)。エラーをはかずに3回解くようになるまで書いてみる。
- 他の人のコードを見て、自分のコードと比較して修正する。

## 自分で考える

### 考え方

1) 問題文にある通りにemailを加工する。
- `@`でemailを分割する(`@`は一つになっている。)
- local name において：
- `.` は無視する
- `+` が現れた場合、それ以降`@`までの文字列は無視する
- domain name において：
- `.` や`+`はそのまま扱う

- 異なるものが何個あるのか数える。
以下の条件が必要。

ここでは、`.`、`+`、`@`、今文字の英語が出てくる個数に制限はない。
local name の中にdotがあったら、スキップする。
local name の中に+があったら、次の@までスキップする。
domin nameの中にdotがあったら、そのままにする。
domain nameの中にplusがあったらinvalidとする。


```py
class Solution:
    def numUniqueEmails(self, emails: List[str]) -> int:
        unique_emails = set()

        for email in emails:
            local_name, domain_name = email.split('@')
            local_name = local_name.split('+')[0]
            local_name = local_name.replace('.', '')
            processed_email = local_name + '@' + domain_name
            unique_emails.add(processed_email)
        
        return len(unique_emails)
```

今回の問題では、emailの文字列に以下の制約が与えられている。

> - 1 <= emails.length <= 100
> - 1 <= emails[i].length <= 100
> - emails[i] consist of lowercase English letters, '+', '.' and '@'.
> - Each emails[i] contains exactly one '@' character.
> - All local and domain names are non-empty.
> - Local names do not start with a '+' character.
> - Domain names end with the ".com" suffix.
> - Domain names must contain at least one character before ".com" suffix.

これらの制約は問題側で保証されているが、実務では自前でバリデーションを行うケースも考えられる。
例えば、2つ目の制約（1 <= emails[i].length <= 100）をチェックする場合は、以下のように実装できる。
```py
class Solution:
    def numUniqueEmails(self, emails: List[str]) -> int:
        unique_emails = set()

        for email in emails:
            self._validate_email(email)
            local_name, domain_name = email.split('@')
            local_name = local_name.split('+')[0]
            local_name = local_name.replace('.', '')
            processed_email = local_name + '@' + domain_name
            unique_emails.add(processed_email)
        
        return len(unique_emails)
    
    def _validate_email(self, email: str):
        if len(email) > 100:
            raise ValueError("Email length must be at most 100 characters")

        #以下の必要に応じてチェックを追加
```
RFC5321だとThe maximum total length of a reverse-path or forward-path is 256 octets (including the punctuation and element separators).とのことらしい。
これ、たくさん制約はあるが、実務だと全部チェックしたりするものなのだろうか。


## 他の人のコードを見る。

1) https://discord.com/channels/1084280443945353267/1200089668901937312/1207996784211918899
- ステートマシンで解くアプローチ  
- これでもいいが、拡張していくと複雑になりそう。

2) https://github.com/akmhmgc/arai60/pull/11#discussion_r2311995496
- この問題ではどんなことが見えているとよいか
- メールアドレスのバリデーションは、RFCに忠実に従おうとすると、とても複雑になる（https://www.regular-expressions.info/email.html）。
- 実用上は「ある程度をカバーする簡易な正規表現」を使うのが現実的だと感じたが、どうするのがいいのかよくわからない。冒頭で紹介されているものが無難なのだろうか。 
- もし、これがメールの登録に使われてるのなら、やはりセキュリティ（インジェクション）の観点のバリデーションは欲しいと感じる。文字の種類制限と文字列の長さ制限を書けるのは有効そう。
- あとは、バリデーション結果に応じて、システムがどう振る舞うかが重要。例えば、一斉送信のような用途では、無効なメールアドレスが含まれていても処理全体は止めずにスキップして継続する方が望ましいケースもある。
