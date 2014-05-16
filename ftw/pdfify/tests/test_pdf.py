from ftw.builder import Builder
from ftw.builder import create
from ftw.pdfify import STATE_CONVERTING
from ftw.pdfify import STATE_OK
from ftw.pdfify.interfaces import IPdf
from ftw.pdfify.interfaces import IPdfStorage
from ftw.pdfify.interfaces import IPdfifyable
from ftw.pdfify import testing
from ftw.pdfify.tests.base import FunctionalTestCase
import hashlib


class TestPdfAdapter(FunctionalTestCase):

    def setUp(self):
        super(TestPdfAdapter, self).setUp()

        self.file = create(Builder('file')
                           .providing(IPdfifyable)
                           .with_dummy_content())

    def test_current_hash_returns_md5_hash_of_the_primary_field_value(self):
        self.assertEquals(
            hashlib.md5("Test data").digest(),
            IPdf(self.file).current_hash())

    def test_has_current_pdf_is_false_when_conversion_is_running(self):
        storage = IPdfStorage(self.file)
        storage.status = STATE_CONVERTING

        self.assertFalse(IPdf(self.file).has_current_pdf())

    def test_has_current_pdf_is_true_when_conversion_is_ok_and_checksum_is_not_changed(self):
        pdfadapter = IPdf(self.file)

        storage = IPdfStorage(self.file)
        storage.status = STATE_OK

        self.assertTrue(pdfadapter.has_current_pdf())

    def test_verify_token_compare_with_the_token_in_the_storage(self):

        IPdfStorage(self.file).token = 'e2e5e8cd172775b4e8268acd1c88bba0'

        self.assertTrue(
            IPdf(self.file).verify_token('e2e5e8cd172775b4e8268acd1c88bba0'))

        self.assertFalse(
            IPdf(self.file).verify_token('0389bd531d52d3761fe12d1ee3f21975'))


class TestConvertToPdf(FunctionalTestCase):

    def setUp(self):
        super(TestConvertToPdf, self).setUp()

        self.file = create(Builder('file')
                           .providing(IPdfifyable)
                           .with_dummy_content())

        testing.TESTING_CONVERSION_JOB_QUEUE = []

    def test_updates_checksum(self):
        self.file.getPrimaryField().set(self.file, 'Updated Data')

        IPdf(self.file).convert_to_pdf()

        self.assertEquals(
            hashlib.md5('Updated Data').digest(),
            IPdfStorage(self.file).checksum)

    def test_set_converting_state(self):
        IPdf(self.file).convert_to_pdf()
        self.assertEquals(
            STATE_CONVERTING,
            IPdfStorage(self.file).status)

    def test_generates_url_with_new_token(self):
        IPdfStorage(self.file).token = 'Old Token'

        IPdf(self.file).convert_to_pdf()
        queued_job = testing.TESTING_CONVERSION_JOB_QUEUE[0]
        new_token = IPdfStorage(self.file).token

        self.assertNotEquals('Old Token', new_token)
        self.assertEquals(
            'http://localhost:55001/plone/file/pdfify?token=%s' % (new_token),
            queued_job.get('url'))

    def test_pass_when_pdf_is_already_present(self):
        pdf = IPdf(self.file)
        pdf.convert_to_pdf()
        pdf.store_pdf('__PDF DATA__')

        self.assertEquals(1, len(testing.TESTING_CONVERSION_JOB_QUEUE))

        IPdf(self.file).convert_to_pdf()

        self.assertEquals(1, len(testing.TESTING_CONVERSION_JOB_QUEUE))
