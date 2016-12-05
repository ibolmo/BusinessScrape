import re

class PhoneFaxPipeline(object):

	def process_item(self, item, spider):
		if item['phone']:
			digits = re.sub(r'[^0-9x]', '', item['phone'])
			if len(item['phone']) == 10:
				item['phone'] = '-'.join([digits[0:3], digits[3:6], digits[6:10]])

		return item

