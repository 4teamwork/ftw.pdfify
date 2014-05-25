from ftw.pdfify import ASYNC_CONVERT_JOB
from ftw.pdfify import STATE_CONVERTING
from ftw.pdfify.interfaces import IPdf
from plone.uuid.interfaces import IUUID
import transaction


def queue_pdf_conversion(succeeded, url, uuid, filename, content_type):
    if succeeded:
        ASYNC_CONVERT_JOB.delay(url, uuid, filename, content_type)


def handle_pdf_conversion(context, event):
    pdf = IPdf(context)
    if not pdf.has_current_pdf():
        pdf.storage.checksum = pdf.current_hash
        pdf.storage.status = STATE_CONVERTING
        url = pdf.generate_url()
        uuid = IUUID(pdf.context)
        filename = pdf.primary_value.filename
        content_type = pdf.primary_value.content_type

        transaction.get().addAfterCommitHook(queue_pdf_conversion, args=(url,
            uuid, filename, content_type))
