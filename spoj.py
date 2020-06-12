#!/usr/bin/env python3

import os
import requests
import subprocess
import re

link = ''
pattern = r'^(https://)?(www.)?(spoj.com/)(problems/)(.*)(/)$'
matching = False
while (not matching):
    link = input("SPOJ link: ")
    if requests.get(link).status_code != 200:
        print('unable to connect to ' + link)
        continue
    matching = re.match(pattern, link)

problem_name = matching.groups()[-2]

print('problem name: ' + problem_name)
if not os.path.exists(problem_name + '.cpp'):
    if subprocess.run(['cp', 'template.cpp', problem_name + '.cpp']).returncode == 0:
        print(problem_name + '.cpp created successfully')
else:
    print(problem_name + '.cpp file already exists.')


