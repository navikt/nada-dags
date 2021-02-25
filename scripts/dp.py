from dataverk import Client, Datapackage
import datetime as dt

dp = Datapackage({
    "title": "erik tester",
    "bucket": "nav-opendata",
    "author": {"name": "NAV Kunnskapsavdelingen", "email": "statistikk@nav.no"},
    "temporal": {"from": "2010", "to": "2020"},
    "issued": "2021-02-02",
    "modified": dt.datetime.now().isoformat(),
    "readme": "blahblahblah"
})

dv = Client()
dv.publish(dp)
