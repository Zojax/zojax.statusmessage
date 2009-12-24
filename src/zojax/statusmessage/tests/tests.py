##############################################################################
#
# Copyright (c) 2007 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
""" zojax.statusmessage tests

$Id$
"""
import os, unittest, doctest
from zope.app.testing import setup

from zope import interface, component
from zope.component import provideAdapter
from zope.session.interfaces import ISession, ISessionDataContainer
from zope.session.session import RAMSessionDataContainer
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.app.testing.functional import ZCMLLayer
from zope.app.testing.functional import FunctionalDocFileSuite
from zope.traversing.testing import setUp as setUpTraversing
from zojax.statusmessage import message


statusmessageLayer = ZCMLLayer(
    os.path.join(os.path.split(__file__)[0], 'ftesting.zcml'),
    __name__, 'statusmessageLayer', allow_teardown=True)


class Session(dict):

    def __getitem__(self, key):
        if not self.has_key(key):
            self[key] = {}

        return super(Session, self).__getitem__(key)

session = Session()

@interface.implementer(ISession)
@component.adapter(IBrowserRequest)
def getSession(request):
    return session


def setUp(test):
    setup.placelessSetUp()
    setUpTraversing()
    component.provideAdapter(getSession)
    component.provideAdapter(message.StatusMessage, name='statusMessage')
    component.provideUtility(RAMSessionDataContainer(), ISessionDataContainer)


def tearDown(test):
    session.__init__()
    setup.placelessTearDown()


def test_suite():
    testbrowser = FunctionalDocFileSuite(
        "testbrowser.txt",
        optionflags=doctest.ELLIPSIS|doctest.NORMALIZE_WHITESPACE)
    testbrowser.layer = statusmessageLayer

    return unittest.TestSuite((
            testbrowser,
            doctest.DocFileSuite(
                '../README.txt',
                setUp=setUp, tearDown=tearDown,
                optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS),
            ))
