from dataverk import Client, Datapackage
import datetime as dt

dp = Datapackage({
    "title": "erik tester",
    "bucket": "nav-opendata",
    "author": 'statistikk@nav.no',
    "temporal": {"from": "2010", "to": "2020"},
    "issued": "2021-02-02",
    "modified": dt.datetime.now().isoformat(),
    "readme": "blahblahblah",
    "format": "datapackage",
    "type": "datapackage",
    "store": "nais"
})

print(dp.dp_id)

dv = Client()
dv.publish(dp)
