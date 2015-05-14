#!/usr/bin/env python

import json
import os
import sys
from subprocess import call
from jinja2 import Template
from pyquery import PyQuery

assert len(sys.argv) == 2, "Second argument is the notebook name!"
NOTEBOOK = sys.argv[1]

parts = NOTEBOOK.split('.')
parts[-1] = "html"
HTML_FILE = ".".join(parts)

# Gather the information from the first cell.
with open(NOTEBOOK) as f:
    res = json.load(f)
blocks = json.loads("".join(res['cells'][0]['source']))

# Convert the notebook. 
call(['ipython', 'nbconvert', NOTEBOOK, '--to', 'html', '--template', 'basic'])

# Remove input cells.
with open(HTML_FILE) as f:
    doc = PyQuery(f.read(), parser='html')
    doc.remove('.input')
    blocks['body'] = doc.html()

# Insert into simple template. 
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(BASE_DIR, 'my_template.html')) as f:
    tmpl = f.read()
template = Template(tmpl)

with open(HTML_FILE, 'w') as f:
    f.write(template.render(**blocks))