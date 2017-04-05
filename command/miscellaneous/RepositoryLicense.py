#!python3
#encoding:utf-8
import Data
import time
import pytz
import requests
import json
import datetime

class RepositoryLicense:
    def __init__(self, data):
        self.data = data

    def Update(self):
#        self.data.db_repo.begin()
#        self.data.db_license.begin()
        # リポジトリ作成日時の昇順で1つずつライセンス情報を取得する
        for repo in self.data.db_repo['Repositories'].find(order_by=['CreatedAt']):
            # すでにレコードが存在するリポジトリは飛ばす
            if None is not self.data.db_repo['Licenses'].find_one(RepositoryId=repo['Id']):
                continue
            # GitHubでは1リポジトリ1ライセンスしか割り振れないのかもしれない。型が配列型でなくオブジェクト型になっているから。
            # https://developer.github.com/v3/licenses/#get-a-repositorys-license
            j = self.__RequestRepositoryLicense(repo['Name'])
            
            # ライセンスが取得できないリポジトリはライセンスIDにNULLをセットする
            if None is j['license']:
                self.__InsertUpdateRepositoryLicenses(repo['Id'], None)
            else:
                # リポジトリにlicense情報が含まれているなら
                # ライセンスがないと`"license":null,`が返る
                if None is not j['license']:
                    self.__InsertUpdateLicenses(j)
                    print(j['license']['key'])
                    print(self.data.db_license['Licenses'].find_one(Key=j['license']['key'])['Id'])
                    self.__InsertUpdateRepositoryLicenses(repo['Id'], self.data.db_license['Licenses'].find_one(Key=j['license']['key'])['Id'])
#        self.data.db_license.commit()
#        self.data.db_repo.commit()

    """
    リポジトリのライセンスを取得する。
    @repo_name {string} 対象リポジトリ名
    @return    {dict}   結果(JSON形式)
    """
    def __RequestRepositoryLicense(self, repo_name):
        url = 'https://api.github.com/repos/{0}/{1}'.format(self.data.get_username(), repo_name)
        r = requests.get(url, headers=self.__GetHttpHeaders())
        return self.__ReturnResponse(r, success_code=200)

    """
    ライセンスDBに存在しないなら問い合わせる。
    @repo_name {string} 対象リポジトリ名
    @return    {dict}   結果(JSON形式)
    """
    def __InsertUpdateLicenses(self, j):
        print(j['license'])
        print(j['license']['key'])
        record = self.data.db_license['Licenses'].find_one(Key=j['license']['key'])
        if None is record:
            license = self.__RequestLicense(j['license']['key'])
            print(license)
            if 'key' not in license:
                raise Exception('GitHubに該当ライセンスを問い合わせても存在しませんでした。: {0}'.format(j['license']['key']))
            else:
                self.data.db_license['Licenses'].insert(self.__CreateLicenseRecord(license))

    """
    リポジトリのライセンスをDBに挿入する。
    @repo_name {string} 対象リポジトリ名
    @return    {dict}   結果(JSON形式)
    """
    def __InsertUpdateRepositoryLicenses(self, repo_id, license_id):
        record = self.data.db_repo['Licenses'].find_one(RepositoryId=repo_id)
        if None is record:
            self.data.db_repo['Licenses'].insert(self.__CreateRepoLicenseRecord(repo_id, license_id))
#        else:
#            self.data.db_repo['Licenses'].update(self.__CreateRepoLicenseRecord(repo_id, license_id), ['Key'])

    """
    指定したライセンスの情報を取得する。
    @param  {string} keyはGitHubにおけるライセンスを指定するキー。
    @return {dict}   結果(JSON)
    """
    def __RequestLicense(self, key):
        url = 'https://api.github.com/licenses/' + key
        r = requests.get(url, headers=self.__GetHttpHeaders())
        return self.__ReturnResponse(r, success_code=200)

    def __CreateRepoLicenseRecord(self, repo_id, license_id):
        return dict(
            RepositoryId=repo_id,
            LicenseId=license_id
        )

    def __CreateLicenseRecord(self, j):
        return dict(
            Key=j['key'],
            Name=j['name'],
            SpdxId=j['spdx_id'],
            Url=j['url'],
            HtmlUrl=j['html_url'],
            Featured=self.__BoolToInt(j['featured']),
            Description=j['description'],
            Implementation=j['implementation'],
            Permissions=self.__ArrayToString(j['permissions']),
            Conditions=self.__ArrayToString(j['conditions']),
            Limitations=self.__ArrayToString(j['limitations']),
            Body=j['body']
        )

    def __GetHttpHeaders(self):
        return {
            "Accept": "application/vnd.github.drax-preview+json",
            "Time-Zone": "Asia/Tokyo",
            "Authorization": "token {0}".format(self.data.get_access_token())
        }

    def __ReturnResponse(self, r, success_code=None, sleep_time=2, is_show=True):
        if is_show:
            print("HTTP Status Code: {0}".format(r.status_code))
            print(r.text)
        time.sleep(sleep_time)
        if None is not success_code:
            if (success_code != r.status_code):
                raise Exception('HTTP Error: {0}'.format(r.status_code))
                return None
        return json.loads(r.text)

    def __BoolToInt(self, bool_value):
        if True == bool_value:
            return 1
        else:
            return 0

    def __ArrayToString(self, array):
        ret = ""
        for v in array:
            ret = v + ','
        return ret[:-1]
