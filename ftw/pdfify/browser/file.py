from Acquisition import aq_inner
from ftw.file.browser import file_view
from ftw.pdfify.interfaces import IPdf
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName


class FileView(file_view.FileView):

    template = ViewPageTemplateFile('file.pt')

    def has_pdf(self):
        context = aq_inner(self.context)
        return IPdf(context).has_current_pdf()

    def pdf_download(self):
        """Download pdf"""
        context = aq_inner(self.context)
        return IPdf(context).pdf_download()

    def pdf_size(self):
        return IPdf(aq_inner(self.context)).storage.size

    def pdf_link(self):
        context = aq_inner(self.context)
        pdf = IPdf(context)

        utool = getToolByName(context, 'portal_url')
        mtr = getToolByName(context, 'mimetypes_registry')
        pdf_mti = mtr.lookup('application/pdf')[0]
        pdf_icon = '%s/%s' % (utool(), pdf_mti.icon_path)

        return '<a href="%s/pdf_download"><img src="%s" />&nbsp;%s</a>' % (
            context.absolute_url(), pdf_icon, pdf.pdf_filename())
