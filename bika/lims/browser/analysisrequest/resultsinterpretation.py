# -*- coding: utf-8 -*-
#
# This file is part of SENAITE.CORE
#
# Copyright 2018 by it's authors.
# Some rights reserved. See LICENSE.rst, CONTRIBUTORS.rst.

from bika.lims import bikaMessageFactory as _
from bika.lims import logger
from bika.lims.browser import BrowserView
from bika.lims.permissions import FieldEditResultsInterpretation
from plone import protect
from plone.app.textfield import RichTextValue
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class ARResultsInterpretationView(BrowserView):
    """ Renders the view for ResultsInterpration per Department
    """
    template = ViewPageTemplateFile(
        "templates/analysisrequest_results_interpretation.pt")

    def __init__(self, context, request, **kwargs):
        super(ARResultsInterpretationView, self).__init__(context, request)
        self.context = context

    def __call__(self):
        if self.request.form.get("submitted", False):
            self.handle_form_submit()
        return self.template()

    def handle_form_submit(self):
        """Handle form submission
        """
        protect.CheckAuthenticator(self.request)
        logger.info("Handle ResultsInterpration Submit")
        # Save the results interpretation
        res = self.request.form.get("ResultsInterpretationDepts", [])
        self.context.setResultsInterpretationDepts(res)
        self.add_status_message(_("Changes Saved"), level="info")

    def add_status_message(self, message, level="info"):
        """Set a portal status message
        """
        return self.context.plone_utils.addPortalMessage(message, level)

    def is_edit_allowed(self):
        """Check if edit is allowed
        """
        checkPermission = self.context.portal_membership.checkPermission
        return checkPermission(FieldEditResultsInterpretation, self.context)

    def get_text(self, department, mode="raw"):
        """Returns the text saved for the selected department
        """
        row = self.context.getResultsInterpretationByDepartment(department)
        rt = RichTextValue(row.get("richtext", ""), "text/plain", "text/html")
        if mode == "output":
            return rt.output
        return rt.raw
