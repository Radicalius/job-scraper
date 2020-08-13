from handlers.Handler import Handler
from handlers.make_request import make_request
from handlers.Job import Job

import requests
from bs4 import BeautifulSoup

class DiceHandler(Handler):

    type = "Dice"
    request = """
GET /v1/dice/jobs/search?q=software%20engineer&countryCode2=US&radius=30&radiusUnit=mi&page={0}&pageSize=20&facets=employmentType%7CpostedDate%7CworkFromHomeAvailability%7CemployerType%7CeasyApply%7CisRemote&fields=id%7CjobId%7Csummary%7Ctitle%7CpostedDate%7CjobLocation.displayName%7CdetailsPageUrl%7Csalary%7CclientBrandId%7CcompanyPageUrl%7CcompanyLogoUrl%7CpositionId%7CcompanyName%7CemploymentType%7CisHighlighted%7Cscore%7CeasyApply%7CemployerType%7CworkFromHomeAvailability%7CisRemote&culture=en&recommendations=true&interactionId=0&fj=true&includeRemote=true HTTP/2
Host: job-search-api.svc.dhigroupinc.com
User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0
Accept: application/json, text/plain, */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
x-api-key: 1YAt0R9wBg4WfsF9VB2778F5CHLAPMVW3WAZcKd8
Origin: https://www.dice.com
Connection: keep-alive
Referer: https://www.dice.com/jobs?q=software%20engineer&countryCode=US&radius=30&radiusUnit=mi&page=1&pageSize=20&language=en
Cache-Control: max-age=0
TE: Trailers
"""

    def _load_page(self, n):
        return make_request(DiceHandler.request.format(n)).json()

    def get_num_pages(self):
        return self._load_page(1)["meta"]["pageCount"]

    def scan_page(self,n):
        return self._load_page(n+1)["data"]

    def scan_posting(self, m):
        title = m["title"]
        comp = m["companyName"]
        loc = "n/a" if "jobLocation" not in m else m["jobLocation"]["displayName"]
        url = m["detailsPageUrl"]

        details = requests.get(url).text
        doc = BeautifulSoup(details, 'html.parser')
        desc = doc.find(id="jobdescSec").text

        return Job(
            title, comp, loc, desc, url
        )
