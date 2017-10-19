# -*- coding: utf-8 -*-
from collective.selectivelogin import _
from collective.selectivelogin.interfaces import ISelectiveLoginSettings
from plone.app.registry.browser import controlpanel


class SelectiveLoginSettingsEditForm(controlpanel.RegistryEditForm):

    schema = ISelectiveLoginSettings
    label = _(u'Selective Login Settings')
    description = u""

    def updateFields(self):
        super(SelectiveLoginSettingsEditForm, self).updateFields()

    def updateWidgets(self):
        super(SelectiveLoginSettingsEditForm, self).updateWidgets()


class SelectiveLoginSettingsEditFormSettingsControlPanel(
    controlpanel.ControlPanelFormWrapper
):
    form = SelectiveLoginSettingsEditForm
