"""
    sphinxcontrib.sphinx-diagrams
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Sphinx extension for the Diagrams package

    :copyright: Copyright 2017 by Tomas Zulberti <tzulberti@gmail.com>
    :license: BSD, see LICENSE for details.
"""

import pbr.version

if False:
    # For type annotations
    from typing import Any, Dict  # noqa
    from sphinx.application import Sphinx  # noqa

__version__ = pbr.version.VersionInfo(
    'sphinx-diagrams').version_string()


def setup(app):
    # type: (Sphinx) -> Dict[unicode, Any]
    return {'version': __version__, 'parallel_read_safe': True}
