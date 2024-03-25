"""
This script generates the TextMate patterns from the Oracle docs on SQR.
"""

import json
from _patterns import get_patterns
TM_PATH = '../syntaxes/sqr.tmLanguage.json'

patterns = get_patterns()

with open(TM_PATH, 'r') as fp:
    tm = json.load(fp)

tm['patterns'] = patterns

with open(TM_PATH, 'w') as fp:
    json.dump(tm, fp, indent=2)