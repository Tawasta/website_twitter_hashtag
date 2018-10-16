# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ResConfigSettings(models.TransientModel):

    _inherit = 'res.config.settings'

    _TWITTER_SEARCH_MODES = [
        ('favorites', 'Favorites'),
        ('hashtag', 'By Hashtag')
    ]

    @api.multi
    def purge_tweets(self):
        self.ensure_one()
        self.env['website.twitter.tweet'].search(args=[]).unlink()

    twitter_search_mode = fields.Selection(
        selection=_TWITTER_SEARCH_MODES,
        related='website_id.twitter_search_mode',
        string='Twitter Search Mode',
        default='favorites'
    )
    twitter_hashtag = fields.Char(
        related='website_id.twitter_hashtag',
        string='Hashtag',
        help='Hashtag to search',
    )
