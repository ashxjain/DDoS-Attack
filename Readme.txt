												  Distributed Denial of Service
												 Computer Network Security-CS366
														Project Report 

--------+
﻿Overview|
--------+

A Denial of Service (DoS) attack is an attack with the purpose of preventing legitimate users from using a specified network resource such as a website, web service, or computer system. A Distributed Denial of Service (DDoS) attack is a coordinated attack on the availability of services of a given target system or network that is launched indirectly through many compromised computing systems. The services under attack are those of the primary victim, while the compromised systems used to launch the attack are often called the secondary victims/bots. 
Following diagram shows a basic infrastructure of a DDoS attack network:

									Command & Control Center
							                   |        
	             __________________________________________________________
				|               |                        |                 |
		Bot(Infected Host)  Bot(Infected Host)  Bot(Infected Host)  Bot(Infected Host)
				|               |                        |                 |
	             __________________________________________________________
                                               |
									Victim (Attacked Target) 

Two types of DDoS attack networks have emerged: the Agent-Handler model and the Internet Relay Chat (IRC)-based model.
The Agent-Handler model of a DDoS attack consists of clients, handlers, and agents. The client is where the attacker communicates with the
rest of the DDoS attack system. The handlers are software packages located throughout the Internet that the attacker’s client uses to communicate with the agents. The agent software exists in compromised systems that will eventually carry out the attack. The attacker communicates with any number of handlers to identify which agents are up and running, when to schedule attacks, or when to upgrade agents. 

The IRC-based DDoS attack architecture is similar to the Agent-Handler model except that instead of using a handler program installed on a network server, an IRC (Internet Relay Chat) communication channel is used to connect the client to the agents.

We are using the Agent-Handler model, where 
	* Client software used to communicate with the bots/agents - ssh, botMaker.c
	* Agent Searching is done using - botSearcher.py
	* Handler installed in compromised system - ssh
	* Agent software performing attack - TCPSyn.py, TCPpsh+ack.py, udpflood.py

There are two main classes of DDoS attacks : bandwidth depletion and resource depletion attacks. 
	* A bandwidth depletion attack is designed to flood the victim network with unwanted traffic that prevents legitimate traffic from reaching the primary victim. 
		- In our project we will be demonstrating a UDP Flood Attack:
			+ In a UDP Flood attack, a large number of UDP packets are sent to either random or specified ports on the victim system. The victim system tries to process the incoming data to determine which applications have requested data. If the victim system is not running any applications on the targeted port, it will send out an ICMP packet to the sending system indicating a "destination port unreachable" message

	* A resource depletion attack is an attack that is designed to tie up the resources of a victim system making the victim unable to process legitimate requests for service.
		- Protocol Exploit Attacks: We give two examples, one misusing the TCP SYN (Transfer Control Protocol Synchronize) protocol, and the other misusing the PUSH+ACK protocol.
			+ In a DDoS TCP SYN attack, the attacker instructs the bots to send bogus TCP SYN requests to a victim server in order to tie up the server’s processor resources, and hence prevent the server from responding to legitimate requests. The TCP SYN attack exploits the three-way handshake between the sending system and the receiving system by sending large volumes of TCP SYN packets to the victim system with spoofed source IP addresses, so the victim system responds to a non-requesting system with the ACK+SYN. When a large volume of SYN requests are being processed by a server and none of the ACK+SYN responses are returned, the server eventually runs out of processor and memory resources, and is unable to respond to legitimate users.
			+ In a PUSH + ACK attack, the attacking agents send TCP packets with the PUSH and ACK bits set to one. These triggers in the TCP packet header instruct the victim system to unload all data in the TCP buffer (regardless of whether or not the buffer is full) and send an acknowledgement when complete. If this process is repeated with multiple agents, the receiving system cannot process the large volume of incoming packets and the victim system will crash.

Because of time constraints, we have skipped the process of getting the password of the compromised systems, hence we assume that we have the username and password of the bots in the network and we also assume that all/most of the systems have same username and password.


-------------+
Prerequisites|
-------------+

        Command and Control Center:
        ++++++++++++++++++++++++++
			- Softwares to be installed 
				* nmap - sudo apt-get install nmap
				* sshpass - sudo apt-get install sshpass
				* hping3 - sudo apt-get install hping3
						                                                            
		Bots:
		++++
			* ssh enabled hosts, present in the same network
			* Host must be that system’s administrator 
				
		Victim:
		++++++ 
			* Web-site hosted on victim’s computer to test DDoS attack. We have included a web-site in the folder named: "Website"
			* This web-site can be used to test the attack. For our test, we used nginx web-server.


--------------------+
Summary of Resources|
--------------------+
	[1] Distributed Denial of Service: Taxonomies of Attacks, Tools and Countermeasures: Stephen M. Specht, Ruby B. Lee
		- To understand the basic terminologies and various forms of DDOS attacks
	[2] DDoS Survival handbook, Radware, 2013
		- To understand various mitigation techniques for DDoS
	[3] SAANS Institute Misc Tools Cheat Sheet
		- To understand the working of hping3 tool
	[4] http://resources.infosecinstitute.com/dos-attacks-free-dos-attacking-tools/
		- About DOS attacking tools


------------------------+
Implemented Case studies|
------------------------+

	Resource Depletion attacks:
	+++++++++++++++++++++++++++        
		1. TCP SYN flooding attack:
		===========================	
			$sudo python botSearcher.py
			----------------------------
				* This code will look for IP addresses in the local network using nmap tool. To change the network address, edit line 4 of this program.
				* This tool will save the results in "nmapOP.xml" file. 
				* "botSearcher.py" will then parse this xml file and looks for systems which are up and whose ports are unfiltered and store the IP address of those systems in "IPList.txt" file.
		
			$gcc -pthread botMaker.c
			-------------------------
		
			$./a.out
			--------		
				* "botMaker.c" will take the username and password of the bots and will also take the input as name of the python code for implementing this attack. In this case filename is "TCPSyn.py". This attack will be for 60 seconds. This time value can be changed by changing the value on line 104 in TCPSyn.py file.
				* To change the victim's IP address edit line 36 of "TCPSyn.py". 
				* To spoof the source IP address edit line 35 of "TCPSyn.py" 
		
			Output:
			-------
				* On terminal, login screen of connected hosts will appear. Error messages from unsuccessful connection to hosts will also appear. After the attack, "success" message will be displayed from the all the hosts.
				* Can also run wireshark on the victim system to see the packets.
				* Can use any browser to load the webpage hosted on victim's system, if attack is successful, the page will take more time to load.	  
				* Can ping to the victim and see the time difference after the attack


		2. TCP PSH+ACK flooding attack:
		==============================        
		    $sudo python botSearcher.py
		    ---------------------------
		        * This code will look for IP addresses in the local network using nmap tool.
		 		* This tool will save the results in "nmapOP.xml" file. 
		        * "botSearcher.py" will then parse this xml file and looks for systems which are up and whose ports are unfiltered and store the IP address of those systems in "IPList.txt" file.
		    
		    $gcc -pthread botMaker.c
		    ------------------------
		    
		    $./a.out
		    --------
		        * "botMaker.c" will take the username and password of the bots and will also take the input as name of the python code for implementing this attack. In this case filename is "TCPpsh+ack.py". This attack will be for 60 seconds. This time value can be changed by changing the value on line 104 in TCPpsh+ack.py file.
				* To change the victim's IP address edit line 36 of "TCPpsh+ack.py". 
				* To spoof the source IP address edit line 35 of "TCPpsh+ack.py".
		
			Output:
			-------
				* On terminal, login screen of connected hosts will appear. Error messages from unsuccessful connection to hosts will also appear. After the attack, "success" message will be displayed from the all the hosts.
				* Can also run wireshark on the victim system to see the packets.
				* Can use any browser to load the webpage hosted on victim's system, if attack is successful, the page will take more time to load.	  
				* Can ping to the victim and see the time difference after the attack


	Bandwidth Depletion attack:
	+++++++++++++++++++++++++++
		    UDP flooding attack:
		    ===================
		    $sudo python botSearcher.py
		    ---------------------------
		         * This code will look for IP addresses in the local network using nmap tool.
		 		 * This tool will save the results in "nmapOP.xml" file. 
		         * "botSearcher.py" will then parse this xml file and looks for systems which are up and whose ports are unfiltered and store the IP address of those systems in "IPList.txt" file.
		         
		    $gcc -pthread botMaker.c
		    --------------------------------
		    
		    $./a.out
		    --------
		          * "botMakerUDPFlood.c" will take the username and password of the bots and will also take the input as name of the python code for implementing this attack. In this case filename is "udpflood.py". This attack will be for 60 seconds. This time value can be by changing the value on line 14 in udpflood.py file.
				* To change the victim's IP address edit line 6 of "udpflood.py". 
				* To change the packet size edit line 5 of "udpflood.py".
		
			Output:
			-------
				* On terminal, login screen of connected hosts will appear. Error messages from unsuccessful connection to hosts will also appear. After the attack, "success" message will be displayed from the all the hosts.
				* Can also run wireshark on the victim system to see the packets.
				* Can use any browser to load the webpage hosted on victim's system, if attack is successful, the page will take more time to load.	  
				* Can ping to the victim and see the time difference after the attack


--------------------------+
Take away from the project|
--------------------------+
	DoS/DDoS attacks are the weapon of choice for cyber-hacktivist groups and are increasing in severity and complexity. This project, for demonstrating DDOS has helped us understand various attacks that takes place in real life. We've also learned that once a single system is compromised, one can easily launch an attack on the network. 


-------------------+
Future Enhancements|
-------------------+

	1) Add more attacks:
		* Smurf attack
		* TCP URG attack
		* Attack in application layer/non-network based attack
	2) Consider configuring web-server to make/prevent attack
	3) Accounting for bandwidth depletion attack 
		* Use ifconfig for accounting the number of packets sent 
		* Must use router for this attack
		* Must divide packet size according to the number of bots
	4) Accounting for TCP SYN and PSH+ACK 
		* Use tcpdump, tdump

---------------+
Acknowledgement|
---------------+
We worked on this project under the guidance of Dr. Ram Prakash Rustagi, his wisdom and experience has enabled us to conduct the project work successfully. We express our sincere thanks to him. 
