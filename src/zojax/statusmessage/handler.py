##############################################################################
#
# Copyright (c) 2008 Zope Foundation and Contributors.
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
from zope import component
from zope.publisher.interfaces.browser import IBrowserRequest
from zojax.cacheheaders.interfaces import IAfterCallEvent

from interfaces import IStatusMessage


@component.adapter(IAfterCallEvent)
def afterCallHandler(event):
    request = event.request
    if IBrowserRequest.providedBy(request):
        response = request.response

        status = response.getStatus()
        if status not in (302, 303):
            service = IStatusMessage(request, None)
            if service is not None:
                messages = service.clear()

                if messages:
                    msg = u'\n'.join(messages)
                    msg = msg.encode('utf-8', 'ignore')

                    body = response.consumeBody()
                    body = body.replace('<!--zojax-statusmessage-->', msg, 1)
                    response.setResult(body)
