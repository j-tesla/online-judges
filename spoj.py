#!/usr/bin/env python3

import os
import re
import subprocess
import sys

import requests
from bs4 import NavigableString, Tag, BeautifulSoup


# exits code if passed string is 'exit'
def script_exit(code: str) -> None:
    if not isinstance(code, str):
        raise TypeError('passed argument must be a string')

    if code == 'exit' or code == 'EXIT' or code == 'Exit':
        print('EXITING SCRIPT')
        exit(0)


# appends README.md with problem text passed
def append_readme(text_to_append: str) -> None:
    if not isinstance(text_to_append, str):
        raise TypeError('append_readme takes a string as an argument')

    with open('README.md', 'r') as readme_file:
        text = readme_file.read()

    text = text.replace(r'<!--spoj end-->', text_to_append)

    with open('README.md', 'w') as readme_file:
        readme_file.write(text)


# gets problem link(and the problem name from it) from input or sys args if passed
def get_link_and_problem_name(sys_args: list = None) -> (str, requests.models.Response):
    if sys_args is None:
        sys_args = []
    if not isinstance(sys_args, list):
        raise TypeError('passed argument must be an sized')

    input_message = "SPOJ link: (Enter 'exit' to exit the script)\t"
    pattern = r'^(https://)(www.)(spoj.com/)(problems/)(.+)(/)$'

    if len(sys_args) <= 1:
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
                sys.stderr.write('unable to connect with ' + input_link + '\n')
                continue
        except requests.exceptions.RequestException:
            sys.stderr.write('invalid link\n')
            page = None
            continue

    problem_name_in_link = matching.groups()[-2]

    return input_link, problem_name_in_link, page


# checks if the problem file exists and creates, exits code if the file already exists
def check_and_create_file(name: str) -> None:
    if not isinstance(name, str):
        raise TypeError('argument name should be a string')

    if not os.path.exists('spoj/' + name + '.cpp'):
        if subprocess.run(['cp', 'template.cpp', 'spoj/' + name + '.cpp']).returncode == 0:
            print(name + '.cpp created successfully')
        else:
            sys.stderr.write('failed to create ' + name + '.cpp\n')
            print('exiting...')
    else:
        sys.stderr.write(name + '.cpp file already exists.\n')
        print('exiting...')
        exit(1)


# gets problem's full name from the problem page's soup
def get_problem_full_name(soup_object: BeautifulSoup) -> str:
    if not isinstance(soup_object, BeautifulSoup):
        raise TypeError('BeautifulSoup object must be passed')

    full_name_tag = soup_object.find(id='problem-name')
    full_name = str(full_name_tag.string)
    return full_name


# gets problem's tags from problem page's soup
def get_problem_tags(soup_object):
    if not isinstance(soup_object, BeautifulSoup):
        raise TypeError('BeautifulSoup object must be passed')

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


# generates the text to append in the README.md from the details passed
def problem_text(problem_name: str, problem_full_name: str, link: str, problem_tags: list) -> str:
    if not (isinstance(problem_name, str) and isinstance(problem_full_name, str)):
        raise TypeError("problem_name and problem_full_name should be strings")
    if not isinstance(link, str):
        raise TypeError('link must be a string')
    if not isinstance(problem_tags, list):
        raise TypeError('problem_tags needs to be an iterable')

    the_text = '+ '

    the_text += '[**' + problem_full_name + '**](' + link + ') \\\n'

    for problem_tag in problem_tags:
        the_text += '\t_\\' + problem_tag + '_'

    if len(problem_tags) == 0:
        the_text += '\t_no tags_'

    the_text += '\\\n\tsolution : [' + problem_name + '.cpp](' + problem_name + '.cpp)\n\n<!--spoj end-->'

    return the_text


# it's the frickin' main! does it require any description?
def main(sys_args: list = None) -> None:
    if sys_args is None:
        sys_args = []
    if not isinstance(sys_args, list):
        raise TypeError('sys_args should be an sized')

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
