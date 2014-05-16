from ftw.builder import Builder
from ftw.builder import create
from ftw.pdfify.interfaces import IPdf
from ftw.pdfify.interfaces import IPdfStorage
from ftw.pdfify.interfaces import IPdfifyable
from ftw.pdfify.tests.base import FunctionalTestCase
from ftw.testbrowser import browsing
import transaction


class TestPdfifyView(FunctionalTestCase):

    def setUp(self):
        super(TestPdfifyView, self).setUp()

        self.file = create(Builder('file')
                           .providing(IPdfifyable)
                           .with_dummy_content())

        IPdf(self.file).convert_to_pdf()
        self.token = IPdf(self.file).storage.token
        transaction.commit()

    @browsing
    def test_get_request_is_handled_as_fetch_document(self, browser):
        browser.open( self.file, view='pdfify?token={0}'.format(self.token))

        self.assertEquals('text/plain; charset=iso-8859-15',
                          browser.headers.get('content-type'))
        self.assertEquals('Test data', browser.contents)

    @browsing
    def test_post_request_is_handled_as_put_pdf(self, browser):
        browser.webdav('POST', self.file, view='pdfify',
                       data={'token':self.token, 'data':'__PDF_DATA__'})

        transaction.begin()

        blob = IPdfStorage(self.file).retrieve()
        _blob = blob.open('r')

        self.assertEquals('__PDF_DATA__', _blob.read())

        _blob.close()
