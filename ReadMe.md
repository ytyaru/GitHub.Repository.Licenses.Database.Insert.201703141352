# このソフトウェアについて

自作GitHubリポジトリのライセンスを取得しDBへ挿入する。

# 開発環境

* Linux Mint 17.3 MATE 32bit
* [Python 3.4.3](https://www.python.org/downloads/release/python-343/)
    * [requests](http://requests-docs-ja.readthedocs.io/en/latest/)
    * [dataset](https://github.com/pudo/dataset)
* [SQLite3](https://www.sqlite.org/index.html) 3.8.2

## WebService

* [GitHub](https://github.com/)
    * [アカウント](https://github.com/join?source=header-home)
    * [AccessToken](https://github.com/settings/tokens)
    * [Two-Factor認証](https://github.com/settings/two_factor_authentication/intro)
    * [API v3](https://developer.github.com/v3/)

# 準備

## 必要なデータベースを作成する

* [GitHub.Accounts.Database](https://github.com/ytyaru/GitHub.Accounts.Database.20170107081237765)
    * [GiHubApi.Authorizations.Create](https://github.com/ytyaru/GiHubApi.Authorizations.Create.20170113141429500)
* [GitHub.Repository.Licenses.Database.Create.201703140912](https://github.com/ytyaru/GitHub.Repository.Licenses.Database.Create.201703140912)
	* [GitHub.Repositories.Database.Create](https://github.com/ytyaru/GitHub.Repositories.Database.Create.20170114123411296)	
* [GitHub.Licenses.Database.Create.201703140852](https://github.com/ytyaru/GitHub.Licenses.Database.Create.201703140852)

## 設定

`Main.py`の以下コードで、GitHubユーザ名とDBパスを任意に設定する。

```python
if __name__ == "__main__":
	github_user_name = 'ytyaru'
	os_user_name = getpass.getuser()
	device_name = 'some_device'
	path_db_base = 'db/GitHub'
	path_db_account = '/media/{0}/{1}/{2}/GitHub.Accounts.sqlite3'.format(os_user_name, device_name, path_db_base)
	path_db_repo = '/media/{0}/{1}/{2}/GitHub.Repositories.{3}.sqlite3'.format(os_user_name, device_name, path_db_base, github_user_name)
	path_db_license = '/media/{0}/{1}/{2}/GitHub.Licenses.sqlite3'.format(os_user_name, device_name, path_db_base)
	main = Main(github_user_name, path_db_account, path_db_repo, path_db_license)
	main.Run()
```

# 実行

```dosbatch
bash ./Licenses/Create.sh
```

# 結果

* `GitHub.Licenses.sqlite3`ファイルにライセンスデータが挿入される

試しに以下のように検索した結果。

## ライセンス一覧

```sh
sqlite> select Key from Licenses;
```
```sh
agpl-3.0
apache-2.0
bsd-2-clause
bsd-3-clause
epl-1.0
gpl-2.0
gpl-3.0
lgpl-2.1
lgpl-3.0
mit
mpl-2.0
unlicense
```

## MITライセンス本文

```sh
sqlite> select Body from Licenses where Key='mit';
```
```sh
MIT License

Copyright (c) [year] [fullname]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

```

CC0が含まれていない。

# ライセンス #

このソフトウェアはCC0ライセンスである。

[![CC0](http://i.creativecommons.org/p/zero/1.0/88x31.png "CC0")](http://creativecommons.org/publicdomain/zero/1.0/deed.ja)
