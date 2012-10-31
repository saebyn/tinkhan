# vim: set fileencoding=utf-8 ft=python ff=unix nowrap tabstop=4 shiftwidth=4 softtabstop=4 smarttab shiftround expandtab :
"""
Utilities for Tin Can Statement generation.
"""


class StatementSource(object):
    """
    A source of statements for the TCAPI.
    """
    def get(self):
        """
        return list of dicts representing statements
        """
        raise NotImplementedError

    def commit(self):
        """
        mark source of statements as being synchronized
        """
        raise NotImplementedError
