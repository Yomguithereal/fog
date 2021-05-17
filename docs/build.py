import re
from io import StringIO
from functools import partial
from docstring_parser import parse as docstring_parser
from docstring_parser import (
    DocstringParam,
    DocstringReturns,
    DocstringRaises,
    DocstringDeprecated
)

import fog.evaluation as evaluation
import fog.graph as graph
import fog.metrics as metrics
import fog.key as key

DOCS = [
    {
        'title': 'Evaluation',
        'fns': [
            evaluation.best_matching_macro_average
        ]
    },
    {
        'title': 'Graph',
        'fns': [
            graph.floatsam_sparsification,
            graph.monopartite_projection
        ]
    },
    {
        'title': 'Keyers',
        'fns': [
            key.omission_key,
            key.skeleton_key
        ]
    },
    {
        'title': 'Metrics',
        'fns': [
            metrics.cosine_similarity,
            metrics.sparse_cosine_similarity,
            metrics.sparse_dot_product,
            metrics.binary_cosine_similarity,
            metrics.sparse_binary_cosine_similarity,
            metrics.dice_coefficient,
            metrics.jaccard_similarity,
            metrics.weighted_jaccard_similarity,
            metrics.overlap_coefficient
        ]
    }
]


with open('./README.template.md') as f:
    TEMPLATE = f.read()


def build_toc(data):
    lines = []

    for item in data:
        lines.append('* [%s](#%s)' % (item['title'], item['title'].lower()))

        for fn in item['fns']:
            name = fn.__name__

            lines.append('  * [%s](#%s)' % (name, name.lower()))

    return '\n'.join(lines)


def assembling_description(docstring):
    d = docstring.short_description

    if docstring.blank_after_long_description:
        d += '\n' + docstring.long_description
    else:
        d += ' ' + docstring.long_description

    return d.strip()


EXAMPLE_BLACKLIST = (
    DocstringParam,
    DocstringReturns,
    DocstringRaises,
    DocstringDeprecated
)


def examples_iter(docstring):
    for meta in docstring.meta:
        if isinstance(meta, EXAMPLE_BLACKLIST):
            continue

        yield meta.description


DEFAULT_RE = re.compile(r'.\s*Defaults? to (.+)\.', re.MULTILINE)
CLEAN_RE = re.compile(r'[\'"`]')


def template_param(param):
    line = '* **%s** ' % param.arg_name

    if param.is_optional:
        line += '*?%s*' % param.type_name
    else:
        line += '*%s*' % param.type_name

    m = DEFAULT_RE.search(param.description)

    if m is not None:
        line += ' [`%s`]' % CLEAN_RE.sub('', m.group(1))

    line += ': %s' % DEFAULT_RE.sub('.', param.description)

    return line


def build_docs(data):
    f = StringIO()

    p = partial(print, file=f)

    p()

    for item in data:
        p('### %s' % item['title'])
        p()

        for fn in item['fns']:
            name = fn.__name__
            docstring = docstring_parser(fn.__doc__)
            description = assembling_description(docstring)

            p('#### %s' % name)
            p()
            p(description)

            for example in examples_iter(docstring):
                p()
                p('```python')
                p(example)
                p('```')

            p()
            p('*Arguments*')
            for param in docstring.params:
                p(template_param(param))

            p()

    result = f.getvalue()
    f.close()

    return result


readme = TEMPLATE.format(
    toc=build_toc(DOCS),
    docs=build_docs(DOCS)
).rstrip()

print(readme)
