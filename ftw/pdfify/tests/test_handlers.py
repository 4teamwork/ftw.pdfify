from ftw.builder import Builder
from ftw.builder import create
from ftw.pdfify import testing
from ftw.pdfify.interfaces import IPdf
from ftw.pdfify.interfaces import IPdfifyable
from ftw.pdfify.tests.base import FunctionalTestCase
from ftw.testbrowser import browsing


class TestPdfAdapter(FunctionalTestCase):

    def setUp(self):
        super(TestPdfAdapter, self).setUp()

        self.file = create(Builder('file')
                           .providing(IPdfifyable)
                           .with_dummy_content())

        testing.TESTING_CONVERSION_JOB_QUEUE = []

    @browsing
    def test_modfiyng_a_document_start_pdf_conversion(self, browser):
        browser.login().open(self.file, view='edit')
        browser.fill(
            {'File': ('Raw file data', 'file.txt', 'text/plain')}).submit()

        token = IPdf(self.file).storage.token

        self.assertEquals(1, len(testing.TESTING_CONVERSION_JOB_QUEUE))
        self.assertEquals(
            'http://localhost:55001/plone/file/pdfify?token={0}'.format(token),
            testing.TESTING_CONVERSION_JOB_QUEUE[0].get('url'))
