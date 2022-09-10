import pathlib
import subprocess

from tqdm import tqdm
from gimpformats.gimpXcfDocument import GimpDocument
from layeredimage.io import openLayerImage


def xcf2png_gimpformats(xcf):
    img = GimpDocument(str(xcf))
    img.image.save(str(xcf.parent / (xcf.stem + '-gimpformats.png')))


def xcf2png_layeredimage(xcf):
    img = openLayerImage(str(xcf))
    img.getFlattenLayers().save(str(xcf.parent / (xcf.stem + '-layeredimage.png')))


def xcf2png_xcftools(xcf):
    subprocess.check_call(('xcf2png', str(xcf), '-o',  str(xcf.parent / (xcf.stem + '-xcftools.png'))))


def run_test(testdir):
    testdir = pathlib.Path(testdir)
    for x in tqdm(list(sorted(testdir.glob('*.xcf')))):
        xcf2png_gimpformats(x)
        xcf2png_layeredimage(x)
        xcf2png_xcftools(x)
