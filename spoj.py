#!/usr/bin/env python3

import os
import requests
import subprocess
import re
from bs4 import NavigableString, Tag, BeautifulSoup

link = ''
pattern = r'^(https://)?(www.)?(spoj.com/)(problems/)(.*)(/)$'
matching = re.match(pattern, link)
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
    if isinstance(x, NavigableString):
        y = str(x)
        if re.match(r'no tags', y):
            no_tags = True

    elif isinstance(x, Tag):
        y = str(x.contents[0].contents[0])
        problem_tags.append(y)


if not no_tags:
    print(problem_tags)

the_text = '+ '

the_text += '[**' + problem_full_name + '**](' + link + ') \\\n'

for problem_tag in problem_tags:
    the_text += '\t_\\' + problem_tag + '_'

the_text += '\\\n\tsolution : [' + problem_name + '.cpp](' + problem_name + '.cpp)\n\n<!--spoj end-->'

with open('README.md', 'r') as readme_file:
    text = readme_file.read()

text = re.sub(r'<\!--spoj end-->', the_text, text)

with open('README.md', 'w') as readme_file:
    readme_file.write(text)

