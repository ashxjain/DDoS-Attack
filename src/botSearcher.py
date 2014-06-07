from xml.dom import minidom 
import os
IPList = []
os.system("nmap -sA 10.1.12.0/24 -oX nmapOP.xml") # <--Can change the network in which we are creating bots
xmldoc = minidom.parse('nmapOP.xml')
hosts = xmldoc.getElementsByTagName('host')
for node in hosts:
    filterCheck = node.getElementsByTagName('extraports')
    for eachCheck in filterCheck:
        check =  eachCheck.getAttribute('state')
        if(check == "unfiltered"):
		    Addr = node.getElementsByTagName('address')
		    for ip in Addr:
		    	if(ip.getAttribute('addrtype')=='ipv4'):
		    	    print str(ip.getAttribute('addr'))
		            IPList.append(str(ip.getAttribute('addr')))
g = open("IPList.txt","w")
for i in IPList:
    g.write(i)
    g.write('\n')
g.close()
