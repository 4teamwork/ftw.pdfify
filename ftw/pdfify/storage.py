from ZODB.blob import Blob
from ftw.pdfify.interfaces import IPdfStorage
from ftw.pdfify.interfaces import IPdfifyable
from persistent.mapping import PersistentMapping
from zope.annotation.interfaces import IAnnotations
from zope.component import adapts
from zope.interface import implements


ANNOTATIONS_STORAGE_KEY = 'ftw.pdfify'


class AnnotationsPdfStorage(object):
    implements(IPdfStorage)
    adapts(IPdfifyable)

    def __init__(self, context):

        self.context = context
        self.storage = IAnnotations(self.context).setdefault(
            ANNOTATIONS_STORAGE_KEY, PersistentMapping())

    def store(self, data):
        blob = Blob()
        _blob = blob.open('w')
        _blob.write(data)
        _blob.close()

        self.storage.update({
            'filename': 'TODO',
            'blob': blob,
            'contenttype': 'TODO'})

    def retrieve(self):
        return self.storage.get('blob')

    @property
    def status(self):
        return self.storage.get('status')

    @status.setter
    def status(self, status):
        self.storage['status'] = status

    @property
    def checksum(self):
        return self.storage.get('checksum')

    @checksum.setter
    def checksum(self, checksum):
        self.storage['checksum'] = checksum

    @property
    def token(self):
        return self.storage.get('token')

    @token.setter
    def token(self, token):
        self.storage['token'] = token
