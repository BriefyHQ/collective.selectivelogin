# -*- coding: utf-8 -*-
"""Control Panel."""
from collective.selectivelogin import _
from collective.selectivelogin.interfaces import ISelectiveLoginSettings
from plone.app.registry.browser import controlpanel


class SelectiveLoginSettingsEditForm(controlpanel.RegistryEditForm):
    """Edit Form."""

    schema = ISelectiveLoginSettings
    label = _(u'Selective Login Settings')
    description = u''

    def updateFields(self):
        super(SelectiveLoginSettingsEditForm, self).updateFields()

    def updateWidgets(self):
        super(SelectiveLoginSettingsEditForm, self).updateWidgets()


class SelectiveLoginSettingsEditFormSettingsControlPanel(
    controlpanel.ControlPanelFormWrapper
):
    """Control panel."""
    form = SelectiveLoginSettingsEditForm
