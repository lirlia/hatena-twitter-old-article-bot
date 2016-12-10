# 使い方（はてなブログユーザー向け）

## 必要知識

* AWS
* AWS lambda

## 環境変数

* Hatena_Blog_URL : はてなブログURL（http://lirlia.hatenablog.com/)
* Twitter_Hash_Tag : Twitterのハッシュタグ（#なし）
* Twitter_Consumer_Key : Twitter Consumer Key
* Twitter_Consumer_Secret_Key : Twitter Consumer Secret
* Twitter_Access_Token_Key : Twitter Access Token
* Twitter_Access_Token_Secret : Twitter Access Token Secret

## 使い方

上記の環境変数を指定するだけで、特定はてなブログの過去記事をランダムでTwitterアカウントでつぶやきます。

本プログラムはAWS Lambdaで動かすことを想定しています。

# License

MIT
