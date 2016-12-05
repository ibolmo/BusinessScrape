# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class Business(Item):
	id         = Field()
	name       = Field()
	contact    = Field()
	phone      = Field()
	fax        = Field()
	address    = Field()
	email      = Field()
	website    = Field()
	categories = Field()

class CatalogItem(Item):
	id          = Field()
	detail      = Field()
	name			  = Field()
	lastUpdated = Field()
	dataType    = Field()
	dataSrc     = Field()
	dataLayout  = Field()
	keywords    = Field()
