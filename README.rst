#############
astro_imaging
#############

Description
===========

``astro_imaging`` is a pure Python library designed for downloading and using public astronomical imaging data,
mainly from the `Subaru Hyper-Suprime Cam Strategic Survey Program Public Data Releases <https://hsc.mtk.nao.ac.jp/ssp/data-release/>`_.

Installation
============
Install with ``python -m pip install .``.

If you encounter dependency issues, install `poetry <https://python-poetry.org/>`_ and run ``poetry export -f requirements.txt > requirements.txt``.

Configuration
=============

Files are currently stored in a path specified by the ``ASTRO_IMAGING_DATA_PATH`` environment variable. If undefined, images will be downloaded in the current working directory.

To download files without having to specify a username and password every time, create a ``.netrc`` file in your home directory with the following line for each server:

``echo "machine hsc-release.mtk.nao.ac.jp login your-username password your-password" >> ~/.netrc``

... with appropriate permissions (i.e., ``chmod 600 ~/.netrc``).

Notes
=====

If you encounter any problems or would like to make a contribution, please file an issue.

Users wanting more HSC-specific features should consider `unagi <https://github.com/dr-guangtou/unagi>`_.
