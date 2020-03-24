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
    result = requests.get(
        post_url,
        headers=headers
    )
    print(result)
    from bpdb import set_trace
    set_trace()


if __name__ == '__main__':
    json_path = './jsons/2019_02_20_21_40_48.json'
    post_url = 'http://ec2-13-112-182-177.ap-northeast-1.compute.amazonaws.com:8000/api/documents/'
    test_get_document()
