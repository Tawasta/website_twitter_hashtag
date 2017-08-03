# -*- coding: utf-8 -*-
from openerp import models, fields


class WebsiteConfigSettings(models.TransientModel):

    _inherit = 'website.config.settings'

    _TWITTER_SEARCH_MODES = [('favorites', 'Favorites'), ('hashtag', 'By Hashtag')]

    twitter_search_mode = fields.Selection(_TWITTER_SEARCH_MODES, related='website_id.twitter_search_mode', string='Twitter Search Mode', default='favorites')
    twitter_hashtag = fields.Char(related='website_id.twitter_hashtag', string='Hashtag', help='''Hashtag to search''')