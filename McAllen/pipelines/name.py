from scrapy.exceptions import DropItem
import re

class NamePipeline(object):

	def process_item(self, item, spider):
		if item['name']:
			item['name'] = item['name'].title()
		else:
			raise DropItem("Missing name in %s" % item)

		return item
