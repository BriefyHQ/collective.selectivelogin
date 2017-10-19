"""Login handlers."""
from AccessControl.SecurityManagement import noSecurityManager
from collective.selectivelogin import utils
from plone import api
from Products.statusmessages.interfaces import IStatusMessage
from zope.globalrequest import getRequest


def login_handler(event):
    """Validate if this login is valid or not."""
    user = event.object
    if utils.is_enabled() and not utils.validate_user_domain(user):
        noSecurityManager()
        request = getRequest()
        api.portal.show_message(
            message=utils.get_error_message(),
            request=request,
            type='error'
        )
