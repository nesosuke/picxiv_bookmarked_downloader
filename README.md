# pixiv_bookmarked_downloader

## 現状

- 公開ブックマークしか取れない．
- ローカル以外に保存する機能は未実装．

## 設定ファイル

→ config.json
user_id と refresh_token を記述する．token は auth.py で取得できる．

```config.json
{
  "getAll": true,
  "user_id": "<user_id>",
  "save_to": "local",
  "save_dir": "pixiv_pics",
  "pagecount": 20,
  "max_bookmark_id": "0",
  "refresh_token": "<refresh_token>"",
  "S3_access_key": "",
  "S3_secret_key": "",
  "S3_region": "",
  "S3_bucket": "",
  "S3_path": ""
}
```

## 下準備

```shell
pip install -r requirements.txt
```

ChromeDrive を入れとく．
<https://chromedriver.chromium.org/home> から DL して chromedriver.exe を auth.py と同じディレクトリに置く．

## トークンの取得

```shell
python auth.py login
```

## 使い方

```
python get.py
```

以上．
