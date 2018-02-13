# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
import logging
import json

_logger = logging.getLogger(__name__)

API_ENDPOINT = 'https://api.twitter.com'
API_VERSION = '1.1'
REQUEST_TOKEN_URL = '%s/oauth2/token' % API_ENDPOINT
REQUEST_TWEETS_BY_HASHTAG_URL = '%s/%s/search/tweets.json' % \
                                (API_ENDPOINT, API_VERSION)
URLOPEN_TIMEOUT = 10


class Website(models.Model):
    # Based on the code of website_twitter module,
    # but with very slight modifications to enable hashtag-based tweet fetching

    _inherit = 'website'

    _TWITTER_SEARCH_MODES = [('favorites', 'Favorites'),
                             ('hashtag', 'By Hashtag')]

    twitter_search_mode = fields.Selection(
        selection=_TWITTER_SEARCH_MODES,
        string='Twitter Search Mode',
        default='favorites'
    )
    twitter_hashtag = fields.Char(
        string='Hashtag',
        help='Hashtag to search',
    )

    @api.model
    def _refresh_hashtag_tweets(self):
        # called by cron job
        website = self.env['website'].search([
            ('twitter_api_key', '!=', False),
            ('twitter_api_secret', '!=', False),
            ('twitter_hashtag', '!=', False)
        ])
        msg = _("Refreshing hashtag tweets for website IDs: %r") % website.ids
        _logger.debug(msg)

        website.fetch_hashtag_tweets()

    @api.multi
    def fetch_hashtag_tweets(self):
        WebsiteTweets = self.env['website.twitter.tweet']
        tweet_ids = []
        for website in self:
            if not all((website.twitter_api_key, website.twitter_api_secret,
                        website.twitter_hashtag)):
                msg = _("Skip fetching favorite tweets for unconfigured "
                        "website %s" % website)
                _logger.debug(msg)
                continue

            params = {
                'q': website.twitter_hashtag
            }

            last_tweet = WebsiteTweets.search([
                ('website_id', '=', website.id),
                ('hashtag', '=', website.twitter_hashtag)
            ], limit=1, order='tweet_id desc')

            if last_tweet:
                params['since_id'] = int(last_tweet.tweet_id)

            msg = _("Fetching hashtag tweets using params %r" % params)
            _logger.debug(msg)

            response = self._request(
                website, REQUEST_TWEETS_BY_HASHTAG_URL, params=params
            )

            for tweet_dict in response['statuses']:
                tweet_id = tweet_dict['id']  # unsigned 64-bit snowflake ID
                tweet_ids = WebsiteTweets.search([
                    ('tweet_id', '=', tweet_id)
                ]).ids

                if not tweet_ids:
                    new_tweet = WebsiteTweets.create(
                        {
                            'website_id': website.id,
                            'tweet': json.dumps(tweet_dict),
                            'tweet_id': tweet_id,  # stored in NUMERIC PG field
                            'screen_name': website.twitter_screen_name,
                            'hashtag': website.twitter_hashtag,
                        })

                    msg = _("Found new tweet by hashtag: %r, %r" %
                            (tweet_id, tweet_dict))
                    _logger.debug(msg)

                    tweet_ids.append(new_tweet.id)

        return tweet_ids
