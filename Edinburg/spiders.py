# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

#

from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from scrapy.http import Request

from items import Business

import re

class EdinburgSpider(BaseSpider):
	name = "edinburg"
	allowed_domains = ["edinburg.com"]
	start_urls = ["http://edinburg.com/cgi-bin/members/db.cgi?uid=default&view_records=1&ID=*&nh=1"]

	def parse(self, response):
		hxs = HtmlXPathSelector(response)
		for table in hxs.select("//table[@class='membertable']"):
			business = Business()
			business['name'] = self.get_one(table, ".//span[@class='membertitle']/text()")
			business['phone'] = self.get_one(table, ".//table[@class='membercorner']//td[text()='Phone:']/../td[last()]/text()")
			business['fax'] = self.get_one(table, ".//table[@class='membercorner']//td[text()='Fax:']/../td[last()]/text()")
			business['address'] = self.get_one(table, ".//span[@class='memberdetail']/text()")
			business['email'] = ''.join(re.findall(r':(.+)', self.get_one(table, ".//table[@class='membercorner']//td[@class='memberdetail'][@colspan='2']//a[text()='Email']/@href"))).strip()
			business['website'] = self.get_one(table, ".//table[@class='membercorner']//td[@class='memberdetail'][@colspan='2']//a[text()='Website']/@href")
			business['categories'] = [self.get_one(table, ".//td[@class='memberdetail'][@colspan='2']/text()")]
			yield business

		urls = hxs.select("//a[text()='[>>]']/@href").extract()
		if urls:
			yield Request(urls[0], callback=self.parse)

	def get_one(self, context, selector):
		return '\n'.join(context.select(selector).extract()).strip()
