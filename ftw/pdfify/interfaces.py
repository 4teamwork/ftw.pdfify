from zope.interface import Interface


class IPdfifyable(Interface):
    """Marker interface for objects,
    which provides document to pdf conversion."""


class IPdfStorage(Interface):

    def __init__(context):
        """
        """

    def store(data):
        """
        """

    def retrieve():
        """
        """


class IPdf(Interface):

    def __init__(context):
        """
        """

    def verify_token(token):
        """
        """
