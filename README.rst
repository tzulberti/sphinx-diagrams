=============================
sphinxcontrib-sphinx-diagrams
=============================

.. image:: https://travis-ci.org/tzulberti/sphinxcontrib-sphinx-diagrams.svg?branch=master
    :target: https://travis-ci.org/tzulberti/sphinxcontrib-sphinx-diagrams

Sphinx extension for the `Diagrams <https://github.com/mingrammer/diagrams>`__
package

Overview
--------

Add the ``diagramascode`` directive that will allow to render the diagram
when building the documentation.

To use, add ``sphinxcontrib.diagramsascode`` to the ``extensions`` variable
on the Sphinx configuration.

Create the diagrams in the rST files

::

    .. diagramascode::

        from diagrams import Diagram
        from diagrams.aws.compute import EC2
        from diagrams.aws.database import RDS
        from diagrams.aws.network import ELB

        with Diagram("Grouped Workers", show=False, direction="TB"):
            ELB("lb") >> [EC2("worker1"),
                        EC2("worker2"),
                        EC2("worker3"),
                        EC2("worker4"),
                        EC2("worker5")] >> RDS("events")

When building the HTML documentation, this will add the final image.


Links
-----

- Source: https://github.com/tzulberti/sphinxcontrib-sphinx-diagrams
- Bugs: https://github.com/tzulberti/sphinxcontrib-sphinx-diagrams/issues
