import time
import argparse
from datetime import datetime as dt
from sys import platform
 
hosts_temp = "hosts"
hosts_path = "/etc/hosts"
if platform == "win32":
    hosts_path = r"C:\Windows\System32\drivers\etc"

redirect = "127.0.0.1"
website_list = ["www.facebook.com","facebook.com","instagram.com","www.instagram.com"]
website_list_file = "blocked_sites"

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--start", help = "working hours start time. Default is 9", default = 9, type = int, nargs = '?')
parser.add_argument("-e", "--end", help = "woring hours end time. Default is 17", default = 17, type = int, nargs = '?')
parser.add_argument("-w", "--site", help = "website to be blocked", type = str, default = [], nargs = '*', action = 'append')
parser.add_argument("-t", "--test", help = "use temporary hosts file for tesing. Add -t flag", default = False, type = bool, nargs = '?', metavar = '')
args = parser.parse_args()

if args.site != []:
    for site in args.site:
        website_list.append(site[0])

if args.test is not False:
    hosts_path = hosts_temp

now = dt.now()
while True:
    if dt(now.year, now.month, now.day, args.start) < now < dt(now.year, now.month, now.day, args.end):
        print("Working hours from %s to %s..." % (args.start, args.end))
        with open(hosts_path, 'r+') as file:
            content=file.read()
            for website in website_list:
                if website in content:
                    pass
                else:
                    file.write(redirect+" "+ website+"\n")
        with open(website_list_file, "w") as file:
            for site in website_list:
                file.write(site + "\n")
        print("Websites being blocked: %s" % website_list)
    else:
        with open(website_list_file, 'r+') as file:
            website_list = file.readlines()
            file.seek(0)
            file.truncate()
        with open(hosts_path, 'r+') as file:
            content=file.readlines()
            file.seek(0)
            for line in content:
                if not any(website in line for website in website_list):
                    file.write(line)
            file.truncate()
        print("Fun hours from %s to %s..." % (args.end, args.start))
    time.sleep(10)