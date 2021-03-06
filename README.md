# chicago-pyladies-digest

Python project to scrape data from MeetUp and Lanyard for generating a MailChimp template for a PyLadies email digest.

To use will need to first setup config with API keys:

```
pyladies-digest --option config --meetup_key very_secret --mailchimp_key much_more_secret

```

To scrape MeetUp for events in a location, need to provide a [category](http://www.meetup.com/meetup_api/docs/2/categories/) and text to look for in an event's description.

```
pyladies-digest --option scrape_events --location Chicago --text python --category 34
```

To scrape Lanyard for upcoming conferences and conference CFPs you can provide a query for both conference topics and conference calls.
```
pyladies-digest --option scrape_confs --calls python --topic python
```

To generate and post a template to MailChimp will need to provide a month, year. By default an email digest will include the following categories - career, conference, events, miscellaneous, and volunteer. If you want to
update the data (notes on data format below) used in the digest, provide a location of the new data file for the respective type (e.g. `--career /Users/lm/desktop/career.csv`).
```
pyladies-digest --option template --template-name feb_digest --month Feb. --year 2016 --city Chicago --fb https://www.facebook.com/Chicago-PyLadies-303889346486875/?ref=aymt_homepage_panel
pyladies-digest --option template --template-name feb_digest --month Feb. --year 2016 --city Chicago --data career conferences --fb https://www.facebook.com/Chicago-PyLadies-303889346486875/?ref=aymt_homepage_panel --tw http://www.twitter.com/pyladieschicago
pyladies-digest --option template --template-name feb_digest --month Feb. --year 2016 --city Chicago --career /Users/lm/desktop/career.csv --misc /Users/lm/desktop/misceallaneous.csv --volunteer /Users/lm/desktop/volunteer.csv
```

###Data Format

*Career*: `title,description,contact_url,contact_text`
*Conferences*: `date,name,location,url,cfp,cfp_url,cfp_deadline,fa,fa_url,fa_deadline`
*Events*: `date,event_url,group,name`
*Miscellaneous*: `text,contact_url,contact_text`
*Volunteer*: `text,contact_url,contact_text`