import subprocess
from importlib.metadata import version

import xcftestsuite.gimp


def get_version(prog):
    if prog in ('gimpformats', ):
        return prog + ' ' + version(prog)
    elif prog == 'xcftools':
        return prog + ' ' + subprocess.check_output(('xcf2png', '--version')).split()[-1].decode('utf8')
    elif prog == 'gimp':
        return prog + ' ' + xcftestsuite.gimp.get_version()
