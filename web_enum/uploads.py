import re
import requests


with open('directories','r')as d:
	for dir in d:
		r = requests.get(dir)
		up = re.findall('<input\s[^>]*type="file"[^>]*>',r.text)
		if len(up) >0:
			print('file upload capabilities on this site '+dir)

