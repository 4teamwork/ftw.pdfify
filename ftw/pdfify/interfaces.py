from zope.component.interfaces import IObjectEvent
from zope.interface import Attribute
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


class IPdfReadyEvent(IObjectEvent):
    """An event signalling that a PDF conversion of the given object occured.
    """
    object = Attribute("The file object that was converted into a PDF.")
