import requests
import datetime

f = open("jobs.csv")
cont = f.read().encode('utf8')
f.close()

a = requests.post("http://cache.nlogn.blog/job-scraper/jobs.csv", data=cont)
b = requests.post("http://cache.nlogn.blog/job-scraper/number_of_jobs", data={
    "schemaVersion": 1,
    "label": "jobs",
    "message": cont.count(",https://".encode('utf8')),
    "color": "pink"
})
c = requests.post("http://cache.nlogn.blog/job-scraper/last_update", data={
    "schemaVersion": 1,
    "label": "updated",
    "message": datetime.datetime.now().strftime("%b %d, %Y at %H:%M"),
    "color": "green"
})
