#!/usr/bin/env python3

import sys
import os
import requests
import subprocess
import re
from bs4 import NavigableString, Tag, BeautifulSoup

link = input("SPOJ link: (Enter 'exit' to exit script)\t")
pattern = r'^(https://)(www.)(spoj.com/)(problems/)(.+)(/)$'
matching = re.match(pattern, link)
while (not bool(matching)):
    if link == 'exit':
        print('exiting script')
        exit(0)
    sys.stderr.write('invalid link in context\n')
    link = input("SPOJ link: (Enter 'exit' to exit script)\t")
    try:
        if requests.get(link).status_code != 200:
            sys.stderr.write('unable to establish a connection to ' + link)
            continue
    except:
        sys.stderr.write('invalid link\n')
        continue
    matching = re.match(pattern, link)

problem_name = matching.groups()[-2]

print('problem name: ' + problem_name)
if not os.path.exists(problem_name + '.cpp'):
    if subprocess.run(['cp', 'template.cpp', problem_name + '.cpp']).returncode == 0:
        print(problem_name + '.cpp created successfully')
else:
    print(problem_name + '.cpp file already exists.')
    exit(1)

page = requests.get(link)

soup = BeautifulSoup(page.content, 'html.parser')

problem_full_name_tag = soup.find(id='problem-name')
problem_full_name = str(problem_full_name_tag.string)
print('problem full name : ' + problem_full_name)

problem_tags_bs = soup.find(id='problem-tags').contents

problem_tags = []
no_tags = False
for x in problem_tags_bs:

    y = x
    while isinstance(y, Tag):
        y = y.contents[0]
    if isinstance(y, NavigableString):
        y = str(y)

    if re.match(r'no tag', y):
        no_tags = True
        break
    if re.match(r'(#[\-a-zA-Z0-9_]+)', y):
        problem_tags.append(re.match(r'(#[\-a-zA-Z0-9_]+)', y).groups()[0])

if not no_tags:
    print(problem_tags)

the_text = '+ '

the_text += '[**' + problem_full_name + '**](' + link + ') \\\n'

for problem_tag in problem_tags:
    the_text += '\t_\\' + problem_tag + '_'

if no_tags:
    the_text += '\t_no tags_'

the_text += '\\\n\tsolution : [' + problem_name + '.cpp](' + problem_name + '.cpp)\n\n<!--spoj end-->'

with open('README.md', 'r') as readme_file:
    text = readme_file.read()

text = re.sub(r'<\!--spoj end-->', the_text, text)

with open('README.md', 'w') as readme_file:
    readme_file.write(text)
