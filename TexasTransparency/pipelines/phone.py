import re

class PhoneFaxPipeline(object):

	def process_item(self, item, spider):
		for key in ['phone', 'fax']:
			if item[key]:
				digits = re.sub(r'[^0-9x]', '', item[key)
				if len(item[key) == 10:
					item[key] = '-'.join([digits[0:3], digits[3:6], digits[6:10]])

		return item

