#!python3
#encoding:utf-8
import Data
import time
import pytz
import requests
import json
import datetime

class Licenses:
    def __init__(self, data):
        self.data = data

    def Update(self):
        self.data.db_license.begin()
        licenses = self.__RequestLicenses()
        for l in licenses:
            license = self.__RequestLicense(l['key'])
            self.__InsertUpdateLicenses(license)
        self.data.db_license.commit()

    def __RequestLicenses(self):
        url = 'https://api.github.com/licenses'
        r = requests.get(url, headers=self.__GetHttpHeaders())
        return self.__ReturnResponse(r, success_code=200)

    def __RequestLicense(self, key):
        url = 'https://api.github.com/licenses/' + key
        r = requests.get(url, headers=self.__GetHttpHeaders())
        return self.__ReturnResponse(r, success_code=200)

    def __InsertUpdateLicenses(self, j):
        record = self.data.db_license['Licenses'].find_one(Key=j['key'])
        if None is record:
            self.data.db_license['Licenses'].insert(self.__CreateRecord(j))
        else:
            self.data.db_license['Licenses'].update(self.__CreateRecord(j), ['Key'])

    def __CreateRecord(self, j):
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
