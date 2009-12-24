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
"""

$Id$
"""
from zope import interface, component
from zope.component import getAdapter, queryUtility
from zope.session.interfaces import ISession, ISessionDataContainer
from zope.publisher.interfaces.browser import IBrowserRequest

from null import NullMessageService
from interfaces import SESSIONKEY, IMessage, IStatusMessage


@component.adapter(IBrowserRequest)
@interface.implementer(IStatusMessage)
def getMessageService(request):
    try:
        session = ISession(request)
    except:
        return NullMessageService(request)

    if queryUtility(ISessionDataContainer) is None:
        return NullMessageService(request)

    return MessageService(request, session)


class MessageService(object):
    """ message service """
    component.adapts(IBrowserRequest, ISession)
    interface.implements(IStatusMessage)

    def __init__(self, request, session):
        self.request = request
        self.session = session

    def add(self, text, type='info'):
        message = getAdapter(self.request, IMessage, type)

        try:
            data = self.session[SESSIONKEY]
            messages = data.get('messages', [])
            text = message.render(text)
            if text not in self.messages():
                messages.append(text)
            data['messages'] = messages
        except Exception, e:
            pass

    def clear(self):
        data = self.session.get(SESSIONKEY)
        if data is not None:
            messages = data.get('messages')
            if messages:
                del data['messages']
                return messages
        return ()

    def messages(self):
        data = self.session.get(SESSIONKEY)
        if data is not None:
            messages = data.get('messages')
            if messages:
                return messages
        return ()

    def __nonzero__(self):
        return bool(self.messages())
