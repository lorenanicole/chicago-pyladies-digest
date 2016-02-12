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

To generate and post a template to MailChimp will need to provide a month, year. By default an email digest will include the following categories - career, conference, events, miscellaneous, and volunteer.
```
pyladies-digest --option template --template-name feb_digest --month Feb. --year 2016
pyladies-digest --option template --template-name feb_digest --month Feb. --year 2016 --data career conferences
```