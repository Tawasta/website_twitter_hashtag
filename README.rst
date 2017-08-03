.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

==================================
Hashtag support for Twitter Roller
==================================

Extends the website_twitter module to have the option to show tweets based on a hashtag instead of a specific user's favorited tweets

Installation
============
* Install this module and website_twitter
* Installing this module automatically deactivates website_twitter module's scheduler for fetching favorited tweets

Configuration
=============
* Go to Website Admin -> Configuration and set your Twitter API Key and Twitter API Secret as you would with the website_twitter module
* In the same view, set the Twitter search mode to "By hashtag", and type the hashtag in the new field, e.g. "#odoo"
* Reconfigure the "Fetch new tweets by hashtag" scheduler's frequency in Settings -> Scheduled actions if needed. The default frequency is every 2 hours.
* Note: the front-end has not been edited. It does not do any tweet filtering based on hashtags or favorites - it shows whatever has been fetched from Twitter API to Odoo DB. If you had website_twitter in use previously and it has already fetched some favorited tweets, you probably want to delete them so they don't show up in roller anymore after switching to hashtags. This can be done with the "Delete saved tweets" button.

Usage
=====
* Drag and drop the Twitter Roller block to your website
* The roller becomes visible and functional when there are 12 tweets in total. Note that the Twitter search API only fetches tweets from the past week, so if you use a hashtag with older content, the tweets will not show up.

Known issues / Roadmap
======================
* Add support for multiple hashtags
* Port completely to new API (website_twitter still uses old API in 9.0, so does this module partly)

Credits
=======

Contributors
------------
* Timo Talvitie <timo@vizucom.com>

Maintainer
----------
.. image:: http://vizucom.com/logo.png
   :alt: Vizucom Oy
   :target: http://www.vizucom.com


This module is maintained by Vizucom Oy