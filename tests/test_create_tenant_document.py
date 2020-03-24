# -*- coding: utf-8 -*-
"""
"""
#import unittest
import requests
import http.client
import json

from decouple import config


def get_userinfo():
    conn = http.client.HTTPSConnection('next-ocr.auth0.com')
    headers = {
        'content-type': 'application/json',
        #'authorization': 'Bearer ' + get_access_token()['access_token']
        'authorization': 'Bearer ' + config('TESTUSER_ACCESS_TOKEN')
    }
    conn.request(
        'GET',
        '/userinfo',
        headers=headers
    )
    res = conn.getresponse()
    data = json.loads(res.read())
    return data


def get_access_token():
    #url = 'http://next-ocr.auth0.com/oauth/token'
    conn = http.client.HTTPSConnection('next-ocr.auth0.com')
    headers = {
        'content-type': 'application/json'
    }
    payload = "{{\"client_id\":\"{}\",\"client_secret\":\"{}\",\"audience\":\"{}\",\"grant_type\":\"client_credentials\"}}".format(
        config('AUTH0_CLIENT_ID'),
        config('AUTH0_CLIENT_SECRET'),
        config('AUTH0_API_IDENTIFIER')
    )
    conn.request(
        'POST',
        '/oauth/token',
        payload,
        headers
    )
    res = conn.getresponse()
    data = json.loads(res.read())
    return data


#class TestDocumentAPI(unittest.TestCase):
#def test_create_document(self):
def test_create_tenant_document(tenant: str):
    access_token = config('ADMINUSER_ID_TOKEN')
    headers = {
        'Content-Type': 'application/json',
        'authorization': 'Bearer ' + access_token,
    }
    contents = {
        'name': 'filter_test2',
        'tenant': tenant,
        'document_type': 'invoice',
        'document_content': {}
    }
    #with open(json_path, 'r') as f:
    #    content = json.load(f)
    content = {
        'company': {'company_name': 'imi'},
        'hoge': 'huga'
    }
    contents['document_content'] = json.dumps(content)
    #contents['document_content'] = content
    result = requests.post(
        post_url,
        json.dumps(contents),
        headers=headers
    )
    print(result)


if __name__ == '__main__':
    json_path = './jsons/2019_02_20_21_40_48.json'
    post_url = 'https://9978c754.ngrok.io/api/documents/'
    tenant = 'testtenant2'
    test_create_tenant_document(tenant)
