# CalDAV Bridge - work in progress!

Service that aggregates multiple calendars (single iCals over HTTP, CalDAV discovery, more to be added) and serves them as iCals with censored details.

Example typical scenarios are:
 - have work calendar subscribed in personal devices but only as timeframe when events occur - eg. to be at work before first one occurs
 - have personal calendar subscribed in corporate computer to accomodate personal errands during work time but without sharing any details - for example doctor appointments

## setup 
```
pip3 install -r requirements.txt
```