
import json, fileinput

from McAllen.pipelines.website import WebsitePipeline

pipe = WebsitePipeline()

def process(line):
	business = json.loads(line)
	business = pipe.process_item(business, spider=None)
	return json.dumps(business)

for line in fileinput.input(inplace=1):
    print process(line)
