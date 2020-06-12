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
    matching = re.match(pattern, link)

problem_name = matching.groups()[-2]

print(problem_name)
if not os.path.exists(problem_name + '.cpp'):
    print(subprocess.run(['cp', 'template.cpp', problem_name + '.cpp']))


