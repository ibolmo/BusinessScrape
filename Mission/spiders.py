# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

#

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector

from items import Business

import re

class MissionSpider(CrawlSpider):
	name = "mission"
	allowed_domains = ["missionchamber.com", "services.missionchamber.com"]
	start_urls = ["http://services.missionchamber.com/list/QuickLinkMembers/AllCategories.htm"]

	rules = (
		Rule(SgmlLinkExtractor(allow=('\/member\/.+\.htm')), callback='parse_item'),
	)

	def parse_item(self, response):
		hxs = HtmlXPathSelector(response)
		business = Business()
		business['id'] = ''.join(re.findall(r"\-(\d+)\.htm", response.url)).strip()
		business['name'] = self.get_one(hxs, "//div[@class='cm_memheader']//h1/text()")
		business['contact'] = self.get_one(hxs, "//span[@class='cm_repname']//text()")

		contact = self.get_one(hxs, "//td[@class='cm_infotext'][position()<2]/text()")
		bits = re.findall(r'(.+)\n(.+)\n*(.+)?\n*(.+)?', contact)
		if bits:
			if len(bits[0]) >= 3:
				business['phone'] = bits[0][2]

			if len(bits[0]) >= 4:
				business['fax'] = ''.join(re.findall(r':(.+)', bits[0][3])).strip()

			if len(bits[0]) >= 2:
				business['address'] = '\n'.join(bits[0][0:2])

		business['website'] = self.get_one(hxs, "//tr[@class='cm_noprint']/td[@class='cm_infotext']/a/@href")
		business['categories'] = self.get_one(hxs, "//span[@class='cm_member_categories']/text()")
		return business

	def get_one(self, hxs, selector):
		return '\n'.join(hxs.select(selector).extract()).strip()
