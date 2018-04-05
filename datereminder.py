#!/usr/bin/python
import yaml
import requests
import requests
import csv
import sys
from datetime import datetime, timedelta

config_file = "../datereminder-config.yaml"

mmdd = datetime.now().strftime("%m-%d")
yyyy = datetime.now().strftime("%Y")
yyyymmdd = date = datetime.now().strftime("%Y-%m-%d")
todayObj = datetime.strptime(yyyymmdd, "%Y-%m-%d")

try:
    config = yaml.safe_load(open(config_file))
except:
    print "Unable to read config file."
    sys.exit(0)

csv_r = requests.get(config['downloadurl'])
if csv_r.status_code != 200:
    print "Unable fo fetch spreadsheet. Not a 200 status code."
    sys.exit(0)

ss = list(csv.reader(csv_r.text.split('\n')))
header = ss[0]
headerN = {}
for cellN in range(0,len(header)):
    headerN[header[cellN].lower()] = cellN

for row in ss[1:]:
    for n in range(0,len(row)):
        if headerN['mm-dd'] == n:
            print "Date is " + row[n]
