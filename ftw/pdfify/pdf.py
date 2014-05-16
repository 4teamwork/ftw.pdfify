from Products.CMFPlone.utils import safe_hasattr
from ZPublisher.Iterators import filestream_iterator
from ftw.pdfify import ASYNC_CONVERT_JOB
from ftw.pdfify import STATE_CONVERTING
from ftw.pdfify import STATE_OK
from ftw.pdfify.interfaces import IPdf
from ftw.pdfify.interfaces import IPdfStorage
from ftw.pdfify.interfaces import IPdfifyable
from plone.rfc822.interfaces import IPrimaryFieldInfo
from plone.uuid.interfaces import IUUID
from zope.component import adapts
from zope.interface import implements
import hashlib
import time


class Pdf(object):
    implements(IPdf)
    adapts(IPdfifyable)

    def __init__(self, context):
        self.context = context
        self.storage = IPdfStorage(self.context)

    @property
    def primary_value(self):
        if safe_hasattr(self.context, 'getPrimaryField'):
            return self.context.getPrimaryField().get(self.context)
        else:
            return IPrimaryFieldInfo(self.context).value

    @property
    def status(self):
        return self.storage.status

    @property
    def current_hash(self):
        return hashlib.md5(self.primary_value.data).digest

    def generate_url(self):
        self.storage.token = self.generate_token()
        return '%s/pdfify?token=%s' % (
            self.context.absolute_url(), self.storage.token)
        self.context

    def generate_token(self):
        # TODO improve security
        return hashlib.md5(
            '%s%f' % (self.context.Title(), time.time())).hexdigest()

    def verify_token(self, token):
        return self.storage.token == token

    def has_current_pdf(self):
        if self.storage.status == STATE_OK:
            return self.current_hash() == self.storage.checksum

        return False

    def convert_to_pdf(self):
        if not self.has_current_pdf():
            self.storage.checksum = self.current_hash()
            self.storage.status = STATE_CONVERTING

            ASYNC_CONVERT_JOB(self.generate_url(),
                              IUUID(self.context),
                              self.primary_value.filename,
                              self.primary_value.content_type)

    def store_pdf(self, data):
        self.storage.store(data)
        self.storage.status = STATE_OK

    def pdf(self):
        pdf = self.storage.retrieve()
        filename = pdf._p_blob_uncommitted or pdf._blob.committed()
        return filestream_iterator(filename, 'rb')
