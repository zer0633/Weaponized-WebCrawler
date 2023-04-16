""" 
creator: The_Architect

last updated: 04/09/23

-----------------------------------------------------------------------------------------------------------------------------------------------------------
main notes:                                                                                                                                               |
This is to be used to map the entire web application for possible vulnerabilities it uses the requests library to gather information about the target     |
the main program checks for various things such as hrefs,headers,url parameters,web application language, comments,robots and sitemap urls,               |
hidden form fields and  preforms a file and directory brute force. if you want to run only the main program remove everything after the line of #         |
-----------------------------------------------------------------------------------------------------------------------------------------------------------"""
""" -------------------------------------------------------------------------------------------------------------------------------------------------------
sub notes 1: there are 2 sub processes in this script the first re-runs all the above scripts on the found directories under the name contin              |
sub notes 2: the final portion of this script runs various other modules in an attempt to find possible vulnerabilities which include                     |
LOCAL FILE INCLUSION, LOG POISONING, UNION BASED SQL INJECTION, OS COMMAND INJECTION, FILE UPLOADABILITY, AND RERUNS BRUTEFORCE FOR SECONDARY DIRECTORIES |
-----------------------------------------------------------------------------------------------------------------------------------------------------------"""

import os
import re
import requests
import concurrent.futures
import colorama
from colorama import Fore
colorama.init(autoreset=True)


ip = input("please supply the webpage url, eg  http://localhost ")
os.mkdir(ip+"_Website")
os.chdir(ip+"_Website")
if "http://" not in ip:
	ip = "http://"+ip

	print(Fore.BLUE + "---------------------------------------------------------------------------------------------------------\n\n")
	print(Fore.RED + """

╦ ╦  ╔═╗  ╔═╗  ╔═╗  ╔═╗  ╔╗╔  ╦  ╔═╗  ╔═╗  ╔╦╗
║║║  ║╣   ╠═╣  ╠═╝  ║ ║  ║║║  ║  ╔═╝  ║╣    ║║
╚╩╝  ╚═╝  ╩ ╩  ╩    ╚═╝  ╝╚╝  ╩  ╚═╝  ╚═╝  ═╩╝

╦ ╦╔═╗╔╗   ╔═╗╦═╗╔═╗╦ ╦╦  ╔═╗╦═╗
║║║║╣ ╠╩╗  ║  ╠╦╝╠═╣║║║║  ║╣ ╠╦╝
╚╩╝╚═╝╚═╝  ╚═╝╩╚═╩ ╩╚╩╝╩═╝╚═╝╩╚═

""")
	print(Fore.BLUE + "---------------------------------------------------------------------------------------------------------\n\n")
def hrefs():
	print(Fore.RED + "\nStarting stage 1, gathering Key Information about the application...\n")
	""" Enumerating Content and Functionality """
	#use a get request on the initial webpage, then parse the source for all hrefs
	print(Fore.RED + "Gathering all hrefs to look into on base url\n")
	r = requests.get(ip)
	r = r.text
	result = re.findall(r'href="([^"]*)"',r)
	with open('all_hrefs','w')as f:
		for href in result:
			f.write(href+"\n")
			print("found "+href)
	f.close()
hrefs()

def url_hrefs():
	print(Fore.BLUE + "------------------------------------------------------------------------------------------------------------\n")
	#now only find hrefs with different urls
	print(Fore.RED + "Gathering all hrefs with different urls in base source\n")
	r = requests.get(ip)
	r = r.text
	result = re.findall(r'http\S+',r)
	with open('http_urls','w')as f:
        	for ht in result:
                	f.write(ht+"\n")
	                print("found "+ht)
	f.close()
url_hrefs()

def headers():
	print(Fore.BLUE + "------------------------------------------------------------------------------------------------------------")
	#gather http headers
	print(Fore.RED + "\ngathering http headers\n")
	r = requests.get(ip)
	with open('headers','w')as head:
		for header in r.headers:
			head.write(header + ': '+r.headers[header]+'\n')
	head.close()
	with open('headers','r')as head:
		head = head.readlines()
		for x in head:
			print(x)
headers()

def comments():
	print(Fore.BLUE + "------------------------------------------------------------------------------------------------------------")
	#find comments maybe something juicy in their $$?
	print(Fore.RED + "\nattempting to find any comments\n")
	r = requests.get(ip)
	r = r.text
	result = re.findall(r"<!--(.*?)-->",r)
	with open('comments','w')as f:
        	for comm in result:
                	f.write(comm+"\n")
	                print("found "+comm)
	f.close()
comments()

def file_extentions():
	print(Fore.BLUE + "------------------------------------------------------------------------------------------------------------")

	#check for file extentions type to determine plateform programming language
	print(Fore.RED + '\nchecking what programming language is being used on the site\n')
	ext = ['asp','aspx','jsp','cfm','php','d2w','pl','dll','nfs','ntf']
	r = requests.get(ip)
	r = r.text
	for x in ext:
		if x in r:
			print('found extention '+x)
file_extentions()

def robots():
	print(Fore.BLUE + "------------------------------------------------------------------------------------------------------------")
	#check for robots.txt and sitemap.xml
	print(Fore.RED + "\nchecking for robots.txt file")
	r = requests.get(ip+"/robots.txt")
	if r.status_code == 200:
		print("robots.txt present, outputing to a file")
		with open('robots.txt','w')as f:
			f.write(r.text)
		f.close()
		r = requests.get(ip+"/robots.txt")
		if r.status_code == 200:
			with open('robots.txt','r')as f:
				f = f.readlines()
				for rob in f:
					print(rob)
robots()
def sitemap():

	print(Fore.BLUE + "-------------------------------------------------------------------------------------------------------------")
	print(Fore.RED + "\nchecking for sitemap.xml file")
	r = requests.get(ip+"/sitemap.xml")
	if r.status_code == 200:
		print("sitemap.xml present, outputing to a file")
		with open('sitemap.xml','w')as f:
			f.write(r.text)
		f.close()
		r = requests.get(ip+"/sitemap.xml")
		if r.status_code == 200:
			with open('sitemap.xml','r')as f:
				f = f.readlines()
				for site in f:
					print(site)



sitemap()
print(Fore.BLUE + "-------------------------------------------------------------------------------------------------------------")
""" check for hidden content """
print(Fore.RED + "now starting stage 2, checking for hidden content\n")


filelist = ("/usr/share/SecLists/Discovery/Web-Content/raft-medium-files.txt") # <-- change this to a files list you want to use
dirlist = ("/usr/share/SecLists/Discovery/Web-Content/raft-medium-directories.txt") # change this to a directories list you want to use
# Open wordlists and turn them into lists
with open(filelist) as f:
    files = [word.strip() for word in f]
    f.close()
with open(dirlist) as f:
    dirs = [word.strip() for word in f]
    f.close()

# File brute force
print(Fore.RED + "\nPerforming file brute force...\n")
def words_file(word):
    target = ip + "/" + word
    r = requests.get(target)
    with open("files",'a') as f:
        if r.status_code < 400:
            print(f'{r.status_code} {target}')
            f.write(target + "\n")

with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
    executor.map(words_file, files)

print(Fore.BLUE + "--------------------------------------------------------------------------------")
# Directory brute force
print(Fore.RED + "\nPerforming directory brute force...\n")
def words_dir(word):
        target = ip + "/" + word
        r = requests.get(target)
        with open('directories','a') as f:
                if r.status_code < 400:
                        print(f'{r.status_code} {target}')
                        f.write(target+ "\n")
with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
    executor.map(words_dir, dirs)


def hidden_param():
	print(Fore.BLUE + "--------------------------------------------------------------------------------")
	""" Discover hidden parameters """
	print(Fore.RED + "\n attempting to discover hidden parameters through the source code \nnote: sometimes the webpage will hide it and you will need to manually check")
	lyst=["?secrettier360=","?plot=","?cat=","?dir=","?action=","?board=","?date=","?detail=","?file=","?download=","?path=","?folder=","?prefix=","?include=","?page=","?inc=","?locate=","?show=","?doc=","?site=","?type=","?view=","?content=","?document=","?layout=","?mod=","?conf="]

	with open("files",'r')as f:
		with open('lfi-test_urls','a')as lfi:
			for url in f: 
				f = url.strip() 
				r = requests.get(f) 
				r = r.content 
				r = str(r) 
				for x in lyst:
					if x in r:
						print("found parameter "+f+x)
						lfi.write(f+x)

print(Fore.BLUE + "---------------------------------------------------------------------------------------------------------\n\n")
hidden_param()

def hidden():
	print('checking for hidden form fields')
	import hidden
print(Fore.BLUE + "---------------------------------------------------------------------------------------------------------\n\n")
hidden()

print(Fore.BLUE + "--------------------------------------------------------------------------------")
print(Fore.GREEN +"Inital Enumeration of the webpage Completed")
print(Fore.BLUE + "--------------------------------------------------------------------------------")

###########################################################################################################################################################
contin = input("Would you like to do more targeted checks (y/n)")

if contin == 'y':
	uri = os.getcwd()
	"""ask if you want to run the above commands again on each directory we found"""
	con = input("would you like to run the tests again on all directories we found? (y/n)")
	if con == 'y':
		print('starting the enumeration of all directories we found...')
		"""create a base directory and then create a new directory using the last param in the directory name"""
		with open('directories','r')as dir:
			os.mkdir("Directories")
			os.chdir("Directories")
			for x in dir:
				url = x.strip().split('/')
				url = url[3]
				if not url:
					continue
				os.mkdir(url)
				os.chdir(url)
				ip = x
				ip = ip.strip()
				print("now checking "+ip)
				hrefs()
				url_hrefs()
				headers()
				robots()
				sitemap() 
				comments()
				file_extentions()
				hidden()
				os.chdir('..')
	else:
		print('not performing further enumeration on found dirrectories')


##########################################################################################################################################################
	"""everything under this section conducts various tests using seperate modules this can either be removed or commented out if not needed otherwise
	it will ask to do other tests such as lfi log poisoning and sql injections"""

	os.chdir(uri)
	upload = input("would you like to check for upload capabilities on the directories we found?(y/n)\n")
	if upload == 'y':
		import uploads
	elif upload == 'n':
		print('not checking for upload capabilities')




	"""ask user if they want to test for sql injections"""
	sql = input("would you like to test for possible sql injections? y for yes n for no.\n")
	if  sql == 'y':
		print('starting to test files we found for sql injections')
		import sql_injection

	elif sql == 'n':
		print('not performing sql injection test')




	lfi = input("would you like to check for local file inclusion on the paramter we found? (y/n)\n")
	if lfi == 'y':
		print("starting local file inclusion tests")
		import LFI
	elif lfi == 'n':
		print("not preforming local file inclusion tests")
		pass


	poison = input("would you like to attempt log poisoning? (y/n)\n")
	if poison == 'y':
		print('attempting to poison logs')
		import logpoison
	elif poison == 'n':
		print('not preforming log poisoning attmept')
		pass


	oscommand = input("would you like to check for os command injection within the url params we found?(y/n)")
	if oscommand == 'y':
		import osInjection
	elif oscommand == 'n':
		print('not checking for command injection')


	brute = input("would you like to preform directory bruteforce again on the found direcories? (y/n)")
	if brute == 'y':
		import Continue
	elif brute == 'n':
		print('not preforming more bruteforceing on found directories')



