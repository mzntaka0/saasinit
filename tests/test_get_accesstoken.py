# -*- coding: utf-8 -*-
"""
"""
import requests
import json

from decouple import config


def test_get_accesstoken():
    headers = {
        'Content-Type': 'application/json'
    }
    contents = {
        'email'
    }
