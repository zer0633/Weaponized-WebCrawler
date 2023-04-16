import requests
import concurrent.futures
import colorama
from colorama import Fore


colorama.init(autoreset=True)
print(Fore.BLUE + "-------------------------------------------------------------------------------------------------------------")
""" check for hidden content """

dirlist = ("/usr/share/SecLists/Discovery/Web-Content/raft-small-directories.txt")

with open(dirlist) as f:
    dirs = [word.strip() for word in f]
    f.close()


print(Fore.RED + "\nPerforming directory brute force...\n")
def words_dir(word):
	with open('directories','r')as  dir:
		for d in dir:
			target = d.strip()+'/'+word
			with open('secondary_dirs','a')as sd:
				if r.status_code < 400:
					print(f'{r.status_code} {target}')
					sd.write(target + "\n")



with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
    executor.map(words_dir, dirs)
