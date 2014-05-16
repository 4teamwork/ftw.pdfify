from ZPublisher.Iterators import filestream_iterator
from ftw.pdfify.interfaces import IPdf
from zExceptions import Unauthorized
from zope.publisher.browser import BrowserView


class PdfifyView(BrowserView):

    def __call__(self):
        self.verify_token()

        if self.request.environ.get('REQUEST_METHOD') == 'POST':
            return self.put_pdf()
        else:
            return self.stream_orginal_document()

    def verify_token(self):
        """If token is verified it returns True
        otherwise raise a Unauthorized Exception."""

        token = self.request.get('token')
        if token:
            if IPdf(self.context).verify_token(token):
                return True

        raise Unauthorized

    def stream_orginal_document(self):
        blob = IPdf(self.context).primary_value.blob
        filename = blob._p_blob_uncommitted or blob.committed()
        return filestream_iterator(filename, 'rb')

    def put_pdf(self):
        data = self.request.get('data')
        if not data:
            raise ValueError('PdfifyView  needs pdf data.')

        IPdf(self.context).store_pdf(data)

        return 'hans'
