=====================
Portal status message
=====================

Instead include notification messages directly to template,
developer can use messaging service.

Main interface is IStatusMessage, it is adapter for IBrowserRequest
so we can have different implementations, for example cookie based or session.

By default only session based service implemented.

   >>> from zope import interface, component
   >>> from zope.interface.verify import verifyClass

   >>> from zojax.statusmessage import interfaces, session, message

   >>> verifyClass(interfaces.IStatusMessage, session.MessageService)
   True

   >>> component.provideAdapter(session.getMessageService)

   >>> from zope.publisher.browser import TestRequest
   >>> request = TestRequest()

   >>> service = interfaces.IStatusMessage(request)

   >>> bool(service)
   False

   >>> service.add('Test message')
   Traceback (most recent call last):
   ...
   ComponentLookupError: ...

   >>> service.clear()
   ()


Before we can use message service we need register message type.

   >>> component.provideAdapter(message.InformationMessage, name='info')

   >>> msg = component.getAdapter(request, interfaces.IMessage, 'info')
   >>> print msg.render('Test message')
   <div class="statusMessage">Test message</div>

Now we can add messages.

   >>> service.add('Test message')

   >>> bool(service)
   True

   >>> for msg in service.messages():
   ...     print msg
   <div class="statusMessage">Test message</div>


Let's register another message type.

   >>> component.provideAdapter(message.WarningMessage, name='warning')

   >>> service.add('Warning message', 'warning')

   >>> for msg in service.messages():
   ...     print msg
   <div class="statusMessage">Test message</div>
   <div class="statusWarningMessage">Warning message</div>

Error message, we can add exception object

   >>> component.provideAdapter(message.ErrorMessage, name='error')

   >>> service.add(Exception('Error message'), 'error')

or text message

   >>> service.add('Error message', 'error')

   >>> for msg in service.messages():
   ...     print msg
   <div class="statusMessage">Test message</div>
   <div class="statusWarningMessage">Warning message</div>
   <div class="statusStopMessage">Exception: Error message</div>
   <div class="statusStopMessage">Error message</div>

Serive will oppress duplicated messages:

   >>> service.add('Error message', 'error')
   >>> for msg in service.messages():
   ...     print msg
   <div class="statusMessage">Test message</div>
   <div class="statusWarningMessage">Warning message</div>
   <div class="statusStopMessage">Exception: Error message</div>
   <div class="statusStopMessage">Error message</div>


Clearing service
----------------

clear() method return all messages and clear service.

   >>> for msg in service.clear():
   ...     print msg
   <div class="statusMessage">Test message</div>
   <div class="statusWarningMessage">Warning message</div>
   <div class="statusStopMessage">Exception: Error message</div>
   <div class="statusStopMessage">Error message</div>

   >>> bool(service)
   False
