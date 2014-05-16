from ftw.pdfify.interfaces import IPdf
from zope.publisher.browser import BrowserView


class PdfifyMaintenanceView(BrowserView):

    def start_pdf_conversion(self):
        """Starts the pdf conversion for the current context."""

        pdfier = IPdf(self.context)
        pdfier.convert_to_pdf()

        return pdfier.storage.token

    def pdf(self):
        """Returns the pdf for the saved context."""

        return IPdf(self.context).pdf_download()
