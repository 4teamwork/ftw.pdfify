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

        token = self.request.form.get('token')
        if token:
            if IPdf(self.context).verify_token(token):
                return True

        self.request.response.setStatus(401)
        self.request.response.setHeader('WWW-Authenticate', 'Token')
        return

    def stream_orginal_document(self):
        return IPdf(self.context).primary_download

    def put_pdf(self):
        data = self.request.form.get('file')
        if not data:
            raise ValueError('PdfifyView  needs pdf data.')

        IPdf(self.context).store_pdf(data)

        return 'hans'
