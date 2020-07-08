#!/usr/bin/python3

import yaml
from pprint import pprint
from datetime import datetime, date, timedelta
import caldav
from caldav.elements import dav, cdav
import icalendar
import argparse
from argparse import ArgumentParser
from enum import Enum
import urllib.request
from icalendar import Calendar, Event

class ProgramMode(Enum):
  dump='dump'
  blah='blah'

  def __str__(self):
    return self.value

parser = argparse.ArgumentParser(description='CalDAV bridge')
parser.add_argument('--config', type=str,         nargs=1, default='./config.yml')
parser.add_argument('--mode',   type=ProgramMode, nargs=1, choices=list(ProgramMode), required=True )
args = parser.parse_args()

with open(args.config) as f:
  config = yaml.load(f, Loader=yaml.FullLoader)

#pprint.pprint(config)

for caltype in ['home','work']:
  if config['calendars'][caltype]==None:
  	continue
  for cal in config['calendars'][caltype]:
    if cal==None:
      continue
    if cal['type']=='caldav':
      url='https://'+cal['user']+':'+cal['pass']+'@'+cal['url']
      client = caldav.DAVClient(url)
      principal = client.principal()
      calendars = principal.calendars()
      for calendar in calendars:
        if args.mode[0]==ProgramMode.dump:
          print(caltype, '- calendar', calendar)
          results = calendar.date_search(
            datetime.today() - timedelta(days=2),
            datetime.today() + timedelta(days=2)) #freebusy_request
          for event in results:
            print('  Found', event)
            data = calendar.event_by_url(event.url).load().data
            parsedCal = vobject.readOne(data)
            print('    Summary: ',parsedCal.vevent.summary.value)
            print('    Start:   ',parsedCal.vevent.dtstart.value)
            print('    End:     ',parsedCal.vevent.dtend.value)
    elif cal['type']=='ical':
      if args.mode[0]==ProgramMode.dump:
        print(caltype, '- calendar', cal['url'])
        with urllib.request.urlopen(cal['url']) as f:
          data = f.read().decode('utf-8')
          cal = Calendar.from_ical(data)
          for evt in cal.walk():
            if evt.name == "VEVENT":
              print('  Found')
              print('    Summary: ',evt.get('summary'))
              print('    Start:   ',evt.get('dtstart').dt)
              print('    End:     ',evt.get('dtend').dt)
            