# TrainNotify

機能：1分ごとにJR東日本、小田急線のサイトを覗いて遅延情報があればメールを送信します。

必要な物：
python動作環境
lxml
requests
yahooのメールアドレス

settings.ini
[smtp]
fromにメールアドレス、passにパスワード
[settings]
toに送信先メールアドレス(|で区切って複数指定可能)
notifyにクローリングする路線(|で区切って複数指定可能)

を入れてください。
