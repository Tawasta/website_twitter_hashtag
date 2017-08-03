# -*- coding: utf-8 -*-
from openerp.osv import fields, osv
import logging
import json
import urllib

_logger = logging.getLogger(__name__)

API_ENDPOINT = 'https://api.twitter.com'
API_VERSION = '1.1'
REQUEST_TOKEN_URL = '%s/oauth2/token' % API_ENDPOINT
REQUEST_TWEETS_BY_HASHTAG_URL = '%s/%s/search/tweets.json' % (API_ENDPOINT, API_VERSION)
URLOPEN_TIMEOUT = 10


class Website(osv.osv):
    ''' Based on the code of website_twitter module, but with very slight modifications to enable hashtag-based tweet fetching'''

    _inherit = 'website'

    _TWITTER_SEARCH_MODES = [('favorites', 'Favorites'), ('hashtag', 'By Hashtag')]

    def _refresh_hashtag_tweets(self, cr, uid, context=None):
        ''' called by cron job '''
        website = self.pool['website']
        ids = self.pool['website'].search(cr, uid, [('twitter_api_key', '!=', False),
                                                    ('twitter_api_secret', '!=', False),
                                                    ('twitter_hashtag', '!=', False)],
                                          context=context)
        _logger.debug("Refreshing hashtag tweets for website IDs: %r", ids)
        website.fetch_hashtag_tweets(cr, uid, ids, context=context)

    def fetch_hashtag_tweets(self, cr, uid, ids, context=None):
        website_tweets = self.pool['website.twitter.tweet']
        tweet_ids = []
        for website in self.browse(cr, uid, ids, context=context):
            if not all((website.twitter_api_key, website.twitter_api_secret,
                       website.twitter_hashtag)):
                _logger.debug("Skip fetching hashtag tweets for unconfigured website %s",
                              website) 
                continue
            params = {
                'q': website.twitter_hashtag
            }
            last_tweet = website_tweets.search_read(
                    cr, uid, [('website_id', '=', website.id),
                              ('hashtag', '=', website.twitter_hashtag)],
                    ['tweet_id'],
                    limit=1, order='tweet_id desc', context=context)
            if last_tweet:
                params['since_id'] = int(last_tweet[0]['tweet_id'])
            _logger.debug("Fetching hashtag tweets using params %r", params)
            response = self._request(website, REQUEST_TWEETS_BY_HASHTAG_URL, params=params)
            for tweet_dict in response['statuses']:
                tweet_id = tweet_dict['id'] # unsigned 64-bit snowflake ID
                tweet_ids = website_tweets.search(cr, uid, [('tweet_id', '=', tweet_id)])
                if not tweet_ids:
                    new_tweet = website_tweets.create(
                            cr, uid,
                            {
                              'website_id': website.id,
                              'tweet': json.dumps(tweet_dict),
                              'tweet_id': tweet_id, # stored in NUMERIC PG field 
                              'screen_name': website.twitter_screen_name,
                              'hashtag': website.twitter_hashtag,
                            },
                            context=context)
                    _logger.debug("Found new tweet by hashtag: %r, %r", tweet_id, tweet_dict)
                    tweet_ids.append(new_tweet)
        return tweet_ids

    _columns = {
        'twitter_search_mode': fields.selection(_TWITTER_SEARCH_MODES, 'Twitter Search Mode'),
        'twitter_hashtag': fields.char('Hashtag', help='''Hashtag to search''')
    }

    _defaults = {
        'twitter_search_mode': 'favorites'
    }