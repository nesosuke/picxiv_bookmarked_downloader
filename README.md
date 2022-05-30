# pixiv_bookmarked_downloader

## 現状

- 公開ブックマークしか取れない．
- ローカル以外に保存する機能は未実装．

## 設定ファイル

→ config.json
user_id と refresh_token を記述する．token は auth.py で取得できる．

## 下準備

ChromeDrive を入れとく．
<https://chromedriver.chromium.org/home> から DL して chromedriver.exe を auth.py と同じディレクトリに置く．

## トークンの取得

```
python auth.py login
```

## 使い方

```
python get.py
```

以上．
