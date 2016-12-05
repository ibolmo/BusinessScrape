import re, urllib2
from urlparse import urlparse
from urllib2 import Request, urlopen, HTTPError

class WebsitePipeline(object):

	def process_item(self, item, spider):
		item['is_google_apps'] = False

		if item['website'] and re.match(r'^https?:\/\/$', item['website']):
			item['website'] = ''
		else:
			url = urlparse(item['website'])
			req = Request('https://www.google.com/a/%s' % url.netloc)
			try:
				urlopen(req)
			except HTTPError as e:
				if e.code < 500:
					item['is_google_apps'] = True

		return item

