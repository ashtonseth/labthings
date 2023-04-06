import os
import datetime
import time
import schedule

#CLIENT TRAFFIC GENERATION SCRIPT

"""
Host Requirements:
- Linux-based host
- Python3 / curl / wget
- 'schedule' Python Library - 'pip install schedule'

Security Policy Tests
- URL Filtering
- IPS Traffic Test
- AMP File Download Test

How to Use:
- Update the Traffic Dictionaries (& time intervals if necessary)
- Make the file executable - 'sudo chmod 755 tgen.py'
- Run using 'python3 tgen.py' (schedule runs every weekday 8-5pm local time, update as necessary)
"""

#Traffic Dictionaries
wget_traffic = { #URL filtering test URLs
					"Zoom":"https://www.zoom.us/",
					"Cisco":"https://www.cisco.com/",
                    			"Twitter":"https://www.twitter.com/", #SOCIAL MEDIA
					"Microsoft Teams":"https://teams.microsoft.com/",
					"Webex":"https://www.webex.com/",
					"Box":"https://www.box.com/",
					"Facebook":"https://www.facebook.com/", #SOCIAL MEDIA 
					"888 Gambling":"https://www.888.com/",
					"Sephora":"https://www.sephora.com/", #BEAUTY & MAKEUP
                			"Youtube":"https://www.youtube.com" #STREAMING - YOUTUBE
				}

ips_traffic = [ #IPS Traffic test user-agent argument for curl command
					"ZEPPELIN",
					"spam_bot",
					"GetRight",
					"\"() {:;}; /bin/cat /etc/passwd\"",
                   			 "\"-H 'range: bytes=0-18446744073709551615'\""
				]

malware_traffic = { #AMP test malicious file download / ZBFW Access URLs for curl command
					"Eicar file":"https://secure.eicar.org/eicar.com.txt",
					"africau PDF":"http://www.africau.edu/images/default/sample.pdf",
                    			"C&C 10.101.150.40:8001":"http://10.101.150.40:8001", #ZBFW RULE
					"W3 PDF":"https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"
				}


def startTraffic():
    t = time.localtime()
    current_time = time.strftime("%I:%M:%S%p", t)
    current_hour = time.strftime("%H", t)
    
    print("\n\nGenerating user A traffic pattern until 5PM local time. . .\n")
    print("\n*** START TIME: {} ***\n\n".format(current_time))
    time.sleep(3)

    #Count the number of entries in each dictionary
    wget_dict = len(wget_traffic)
    ips_dict = len(ips_traffic)
    malware_dict = len(malware_traffic)

    #Hit Counters
    c = 0 #cycle counter - 1 cycle / second
    n = 0 #normal hit counter @ 1 hit/cycle
    i = 0 #IPS hit counter @ 1/13  hit/cycle
    m = 0 #malware hit counter @ 1/17 hit/cycle
    
    #Generate Traffic 
    while True:
        t = time.localtime()
        current_time = time.strftime("%I:%M:%S %p", t)
        
        #Normal Traffic Hit
        if (c % 1 == 0):
            current = list(wget_traffic.items())[j]
            os.system('wget --user-agent="Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0" -q --delete-after {}'.format(current[1]))
            print("{} - WGET attempt to {}.".format(current_time, current[0]))
            if n == wget_dict - 1: #Reset index at the end of the list
                n = 0
            else:
                n += 1 
        
        #IPS Signature Hit Attempt
        if (c % 13 == 0):
            current = ips_traffic[k]
            os.system('sudo curl -4 -v -L -k -o /dev/null --connect-timeout 3 https://bing.com --user-agent {}'.format(current))
            print("{} - IPS Hit attempt with user-agent {}".format(current_time, current))
            if i == ips_dict - 1: #Reset index at the end of the list
                i = 0
            else:
                i += 1        
        
        #Malware File Download Attempt
        if (c % 17 == 0):
            current = list(malware_traffic.items())[m]
            os.system('sudo curl -4 -v -L -k -o /dev/null --connect-timeout 3 {}'.format(current[1]))
            print("{} - Malware download attempt from {}".format(current_time, current[1]))
            if m == malware_dict - 1: #Reset index at the end of the list
                m = 0
            else:
                m += 1
        
        c += 1 # one hit cycle completed
        
        #break the loop at 5pm and return to wait
        t = time.localtime()
        current_hour = time.strftime("%H", t)
        if current_hour >= "17":
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
    schedule.run_pending() #wait for next scheduled run
