from ftw.pdfify.interfaces import IPdfReadyEvent
from zope.interface import implements


class PdfReadyEvent(object):
    """An event signalling that a PDF conversion of the given object occured.
    """
    implements(IPdfReadyEvent)

    def __init__(self, obj):
        self.object = obj
