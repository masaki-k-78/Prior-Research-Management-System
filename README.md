#### 過去に読んだ論文等をまとめておけるシステムを作りたい
* 機能
    * 論文の追加
    * 論文の名前検索機能(部分一致)
    * 同じ著者の論文を探す機能
    * 一覧を見る機能
    * (論文の概要が読める機能)
    * (輪講を行っていたら，その時の日時と誰が行ったかがわかる機能)
    * (論文にキーワードをつけておき，それによって分類する機能)

* 予定（数字はやる順番）
    * 今はCSVで保存しているが，MySQLを使う．(完了)
        * Webアプリケーションのログインシステムができ次第統合する予定．
    * flaskを用いてWebアプリケーションにする．
        * メインページ（完了）
        * ログインページ（完了だけどまだやることある）
        * ログアウトページ(3)
        * サインアップページ（完了だけどまだやることある）
        * 個人のページ（1）
    * ユーザ認証と，それぞれのデータベースを作る．
        * ユーザーの追加：userの中にテーブルを作成，その中にユーザー情報を保存（完了）
        * ユーザーを追加した際に，prior_researchの中に個人のテーブルを作成（完了）
        * ユーザーごとのデータベース：prior_researchの個人のテーブルの中に論文データを保存(2)
    * .envを使ってMySQLのパスワードをソースコードに載せない．(完了)

* 学びポイント
    * flaskはMySQLよりもsqlAlchemyの方が相性が良いみたい
        * 今回はせっかくなのでMySQLを使う
    * FlaskFormを継承して作ったFormを使うといろいろ便利
        * HTMLのFormの作成や，エラー処理，データのやり取り．．．
    * flask_loginは優秀っぽい
    * 下手に真似しようとしても使ってるDB次第で全然処理が違うことがある
    * POST送信の時は@app_routeにしっかりとmethodsをかく
    * CSRFなるものがある，tokenでの対策が必須らしい
