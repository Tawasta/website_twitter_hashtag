# -*- coding: utf-8 -*-
from openerp import models, fields


class Tweet(models.Model):

    _inherit = 'website.twitter.tweet'

    hashtag = fields.Char('Hashtag', help='''What hashtag was searched to find this tweet. ''')