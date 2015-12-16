#!/usr/bin/python

# test_json.py

import json

with open('./data/sipm_366/sipm_366_1.txt', 'w') as outfile:
        json.dump(data, outfile)
