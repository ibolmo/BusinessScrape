# Scrapy settings for McAllen project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = ''

SPIDER_MODULES = ['McAllen.spiders', 'Mission.spiders', 'Edinburg.spiders', 'TexasTransparency.spiders']

#DOWNLOAD_DELAY = 10

CLOSESPIDER_ERRORCOUNT = 1

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'McAllen (+http://www.yourdomain.com)'
