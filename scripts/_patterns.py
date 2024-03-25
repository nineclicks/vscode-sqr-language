import requests
from bs4 import BeautifulSoup
import re

# URL to scrape
url = "https://docs.oracle.com/cd/E24150_01/pt851h2/eng/psbooks/tsql/htm/tsql03.htm"

def _is_named_table(name, table):
    first_row = table.find('tr')
    if first_row:
        first_cell = first_row.find('td')
        if first_cell and name in first_cell.text:
            return True
    return False

def _get_tables(soup, name):
    values = []
    for table in soup.find_all('table'):
        if _is_named_table(name, table):
            for row in table.find_all('tr')[1:]:  # Skip the first row which is the header
                first_cell = row.find('td')
                if first_cell:
                    values.append(first_cell.text.strip())

    return values

def get_patterns():
    # Fetch the webpage content
    response = requests.get(url)
    html_content = response.text
    # Parse the HTML content
    soup = BeautifulSoup(html_content, "html.parser")
    items = []

    all_keywords = [y.strip().split(' ')[0].replace('\xa0', ' ') for tag in soup.find_all('h4') for y in tag.text.lower().split(',')]


    items.append({
        'comment': 'directives',
        'name': 'entity.name.function.macro.sqr',
        'list': [x for x in all_keywords if x.startswith('#')],
    })

    items.append({
            'comment': 'comments',
            "name": "comment.block.sqr",
            "match": "!.*$"
        })

    items.append({
            'comment': 'variables',
            "name": "variable.name.sqr",
            "match": "([$#&][\w-]+)"
        })

    items.append({
        "name": "string.single.source.sqr",
        "match": "'(?:\\\\.|[^'\\\\])*'",
        "comment": "String single quote"
        })

    items.append({
        "name": "string.double.source.sqr",
        "match": '"(?:\\\\.|[^"\\\\])*"',
        "comment": "String double quote"
        })

    items.append({
            'comment': 'procedure call',
            "match": "(?i)\\b(do)\\b[\\t ]+([\\w-]+)",
            "captures": {
                '1': {
                    'name': 'keyword.control.sqr'
                },
                '2': {
                    'name': 'entity.name.function.SQR'
                },
            }
        })

    items.append({
            'name': 'meta.function.procedure.SQR',
            'begin': '(?i)^[ \\t]*(begin-procedure)[ \\t]+([\\w-]+)(?:[ \\t]+(local))?',
            'beginCaptures': {
                '1': {
                    'name': 'keyword.control.SQR'
                },
                '2': {
                    'name': 'entity.name.function.SQR'
                },
                '3': {
                    'name': 'entity.name.type.SQR'
                }
            },
            'end': '(?i)^[ \\t]*(end-procedure)',
            'endCaptures': {
                '0': {
                    'name': 'keyword.control.sqr'
                }
            },
            'patterns': [
                {
                    'include': '$self'
                }
            ]
        })

    ############################################
    ########### match generated from list ######
    ############################################


    items.append({
        'comment': 'stuff that is manually included later, to be excluded in list->match generation',
        'exclude': True,
        'list': [
            'do',
            *[y for x in ['procedure'] for y in (f'begin-{x}', f'end-{x}')],
        ],
    })

    items.append({
        'comment': 'controls',
        'name': 'keyword.control.sqr',
        'list': ['if', 'else', 'end-if', 'while', 'end-while', 'evaluate', 'when-other'],
    })

    items.append({
        'comment': 'sections',
        'name': 'entity.name.function.sqr',
        'list': [y for x in ['program', 'setup', 'heading', 'footing'] for y in (f'begin-{x}', f'end-{x}')],
    })

    items.append({
        'comment': 'functions',
        'name': 'entity.name.function.sqr',
        'list': _get_tables(soup, 'Function'),
    })

    items.append({
        'comment': 'operators',
        'name': 'keyword.operator.sqr',
        'list': [y.strip() for x in _get_tables(soup, 'Operator') for y in x.split(',')],
    })

    ###### Everything else from the all_keywords list that is not already in a list
    items.append({
        'comment': 'keywords',
        'name': 'keyword.other.sqr',
        'list': [x for x in all_keywords if x not in [y for item in items for y in item.get('list', [])]],
    })


    for item in items:
        if 'list' in item:
            item['match'] = '(?i)(?<![\\w-])(' + '|'.join([re.escape(x) for x in item['list']]) + ')(?![\\w-])'
            del item['list']


    items = [x for x in items if not x.get('exclude')]
    return items