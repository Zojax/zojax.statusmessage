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
import cgi
from zope import interface, component
from zope.app.pagetemplate import ViewPageTemplateFile
from zope.contentprovider.interfaces import IContentProvider
from zope.publisher.interfaces.browser import IBrowserRequest

from interfaces import IMessage


class Message(object):
    interface.implements(IMessage)
    component.adapts(IBrowserRequest)

    def __init__(self, request):
        self.request = request


class InformationMessage(Message):

    cssClass = 'statusMessage'
    index = ViewPageTemplateFile('message.pt')

    @property
    def context(self):
        return self

    def render(self, message):
        return self.index(message=message)


class WarningMessage(InformationMessage):

    cssClass = 'statusWarningMessage'


class ErrorMessage(InformationMessage):

    cssClass = 'statusStopMessage'

    def render(self, e):
        if isinstance(e, Exception):
            message = '%s: %s'%(e.__class__.__name__, cgi.escape(str(e), True))
        else:
            message = e

        return super(ErrorMessage, self).render(message)


class StatusMessage(object):
    interface.implements(IContentProvider)
    component.adapts(
        interface.Interface, IBrowserRequest, interface.Interface)

    def __init__(self, context, request, view):
        self.context, self.request, self.view = context, request, view

    def update(self):
        pass

    def render(self):
        return u'<!--zojax-statusmessage-->'
