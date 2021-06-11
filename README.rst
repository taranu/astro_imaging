#############
astro_imaging
#############

Description
===========

``astro_imaging`` is a pure Python library designed mainly for downloading and using public data,
mainly from the `Subaru Hyper-Suprime Cam Strategic Survey Program Public Data Releases <https://hsc.mtk.nao.ac.jp/ssp/data-release/>`_.

Installation
============
Install with ``python -m pip install .``.

If you encounter dependency issues, install `poetry <https://python-poetry.org/>`_ and run ``poetry export -f requirements.txt > requirements.txt``.

Configuration
=============

Files are currently stored in a path specified by the ``ASTRO_IMAGING_DATA_PATH`` environment variable. If undefined, images will be downloaded in the current working directory.
