from ftw.pdfify.testing import PDFIFY_FUNCTIONAL_TESTING
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from unittest2 import TestCase


class FunctionalTestCase(TestCase):

    layer = PDFIFY_FUNCTIONAL_TESTING

    def setUp(self):
        super(FunctionalTestCase, self).setUp()

        self.portal = self.layer['portal']
        self.set_testuser_manager_role()

    def tearDown(self):
        super(FunctionalTestCase, self).tearDown()

    def set_testuser_manager_role(self):
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
