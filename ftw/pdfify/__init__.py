from zope.i18nmessageid import MessageFactory
_ = MessageFactory('ftw.pdfify')


from pdfify_celery.tasks import convert
ASYNC_CONVERT_JOB = convert


# Status
STATE_OK = 1
STATE_CONVERTING = 2
STATE_FAILED = 3
