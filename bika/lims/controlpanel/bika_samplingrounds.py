# -*- coding: utf-8 -*-
#
# This file is part of SENAITE.CORE
#
# Copyright 2018 by it's authors.
# Some rights reserved. See LICENSE.rst, CONTRIBUTORS.rst.

from bika.lims import bikaMessageFactory as _
from bika.lims.browser.bika_listing import BikaListingView
from plone.dexterity.content import Container
from plone.supermodel import model
from zope.interface import implements


class SamplingRoundsView(BikaListingView):
    """Displays all system's sampling rounds
    """

    def __init__(self, context, request):
        super(SamplingRoundsView, self).__init__(context, request)
        self.catalog = "portal_catalog"
        self.contentFilter = {
            'portal_type': 'SamplingRound',
            'sort_on': 'sortable_title'
        }

        self.show_select_row = False
        self.show_select_column = True
        self.pagesize = 25
        self.form_id = "samplinground"
        self.icon = self.portal_url + "/++resource++bika.lims.images/instrumentcertification_big.png"
        self.title = self.context.translate(_("Sampling Rounds"))
        self.description = ""
        # Hide the ugly edit-bar with 'new', 'draft', etc
        # self.request.set('disable_border', 1)
        self.columns = {
            'title': {'title': _('Title'),
                      'sortable': True,
                      'toggle': True,
                      'replace_url': 'absolute_url'},
            'Description': {'title': _('Description')},
            'num_sample_points': {'title': _('Number of sampling points'),
                                    'index': 'sortable_title'},
            'num_containers': {'title': _('Number of containers'),
                               'index': 'sortable_title'},
        }
        self.review_states = [
            {'id': 'default',
             'title':  _('Open'),
             'contentFilter': {'review_state': 'open'},
             'columns': ['title',
                         'Description',
                         'num_sample_points',
                         'num_containers',
                         ]
             },
             {'id': 'closed',
             'contentFilter': {'review_state': 'closed'},
             'title': _('Closed'),
             'transitions': [{'id': 'open'}],
             'columns': ['title',
                         'Description',
                         'num_sample_points',
                         'num_containers',
                         ]
             },
            {'id': 'cancelled',
             'title': _('Cancelled'),
             'transitions': [{'id': 'reinstate'}],
             'contentFilter': {'review_state': 'cancelled'},
             'columns': ['title',
                         'Description',
                         'num_sample_points',
                         'num_containers',
                         ]
             },
            {'id': 'all',
             'title': _('All'),
             'transitions': [],
             'contentFilter':{},
             'columns': ['title',
                         'Description',
                         'num_sample_points',
                         'num_containers',
                         ]
             },
        ]

    def before_render(self):
        """Before template render hook
        """
        # Don't allow any context actions
        self.request.set("disable_border", 1)


class ISamplingRounds(model.Schema):
    """ A Sampling Rounds container.
    """


class SamplingRounds(Container):
    implements(ISamplingRounds)
    displayContentsTab = False
