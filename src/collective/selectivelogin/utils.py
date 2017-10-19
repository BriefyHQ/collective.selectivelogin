# -*- coding: utf-8 -*-
from collective.selectivelogin.interfaces import ISelectiveLoginSettings
from plone import api


def is_enabled():
    """Check if Selective Login is enabled for this Portal.

    :returns: If Selective Login is enabled for this portal.
    :rtype: bool
    """
    try:
        value = api.portal.get_registry_record('enabled', interface=ISelectiveLoginSettings)
    except KeyError:
        value = False
    return value


def allowed_domains():
    """Whitelist of email domains we accept logins from.

    :returns: List of whitelisted domains.
    :rtype: list
    """
    allowed_domains = api.portal.get_registry_record(
        'allowed_domains',
        interface=ISelectiveLoginSettings
    ) or ''
    return [d.strip() for d in allowed_domains.split('\n') if d.strip()]


def get_error_message():
    """Error message to be displayed to users when their login fails.

    :returns: Error message to be displayed to the user.
    :rtype: unicode
    """
    error_message = api.portal.get_registry_record(
        'error_message',
        interface=ISelectiveLoginSettings
    ) or u'Invalid domain.'
    return error_message


def user_domain(user):
    """Extract email domain from user object.

    :param user: A user in the portal.
    :type user: MemberData object
    :returns: Email domain for the given user.
    :rtype: str
    """
    domain = ''
    email = user.getProperty('email')
    if email:
        domain = email.split('@')[-1]
    return domain


def validate_user_domain(user):
    """Validate if user email domain is whitelisted for logins on this portal.

    :param user: A user in the portal.
    :type user: MemberData object
    :returns: If user email domain is whitelisted for login.
    :rtype: bool
    """
    domain = user_domain(user)
    return domain in allowed_domains()
