import posixpath
import tempfile
from hashlib import sha1
from os import path, getcwd, chdir, listdir
from shutil import move

from docutils import nodes
from sphinx.util import logging
from sphinx.locale import __
from sphinx.util.osutil import ensuredir
from .exceptions import DiagramError

logger = logging.getLogger(__name__)


def render_diagram(self, code, options, format=None, prefix='diagram'):
    """Render graphviz code into a PNG or PDF output file."""
    hashkey = (code + str(options)).encode()

    current_dir = getcwd()
    try:
        with tempfile.TemporaryDirectory() as tmpdirname:
            chdir(tmpdirname)
            exec(code)
            # check that the code should have generated an PNG or an SVG
            # file inside that folder
            for filename in listdir(tmpdirname):
                if filename.endswith('.png') or filename.endswith('.svg'):
                    break
            else:
                raise DiagramError('No generated image was found')

            fname = '%s-%s%s' % (prefix, sha1(hashkey).hexdigest(), path.splitext(filename)[1])
            relfn = posixpath.join(self.builder.imgpath, fname)
            outfn = path.join(self.builder.outdir, self.builder.imagedir, fname)
            ensuredir(path.dirname(outfn))

            move(path.join(tmpdirname, filename), outfn)
    finally:
        chdir(current_dir)

    return relfn, outfn


def render_diagram_html(self, node, code, options, prefix='diagramascode', imgcls=None, alt=None):
    if imgcls:
        imgcls += " diagramascode"
    else:
        imgcls = "diagramascode"

    fname, outfn = render_diagram(self, code, options, format, prefix)
    if alt is None:
        alt = node.get('alt', self.encode(code).strip())
    if 'align' in node:
        self.body.append('<div align="%s" class="align-%s">')

    self.body.append('<div class="graphviz">')
    self.body.append('<img src="%s" alt="%s" class="%s" />' %
                     (fname, alt, imgcls))
    self.body.append('</div>\n')

    if 'align' in node:
        self.body.append('</div>\n')

    raise nodes.SkipNode


def html_visit_diagramascode(self, node):
    render_diagram_html(self, node, node['code'], node['options'])
