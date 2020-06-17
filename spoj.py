#!/usr/bin/env python3

import os
import re
import subprocess
import sys
from collections.abc import Iterable

import requests
from bs4 import NavigableString, Tag, BeautifulSoup


def is_iterable(obj):
    return isinstance(obj, Iterable)


def script_exit(code):
    if code == 'exit' or code == 'EXIT' or code == 'Exit':
        print('EXITING SCRIPT')
        exit(0)


def append_readme(text_to_append):
    with open('README.md', 'r') as readme_file:
        text = readme_file.read()

    text = text.replace(r'<!--spoj end-->', text_to_append)

    with open('README.md', 'w') as readme_file:
        readme_file.write(text)


def get_link_and_problem_name(sys_args=None):
    if sys_args is None:
        sys_args = []
    if not is_iterable(sys_args):
        raise TypeError('passed argument needs to be an iterable')

    input_message = "SPOJ link: (Enter 'exit' to exit the script)\t"
    pattern = r'^(https://)(www.)(spoj.com/)(problems/)(.+)(/)$'

    if len(sys_args) == 1:
        input_link = input(input_message)
        script_exit(input_link)
    else:
        input_link = sys_args[1]

    matching = re.match(pattern, input_link)

    if matching:
        page = requests.get(input_link)
        print(str(page.status_code) + ':', end='\t')
        if page.status_code != 200:
            sys.stderr.write('unable to connect with ' + input_link + '\n')
            matching = False
    else:
        print('not a valid link in context')

    while not matching:
        input_link = input(input_message)
        script_exit(input_link)
        matching = re.match(pattern, input_link)
        if not matching:
            sys.stderr.write('not a valid link in context\n')
            continue

        try:
            page = requests.get(input_link)
            print(str(page.status_code) + ':', end='\t')
            if page.status_code != 200:
                sys.stderr.write('unable to connect with ' + input_link)
                continue
        except requests.exceptions.RequestException:
            sys.stderr.write('invalid link\n')
            page = None
            continue

    problem_name_in_link = matching.groups()[-2]

    return input_link, problem_name_in_link, page


def check_and_create_file(name):
    if not os.path.exists(name + '.cpp'):
        if subprocess.run(['cp', 'template.cpp', name + '.cpp']).returncode == 0:
            print(name + '.cpp created successfully')
        else:
            sys.stderr.write('failed to create ' + name + '.cpp')
    else:
        sys.stderr.write(name + '.cpp file already exists.')
        exit(1)


def get_problem_full_name(soup_object):
    full_name_tag = soup_object.find(id='problem-name')
    full_name = str(full_name_tag.string)
    return full_name


def get_problem_tags(soup_object):
    problem_tags_bs = soup_object.find(id='problem-tags').contents
    tags = []

    for x in problem_tags_bs:

        y = x
        while isinstance(y, Tag):
            y = y.contents[0]
        if isinstance(y, NavigableString):
            y = str(y)

        if re.match(r'(#[\-a-zA-Z0-9_]+)', y):
            tags.append(re.match(r'(#[\-a-zA-Z0-9_]+)', y).groups()[0])

    return tags


def problem_text(problem_name, problem_full_name, link, problem_tags):
    the_text = '+ '

    the_text += '[**' + problem_full_name + '**](' + link + ') \\\n'

    for problem_tag in problem_tags:
        the_text += '\t_\\' + problem_tag + '_'

    if len(problem_tags) == 0:
        the_text += '\t_no tags_'

    the_text += '\\\n\tsolution : [' + problem_name + '.cpp](' + problem_name + '.cpp)\n\n<!--spoj end-->'

    return the_text


def main(sys_args):
    link, problem_name, problem_page = get_link_and_problem_name(sys_args)
    print('problem name: ' + problem_name)
    soup = BeautifulSoup(problem_page.content, 'html.parser')

    check_and_create_file(problem_name)
    print('checked and created')
    problem_full_name = get_problem_full_name(soup)
    print('problem full name : ' + problem_full_name)

    problem_tags = get_problem_tags(soup)

    print('tags:', end='\t')
    print(problem_tags)

    append_readme(problem_text(problem_name, problem_full_name, link, problem_tags))


if __name__ == '__main__':
    main(sys.argv)
