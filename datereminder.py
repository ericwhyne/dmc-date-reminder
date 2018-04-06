#!/usr/bin/python
import yaml
import requests
import requests
import csv
import sys
import json
from datetime import datetime, timedelta
from os.path import expanduser
import time

config_file = expanduser("~") + "/.datereminder/config.yml"
print config_file
mmdd = datetime.now().strftime("%m-%d")
yyyy = datetime.now().strftime("%Y")
yyyymmdd = date = datetime.now().strftime("%Y-%m-%d")
todayObj = datetime.strptime(yyyymmdd, "%Y-%m-%d")
try:
    config = yaml.safe_load(open(config_file))
except:
    print "Unable to read config file."
    sys.exit(0)

def slack(chan, text):
    payload = {
        "text":text,
        "channel": chan,
        "icon_emoji": config['icon_emoji'],
        "username": config['username']
    }
    slackr = requests.post(config['webhook'], data = json.dumps(payload))
    print "Slack response:", slackr.text
    time.sleep(1)

csv_r = requests.get(config['downloadurl'])
if csv_r.status_code != 200:
    print "Unable fo fetch spreadsheet. Not a 200 status code."
    sys.exit(0)

ss = list(csv.reader(csv_r.text.split('\n')))
header = ss[0]
headerN = {}
for cellN in range(0,len(header)):
    headerN[header[cellN].strip().lower()] = cellN

for row in ss[1:]:
    record = {}
    for n in range(0,len(row)):
        for hcol in headerN.keys():
            if headerN[hcol] == n:
                if row[n].strip() != '':
                    record[hcol] = row[n]
    if all(col in record.keys() for col in ['mm-dd', 'type', 'channel', 'days prior', 'text']):
        #print "Valid Record", record
        rec_date_obj = datetime.strptime(yyyy + "-" + record['mm-dd'], "%Y-%m-%d")
        rec_alert_date_obj = datetime.strptime(yyyy + "-" + record['mm-dd'], "%Y-%m-%d") - \
            timedelta(days=int(record['days prior']))
        if todayObj >= rec_alert_date_obj and todayObj <= rec_date_obj:
            days = (rec_date_obj - todayObj).days
            daystext = " in " + str(days) + " day"
            if days > 1:
                daystext += "s"
            if record['type'].lower().strip() == 'birthday':
                text = ':birthday: ' + record['text'] + " has a birthday" + daystext + " on " + record['mm-dd']
            else:
                text = record['text'] + daystext + " on " + record['mm-dd']
            print record['channel'], text
            slack(record['channel'], text)
