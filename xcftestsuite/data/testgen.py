import os
from itertools import product

from gimpfu import *


all_modes = {
    k[:-5].lower(): v for k, v in globals().items() if k.endswith('_MODE')
}


class Templates:

    def __init__(self):
        src = os.path.join(os.path.dirname(__file__), 'layers.xcf')
        self._img = pdb.gimp_file_load(src, src)
        self._layers = {
            l.name.lower(): l for l in self._img.layers
        }

    def __del__(self):
        del self._layers
        pdb.gimp_image_delete(self._img)

    def __getitem__(self, item):
        return self._layers[item.lower()]

    def names(self):
        return self._layers.keys()


class LayerDef:
    def __init__(self, name, opacity, mode):
        self.name = name
        self.opacity = opacity
        self.mode = mode

    def __str__(self):
        return '{}_{}_{}'.format(
            self.name,
            self.opacity,
            self.mode
        )


class Image:

    layer_templates = Templates()

    def __init__(self, dir, name):
        self._dir = dir
        self._name = name
        self._stem = os.path.join(dir, name)
        self._xcf = self._stem + '.xcf'
        self._png = self._stem + '-gimp.png'
        self._img = gimp.Image(64, 64, RGB)

    def __del__(self):
        pdb.gimp_image_delete(self._img)

    def new_layer(self, opacity=100.0, mode=NORMAL_MODE):
        layer = gimp.Layer(self._img, 'Base', 64, 64, RGBA_IMAGE, opacity, mode)
        self._img.add_layer(layer)
        return layer

    def template_layer(self, name, opacity=100.0, mode=NORMAL_MODE):
        layer = self.new_layer(opacity, mode)
        pdb.gimp_edit_copy(self.layer_templates[name])
        floatingLayer = pdb.gimp_edit_paste(layer, FALSE)
        pdb.gimp_floating_sel_anchor(floatingLayer)

    def save(self):
        pdb.gimp_xcf_save(0, self._img, None, self._xcf, self._xcf)

    def export(self):
        l = self._img.merge_visible_layers(NORMAL_MODE)
        pdb.file_png_save(self._img, l, self._png, self._png, 0, 9, 1, 0, 0, 1, 1)

    @classmethod
    def make(cls, tests, layer1, layer2):
        i = Image(tests, str(layer1)+'_'+str(layer2))
        i.template_layer(layer1.name, layer1.opacity, all_modes[layer1.mode])
        i.template_layer(layer2.name, layer2.opacity, all_modes[layer2.mode])
        i.save()
        i.export()


def run(tests):
    templates = Image.layer_templates.names()
    opacities = (50.0, )
    modes = ('multiply', 'addition')

    layer_defs = [LayerDef(*args) for args in product(templates, opacities, modes)]
    test_count = len(layer_defs) ** 2
    for n, (l1, l2) in enumerate(product(layer_defs, layer_defs), start=1):
        Image.make(tests, l1, l2)
        if n & 0xf == 0:
            print(n, '/', test_count)

    del Image.layer_templates
