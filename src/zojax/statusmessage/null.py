##############################################################################
#
# Copyright (c) 2009 Zope Foundation and Contributors.
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
"""

$Id$
"""
from zope import component, interface
from zope.component import getAdapter
from interfaces import IMessage, IStatusMessage


class NullMessageService(object):
    interface.implements(IStatusMessage)

    def __init__(self, request):
        self.request = request
        self._messages = []

    def add(self, text, type='info'):
        message = getAdapter(self.request, IMessage, type)
        self._messages.append(message.render(text))

    def clear(self):
        self._messages = []

    def messages(self):
        return tuple(self._messages)

    def __nonzero__(self):
        return bool(self._messages)
