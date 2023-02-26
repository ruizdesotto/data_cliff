=====
Usage
=====

To use Data Cliff in a project::

    cliff [a_rev] [b_rev] path/to/file

Where ``a_rev`` and ``b_rev`` are the two git revisions to which you want to compare
``path/to/file``

Example::

    cliff main test config/configuration.json

The git revisions are optional, if they are not given they will default
to ``a_rev=HEAD`` and ``b_rev=None`` (current changes)
