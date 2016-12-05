from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.item import Item, Field


class CatalogItem(Item):
	id          = Field()
	detail      = Field()
	name			  = Field()
	lastUpdated = Field()
	dataType    = Field()
	dataSrc     = Field()
	dataLayout  = Field()
	keywords    = Field()


import re

class TexasTransparencySpider(BaseSpider):
	name = "texastransparency"
	allowed_domains = ["texastransparency.org/"]
	start_urls = ["http://www.texastransparency.org/opendata/catalog.php"]

	def parse(self, response):
		hxs = HtmlXPathSelector(response)
		for table in hxs.select("//table[@id='resultTable']/tbody/tr"):
			business = CatalogItem()
			business['detail'] = self.get_one(table, ".//div[@class='dataCellName']//a[@href]")
			business['name'] = self.get_one(table, ".//div[@class='dataCellName']//a/text()")
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
