# -*- coding: utf-8 -*-
"""
"""
import sys
import requests
import http.client
import json
sys.path.append('..')
from next.utils import DRFAbstractInfo


def test_utils():
    print(DRFAbstractInfo.Fields.all())
    print(DRFAbstractInfo.Fields.default_args)
    pass


test_utils()
