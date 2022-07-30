#!/usr/bin/env python3
import re
import os
import json

from bs4 import BeautifulSoup
import click
import requests


YALELIST_URL = 'https://som.yale.edu/story/2022/over-1000-companies-have-curtailed-operations-russia-some-remain'


def section_extract_description(section):
    text_long = section.find_all(class_='text-long')
    assert len(text_long) == 1
    text_long = text_long[0]
    contents = [' '.join(p.contents) for p in text_long.find_all('p')]
    return '\n'.join(contents)


def tr_extract_record(tr):
    tds = [td for td in tr.findChildren()]
    # not all tds are populated with innerHTML`s
    contents = [td.contents[0] if len(td.contents) > 0 else '' for td in tds]
    record = {
        'name': contents[0].strip(),
        'action': contents[1].strip(),
        'industry': contents[2].strip(),
        'country': contents[3].strip()
    }
    return record


def section_extract_table(section):
    tbody = section.find_all('tbody')
    assert len(tbody) == 1
    tbody = tbody[0]
    records = []
    for i, row in enumerate(tbody.find_all('tr')):
        record = tr_extract_record(row)
        records.append(record)
    return records


def extract_category(soup, id):
    sections = soup.find_all(id=id)
    assert len(sections) == 1
    section = sections[0]
    description = section_extract_description(section)
    grade = re.search(r'Grade: [A-Z]', description).group(0)[len('Grade: '):]
    records = section_extract_table(section)
    category = {
        'description': description,
        'grade': grade,
        'records': records
    }
    return category


def extract_data(soup):
    categories = ('diggingin', 'buyingtime', 'scalingback', 'suspension', 'withdrawal')
    data = {}
    colors = ('red', 'yellow', 'green', 'blue', 'magenta')
    for i, category in enumerate(categories):
        click.secho(f'~= extracting category {category} =~', fg=colors[i % len(colors)])
        data[category] = extract_category(soup, category)
    return data


@click.command()
@click.option('--output', '-o', type=click.File('w+'), default='yalelist.json')
def main(output):
    url = YALELIST_URL
    page = requests.get(url)
    html = page.text
    soup = BeautifulSoup(html, 'html.parser')
    data = extract_data(soup)
    json.dump(data, output, indent='\t')

if __name__ == '__main__':
    main()