import os
import datetime
import time
import schedule


#CLIENT TRAFFIC GENERATION SCRIPT

"""
Host Requirements:
- Linux-based host
- Python3 / curl / wget
- 'Schedule' Python Library - pip install schedule

Security Policy Tests
- URL Filtering
- IPS Traffic Test
- AMP File Download Test

How to Use:
- Update the Traffic Dictionaries (& time intervals if necessary)
- Make the file executable - sudo chmod 755 tgen.py
- Run using python3 tgen.py 
"""

#Traffic Dictionaries
wget_traffic = { #links for URL filtering
					"Zoom":"https://www.zoom.us/",
					"Cisco":"https://www.cisco.com/",
					"Microsoft Teams":"https://teams.microsoft.com/",
					"Webex":"https://www.webex.com/",
					"Box":"https://www.box.com/"
				}

ips_traffic = [ #user-agent argument for curl command
					"ZEPPELIN",
					"spam_bot",
					"GetRight",
					"\"() {:;}; /bin/cat /etc/passwd\"",
                    "\"-H 'range: bytes=0-18446744073709551615'\""
				]

malware_traffic = { #Malicious File download URLs for curl command
					"Eicar file":"https://secure.eicar.org/eicar.com.txt",
					"africau PDF":"http://www.africau.edu/images/default/sample.pdf",
					"W3 PDF":"https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"
				}


def startTraffic():
    t = time.localtime()
    current_time = time.strftime("%I:%M:%S%p", t)
    current_hour = time.strftime("%H", t)
    
    print("\n\nGenerating user A traffic pattern until 5PM local time. . .\n")
    print("\n*** START TIME: {} ***\n\n".format(current_time))

    #Count the number of entries in each dictionary
    wget_dict = len(wget_traffic)
    ips_dict = len(ips_traffic)
    malware_dict = len(malware_traffic)

    #Generate Traffic 
    i = 0 #cycle counter - 1 cycle / second
    j = 0 #normal hit counter @ 1 hit/second
    k = 0 #IPS hit counter @ 1/13  hit/second
    m = 0 #malware hit counter @ 1/17 hit/second
    while True:
        t = time.localtime()
        current_time = time.strftime("%I:%M:%S %p", t)
        
        #Normal Traffic Hit
        if (i % 1 == 0):
            current = list(wget_traffic.items())[j]
            os.system('wget --user-agent="Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0" -q --delete-after {}'.format(current[1]))
            print("{} - WGET attempt to {}.".format(current_time, current[0]))
            if j == wget_dict - 1: #Reset index at the end of the list
                j = 0
            else:
                j += 1 
        
        #IPS Signature Hit Attempt
        if (i % 13 == 0):
            current = ips_traffic[k]
            os.system('sudo curl -4 -v -L -k -o /dev/null --connect-timeout 3 https://bing.com --user-agent {}'.format(current))
            print("{} - IPS Hit attempt with user-agent {}".format(current_time, current))
            if k == ips_dict - 1: #Reset index at the end of the list
                k = 0
            else:
                k += 1        
        
        #Malware File Download Attempt
        if (i % 17 == 0):
            current = list(malware_traffic.items())[m]
            os.system('sudo curl -4 -v -L -k -o /dev/null --connect-timeout 3 {}'.format(current[1]))
            print("{} - Malware download attempt from {}".format(current_time, current[1]))
            if m == malware_dict - 1: #Reset index at the end of the list
                m = 0
            else:
                m += 1
        
        i += 1 # one hit cycle completed
        
        #At 5PM, break the loop and return to wait for next scheduled run
        t = time.localtime()
        current_hour = time.strftime("%H", t)
        print(current_hour)
        if current_hour == "17":
            break
        else:
            time.sleep(1)


#RUN SCHEDULE: Every Weekday at 8 AM
schedule.every().monday.at("08:00").do(startTraffic)
schedule.every().tuesday.at("08:00").do(startTraffic)
schedule.every().wednesday.at("08:00").do(startTraffic)
schedule.every().thursday.at("08:00").do(startTraffic)
schedule.every().friday.at("08:00").do(startTraffic)

while True:
    #Display Program Run Start Time:
    t = time.localtime()
    current_time = time.strftime("%I:%M:%S%p", t)
    print("\n*** THE CURRENT TIME IS  {} ***\n".format(current_time))
    startTraffic()
    schedule.run_pending()
    time.sleep(30)