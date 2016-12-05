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

class McAllenSpider(CrawlSpider):
	name = "mcallen"
	allowed_domains = ["mcallen.org"]
	start_urls = ["http://www.mcallen.org/Members/Business-Type"]

	rules = (
		Rule(SgmlLinkExtractor(allow=('Members\/[0-9]+')), callback='parse_item'),
	)

	def parse_item(self, response):
		hxs = HtmlXPathSelector(response)
		business = Business()
		business['id'] = ''.join(re.findall(r"\/(\d+)", response.url)).strip()
		business['name'] = self.get_one(hxs, "//div[@id='content']//td[@colspan=2]/b/text()")
		business['contact'] = self.get_one(hxs, "//div[@id='content']//td//b[text()='Contact Person:']/../../td[last()]/text()")
		business['phone'] = re.sub(r'\(\)', '', self.get_one(hxs, "//div[@id='content']//td//b[text()='Phone Number:']/../../td[last()]/text()"))
		business['fax'] = re.sub(r'\(\)', '', self.get_one(hxs, "//div[@id='content']//td//b[text()='Fax:']/../../td[last()]/text()"))
		business['address'] = self.get_one(hxs, "//div[@id='content']//td//b[text()='Address:']/../../td[last()]/text()")
		business['email'] = self.get_one(hxs, "//div[@id='content']//td//b[text()='Email Address:']/../../td[last()]/text()")
		business['website'] = self.get_one(hxs, "//div[@id='content']//td//b[text()='Website:']/../../td[last()]//a/@href")
		business['categories'] = self.get_one(hxs, "//div[@id='content']//td//b[text()='Categories:']/../../td[last()]/text()")
		if len(business['categories']):
			business['categories'] = [re.sub(r"^ *\d+\. *", "", cat) for cat in business['categories'].split('\n')]
		return business

	def get_one(self, hxs, selector):
		return '\n'.join(hxs.select(selector).extract()).strip()
