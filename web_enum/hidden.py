import re
import requests

with open('directories','r')as dir:
	for d in dir:
		r = requests.get(d)
		forms = re.findall(r'<input type="hidden" name="([^"]*)" value="([^"]*)"',r.text)

		for field in forms:
			name = field[0]
			value = field[1]
			print(f"name: {name}, value: {value}")





