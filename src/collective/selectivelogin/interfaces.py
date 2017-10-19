# -*- coding: utf-8 -*-
"""Interfaces for collective.selectivelogin."""
from collective.selectivelogin import _
from zope import schema
from zope.interface import Interface


class ISelectiveLoginLayer(Interface):
    """A layer specific for collective.selectivelogin package.

    This interface is referred in browserlayer.xml.

    All views and viewlets register against this layer will appear on
    your Plone site only when the this package is installed.
    """
    pass


class ISelectiveLoginSettings(Interface):
    """Selective Login settings."""

    enabled = schema.Bool(
        title=_(u"Enabled"),
        description=_(
            'help_enabled',
            default=u"Should we validate logins"
        ),
        required=False,
        default=False,
    )

    allowed_domains = schema.Text(
        title=_(u"Allowed email domains"),
        description=_(
            "help_allowed_domains",
            default=u"List of email domains we allow logins from, one per line."
        ),
        default=u''
    )

    error_message = schema.TextLine(
        title=_(u"Error message"),
        description=_(
            "help_error_message",
            default=u"Message to be displayed to users when their email domain is not allowed."
        ),
        default=u'Invalid domain.'
    )
