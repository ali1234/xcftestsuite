from datetime import datetime
import pathlib
from collections import defaultdict

from tabulate import tabulate
from PIL import Image
import numpy as np
from tqdm import tqdm

from xcftestsuite.versions import get_version


html = """<html>
<head>
<title>XCF Test Suite</title>
<link rel="stylesheet" href="styles.css" />
</head>
<body>
<p>{count} tests run at {date} UTC. Source code: {url}</p>
{results}
</body>
</html>
"""


def link(p, h=None):
    if h is None:
        h = p
    return f'<a href="{p}">{h}</a>'


def img(p, c):
    return link(p, f'<img class="{c}" src="{p}" />')


def mimg(p):
    return ''.join(
        img(p, 'bg_' + c) for c in ('white', 'grey', 'black')
    )


def imgbox(p, c):
    return f'<div class="{c}">{mimg(p)}</div>'


def compare(a, b):
    a = np.asarray(a).astype(np.int32)
    b = np.asarray(b).astype(np.int32)
    return (np.abs(a - b) < 8).all()


def get_results(testdir, exts):
    for xcf in tqdm(list(sorted(testdir.glob('*.xcf')))):
        gimp = (xcf.stem + '-gimp.png')
        others = [xcf.stem + '-' + ext + '.png' for ext in exts]
        gimp_result = Image.open(testdir / gimp)
        results = [compare(gimp_result, Image.open(testdir / other)) for other in others]
        yield xcf.name, gimp, list(zip(exts, others, results))


def get_header(prog, test_count, pass_count):
    passed = pass_count[prog]
    failed = test_count - passed
    percent = (passed / test_count) * 100.0
    return f'<p class="prog">{get_version(prog)}</p><p class="counts">{passed} passed, {failed} failed ({percent:.0f}%)</p>'


def run_report(testdir):
    testdir = pathlib.Path(testdir)
    tests = []
    progs = 'gimpformats', 'layeredimage', 'xcftools'
    test_count = 0
    pass_count = defaultdict(int)
    for xcf, gimp, result in get_results(testdir, progs):
        test_count += 1
        for prog, file, passed in result:
            if passed:
                pass_count[prog] += 1
        row = [
            link(xcf, xcf),
            imgbox(gimp, 'orig'),
            *(
                imgbox(file, 'pass' if passed else 'fail') for prog, file, passed in result
            )
        ]
        tests.append(row)

    headers = ('xcf', get_version('gimp'), *(get_header(prog, test_count, pass_count) for prog in progs))
    result_table = tabulate(tests, headers=headers, tablefmt='unsafehtml')

    with open(testdir / 'index.html', 'w') as report:
        report.write(html.format(
            url = link('https://github.com/ali1234/xcftestsuite'),
            date = datetime.utcnow(),
            count = test_count,
            results = result_table
        ))

    style_file = pathlib.Path(__file__).parent / 'data' / 'styles.css'
    with open(testdir / 'styles.css', 'w') as styles:
        styles.write(style_file.read_text())
