import json
import requests
import yaml
from datetime import datetime, timedelta
import csv
from argparse import ArgumentParser

BASE_URL = 'https://api.meetup.com/'

def date_within_num_days(utc_offset, utctimestamp, days=30):
    utctimestamp = (int(utctimestamp) + int(utc_offset)) / 1000.0
    margin = timedelta(days=days)
    return datetime.fromtimestamp(utctimestamp) - datetime.now() <= margin

def utc_timestamp_to_datetime_string(utc_offset, utctimestamp):
    utctimestamp = (int(utctimestamp) + int(utc_offset)) / 1000.0
    return datetime.fromtimestamp(utctimestamp).strftime("%m/%d/%y")


if __name__ == "__main__":

    with open("config.yml", 'r') as stream:
        doc = yaml.load(stream)


    MEETUP_KEY = doc['meetup_key']

    parser = ArgumentParser()
    parser.add_argument(
        '--category', default='34', metavar='str', type=str,
         help='category as defined by MeetUp API http://www.meetup.com/meetup_api/docs/2/categories/')
    parser.add_argument(
        '--location', default='Chicago', metavar='str', type=str,
         help='location to query group events for e.g. Chicago')
    parser.add_argument(
        '--text', default='python', metavar='str', type=str,
         help='text to query group events for e.g. Python')
    parser.add_argument(
        '--key', default=MEETUP_KEY, metavar='str', type=str,
         help='MeetUp API key https://secure.meetup.com/meetup_api/key/')

    args = parser.parse_args().__dict__

    upcoming_events = BASE_URL + 'find/groups?category={0}&location={1}&key={2}&text={3}&upcoming_events=true'.format(args.get('category'),
                                                                                                                      args.get('location'),
                                                                                                                      args.get('key'),
                                                                                                                      args.get('text'))

    response = requests.get(upcoming_events)
    data = json.loads(response.content)

    events = {}
    for d in data:
        if 'python' in d.get('description').lower() and d.get('next_event'):
            next_event = d.get('next_event')
            if date_within_num_days(next_event.get('utc_offset'), next_event.get('time')):
                date = utc_timestamp_to_datetime_string(next_event.get('utc_offset'), next_event.get('time'))
                events[d.get('name')] = {'id': next_event.get('id'),
                                         'date': date,
                                         'name': next_event.get('name')}

    event_ids = [event_data.get('id') for event, event_data in events.iteritems()]

    upcoming_events = BASE_URL + '2/events?key={0}&event_id={1}'.format(MEETUP_KEY, ','.join(event_ids))

    response = requests.get(upcoming_events)
    data = json.loads(response.content).get('results')

    for d in data:
        group_name = d.get('group').get('name')
        if events.get(group_name):
            events[group_name]['event_url'] = d.get('event_url')
            events[group_name]['group'] = d.get('group').get('name')
            events[group_name].pop('id')

    with open('events.csv', 'w') as python_events:
        headers = events.get(events.keys()[0]).keys()

        writer = csv.DictWriter(python_events, fieldnames=headers)
        writer.writeheader()

        for group, event in events.iteritems():
            writer.writerow(event)



