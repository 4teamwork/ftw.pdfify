from ftw.builder.testing import BUILDER_LAYER
from ftw.builder.testing import functional_session_factory
from ftw.builder.testing import set_builder_session_factory
from plone.app.testing import FunctionalTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing.z2 import ZSERVER_FIXTURE
from zope.configuration import xmlconfig


# patch ASYNC_CONVERT_JOB we don't wanna setup the celery stuffx
TESTING_CONVERSION_JOB_QUEUE = []



class MockedConvertJob(object):

    def delay(self, url, uuid, filename, contenttype):
        TESTING_CONVERSION_JOB_QUEUE.append(
            {'url': url, 'uuid': uuid,
             'filename': filename, 'contenttype': contenttype})


from ftw import pdfify
pdfify.ASYNC_CONVERT_JOB = MockedConvertJob()


class PdfifyLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, BUILDER_LAYER, ZSERVER_FIXTURE)

    def setUpZope(self, app, configurationContext):
        import ftw.pdfify
        xmlconfig.file('configure.zcml',
                       ftw.pdfify,
                       context=configurationContext)


PDFIFY_FIXTURE = PdfifyLayer()
PDFIFY_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(PDFIFY_FIXTURE,
           set_builder_session_factory(functional_session_factory)),
    name="ftw.pdfify:functional")
