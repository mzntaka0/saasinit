# -*- coding: utf-8 -*-
"""
"""
#import unittest
import requests
#import http.client
#import json

from decouple import config


#class TestDocumentAPI(unittest.TestCase):
#def test_create_document(self):
def test_get_document():
    access_token = config('TESTUSER_ID_TOKEN')
    #access_token = get_access_token()['access_token']
    headers = {
        'Content-Type': 'application/json',
        'authorization': 'Bearer ' + access_token
    }
    contents = {
        #"会社_2__会社名": "アイ·エム·アイ株式会社"
        "company__company_name": "imi"
    }
    result = requests.get(
        post_url,
        params=contents,
        headers=headers
    )
    print(result)
    from bpdb import set_trace
    set_trace()


if __name__ == '__main__':
    #json_path = './jsons/2019_02_20_21_40_48.json'
    post_url = 'http://9978c754.ngrok.io/api/documents/filter/'
    test_get_document()
