"""
    sphinxcontrib.sphinx-diagrams
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Sphinx extension for the Diagrams package

    :copyright: Copyright 2017 by Tomas Zulberti <tzulberti@gmail.com>
    :license: BSD, see LICENSE for details.
"""

import pbr.version

from sphinx.locale import __
from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.util.docutils import SphinxDirective
from sphinx.util.i18n import search_image_for_language

from .render import html_visit_diagramascode

__version__ = pbr.version.VersionInfo('sphinx-diagrams').version_string()


class DiagramNode(nodes.General, nodes.Inline, nodes.Element):
    pass


class DiagramAsCode(SphinxDirective):
    """
    Directive to insert arbitrary dot markup.
    """
    has_content = True
    required_arguments = 0
    optional_arguments = 1
    final_argument_whitespace = False
    option_spec = {
        'alt': directives.unchanged,
        'caption': directives.unchanged,
        'layout': directives.unchanged,
        'graphviz_dot': directives.unchanged,  # an old alias of `layout` option
        'name': directives.unchanged,
    }

    def run(self):
        if self.arguments:
            document = self.state.document
            if self.content:
                return [document.reporter.warning(
                    __('Graphviz directive cannot have both content and '
                       'a filename argument'), line=self.lineno)]
            argument = search_image_for_language(self.arguments[0], self.env)
            rel_filename, filename = self.env.relfn2path(argument)
            self.env.note_dependency(rel_filename)
            try:
                with open(filename, encoding='utf-8') as fp:
                    dotcode = fp.read()
            except OSError:
                return [document.reporter.warning(
                    __('External Graphviz file %r not found or reading '
                       'it failed') % filename, line=self.lineno)]
        else:
            dotcode = '\n'.join(self.content)
            if not dotcode.strip():
                return [self.state_machine.reporter.warning(
                    __('Ignoring "graphviz" directive without content.'),
                    line=self.lineno)]
        node = DiagramNode()
        node['code'] = dotcode
        node['options'] = {'docname': self.env.docname}

        if 'graphviz_dot' in self.options:
            node['options']['layout'] = self.options['graphviz_dot']
        if 'layout' in self.options:
            node['options']['layout'] = self.options['layout']
        if 'alt' in self.options:
            node['alt'] = self.options['alt']
        if 'align' in self.options:
            node['align'] = self.options['align']

        self.add_name(node)
        return [node]


def setup(app):
    app.add_node(DiagramNode,
                 html=(html_visit_diagramascode, None),)
    app.add_directive('diagramascode', DiagramAsCode)

    app.add_config_value('diagramascode', 'python_interpreter', 'python')
    return {'version': __version__, 'parallel_read_safe': True}
