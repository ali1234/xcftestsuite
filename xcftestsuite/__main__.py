import pathlib

import click


@click.group()
def xcftestsuite():
    pass


@xcftestsuite.command()
@click.argument('testdir', type=click.Path(writable=True))
def generate(testdir):
    from xcftestsuite.gimp import run_gimp
    script = pathlib.Path(__file__).parent / 'data' / 'testgen.py'
    run_gimp(script, testdir)


@xcftestsuite.command()
@click.argument('testdir', type=click.Path(writable=True))
def test(testdir):
    from xcftestsuite.test import run_test
    run_test(testdir)


@xcftestsuite.command()
@click.argument('testdir', type=click.Path(writable=True))
def generate(testdir):
    from xcftestsuite.gimp import run_script
    script = pathlib.Path(__file__).parent / 'data' / 'testgen.py'
    run_script(script, testdir)


@xcftestsuite.command()
@click.argument('testdir', type=click.Path(writable=True))
def test(testdir):
    from xcftestsuite.test import run_test
    run_test(testdir)


@xcftestsuite.command()
@click.argument('testdir', type=click.Path(writable=True))
def report(testdir):
    from xcftestsuite.report import run_report
    run_report(testdir)


@xcftestsuite.command()
@click.argument('testdir', type=click.Path(writable=True))
def all(testdir):
    print("Generating...")
    from xcftestsuite.gimp import run_script
    script = pathlib.Path(__file__).parent / 'data' / 'testgen.py'
    run_script(script, testdir)

    print("Testing...")
    from xcftestsuite.test import run_test
    run_test(testdir)

    print("Reporting...")
    from xcftestsuite.report import run_report
    run_report(testdir)


if __name__ == '__main__':
    xcftestsuite()
