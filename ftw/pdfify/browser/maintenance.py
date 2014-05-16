from ftw.pdfify.interfaces import IPdf
from zope.publisher.browser import BrowserView


class PdfifyMaintenanceView(BrowserView):

    def start_pdf_conversion(self):
        pdfier = IPdf(self.context)
        pdfier.convert_to_pdf()

        return pdfier.storage.token
