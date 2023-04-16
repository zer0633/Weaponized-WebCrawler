import requests
import concurrent.futures
import colorama
from colorama import Fore


colorama.init(autoreset=True)
print(Fore.YELLOW + "-------------------------------------------------------------------------------------------------------------")
""" check for hidden content """
print(Fore.RED + "now starting stage 2, checking for hidden content\n")


filelist = ("/usr/share/SecLists/Discovery/Web-Content/raft-medium-files.txt") # <-- change this if you want to use a different files list 
dirlist = ("/usr/share/SecLists/Discovery/Web-Content/raft-medium-directories.txt") # <-- change this if you wan to use a different directories list
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
            print(f'{target} {r.status_code}')
            f.write(target + "\n")

with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
    executor.map(words_file, files)

print(Fore.YELLOW + "--------------------------------------------------------------------------------")
# Directory brute force
print(Fore.RED + "\nPerforming directory brute force...\n")
def words_dir(word):
        target = ip + "/" + word
        r = requests.get(target)
        with open('directories','a') as f:
                if r.status_code < 400:
                        print(f'{target} {r.status_code}')
                        f.write(target+ "\n")
with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
    executor.map(words_dir, dirs)
