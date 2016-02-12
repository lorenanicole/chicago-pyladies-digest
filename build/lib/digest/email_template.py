#!/usr/bin/env python

from argparse import ArgumentParser
import requests
import yaml
import json
import codecs
import csv
from jinja2 import Environment, FileSystemLoader
import random
import os

__author__ = 'lorenamesa'

BASE_URL = 'https://{0}.api.mailchimp.com/{1}'
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(BASE_DIR, os.pardir))

TEMPLATE_ENVIRONMENT = Environment(
    autoescape=False,
    loader=FileSystemLoader('{0}/templates'.format(ROOT_DIR)),
    trim_blocks=False)

def render_template(template_filename, month=None, year=None, conferences=None, events=None, miscellaneous=None, volunteer=None, career=None):
    return TEMPLATE_ENVIRONMENT.get_template(template_filename).render(month=month, year=year, conferences=conferences, events=events, miscellaneous=miscellaneous, volunteer=volunteer, career=career)

def main(args):
    print "here are args , ", args
    if not args.get('key'):
        with open("{0}/config.yml".format(BASE_DIR), 'r') as stream:
            doc = yaml.load(stream)

        MAILCHIMP_KEY = doc['mailchimp_key']

    else:
        MAILCHIMP_KEY = args.get('key')

    # mailchimp api datacenter
    # http://developer.mailchimp.com/documentation/mailchimp/guides/get-started-with-mailchimp-api-3/
    dc_indx = MAILCHIMP_KEY.find('-')

    v2_base_url = BASE_URL.format(MAILCHIMP_KEY[dc_indx+1:], '3.0')
    v3_base_url = 'https://{0}.api.mailchimp.com/{1}'.format(MAILCHIMP_KEY[dc_indx+1:], '2.0')

    data = {}

    for item in args.get('data'):
        try:
            print "processing {0}".format(item)
            with open('{0}/data/{1}.csv'.format(ROOT_DIR, item), 'r') as datafile:
                reader = csv.DictReader(datafile)
                data[item] = [row for row in reader]
        except Exception as e:
            print "Couldn't process {0} | {1}".format(item, e.message)
            raise SystemExit

    with open('{0}/output.html'.format(BASE_DIR), 'w') as f:
            html = render_template('template.html', month=args.get('month'), year=args.get('year'),
                                   events=data.get('events'), conferences=data.get('conferences'),
                                   miscellaneous=data.get('miscellaneous'), volunteer=data.get('volunteer'),
                                   career=data.get('career'))
            f.write(html)

    f = codecs.open('{0}/output.html'.format(BASE_DIR), 'r', 'utf-8')
    template_html = "".join(line for line in f.read())

    payload = {'name': args.get('template_name'), 'html': template_html}
    response = requests.post(v3_base_url + '/templates/add.format?apikey={0}'.format(MAILCHIMP_KEY), data=payload)
    template_response = json.loads(response.content)

    if response.status_code == 200:
        print "Template #{0} -- {1} successfully made".format(template_response.get('template_id'), args.get('template_name'))
    else:
        print response.content

if __name__ == "__main__":

    main()
