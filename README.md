# chicago-pyladies-digest

Currently includes a Python script for pulling the latest Python tech events in Chicago and saving to a CSV.

Can define an optional `meetup_key` in a `config.yml` file else can pass one in:

```
python meetup_events.py --location Chicago --text python --category 34
```

To create a MailChimp template define an optional `mailchimp_key` in a `config.yml`:

```
python email_template.py --template-name example6 --month Feb. --year 2016 --data career
```

