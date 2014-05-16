from ftw.pdfify.interfaces import IPdf


def start_pdf_conversion(context, event):
    IPdf(context).convert_to_pdf()
