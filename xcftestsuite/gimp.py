import subprocess
import sys


ignore = (
    '/app/lib/gimp/2.0/python/gimpfu.py:868',
    'gimp.main(None',
    'libgtk3-nocsd.so.0',
    'batch command executed successfully',
    'batch command experienced an execution error'
)

gimp_cmd = ("/usr/bin/flatpak", "run", "org.gimp.GIMP")


def run_script(script, outdir):
    pycode = f"import time; import sys;sys.path.insert(0, '{script.parent}'); from {script.stem} import run; run('{outdir}')"
    args = ("--no-interface", "-idf", "--batch-interpreter", "python-fu-eval", "-b", pycode, "-b", "pdb.gimp_quit(1)")
    x = subprocess.Popen(gimp_cmd + args, stderr=subprocess.PIPE)
    for line in x.stderr:
        line = line.decode('utf8')
        if any(i in line for i in ignore):
            continue
        sys.stderr.write(line)


def get_version():
    args = ("--version", )
    return subprocess.check_output(gimp_cmd + args, stderr=subprocess.DEVNULL).split()[-1].decode('utf8')
