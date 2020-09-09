from handlers.Handler import Handler
from handlers.Job import Job

import requests
from bs4 import BeautifulSoup
import re

class IndeedHandler(Handler):

    type = "Indeed"

    def __init__(self):
        self.url = "https://www.indeed.com/jobs?q=software+engineer&start={0}"

    def get_num_pages(self):
        return 101

    def scan_page(self, n):
        text = requests.get(self.url.format((n-1)*10)).text
        bs = BeautifulSoup(text, "html.parser")
        as_ = bs.findAll("a", {"class": "jobtitle turnstileLink "})
        links = ['https://indeed.com'+i['href'] for i in as_]
        titles = [i.text for i in as_]
        divs = bs.findAll("div", {"class": "sjcl"})
        locs = []
        for i in divs:
            loc = i.find("span", {"class": "location accessible-contrast-color-location"})
            if loc:
                locs.append(loc.text)
            else:
                locs.append("Remote")
        comps = [i.text for i in bs.findAll("span", {"class": "company"})]
        return [{
            "title": title.strip(),
            "comp": comp.strip(),
            "loc": loc.strip(),
            "url": link
        } for title, comp, loc, link in zip(titles, comps, locs, links)]

    def scan_posting(self, meta):
        text = requests.get(meta["url"]).text
        bs = BeautifulSoup(text, "html.parser")
        desc = bs.find("div", {"id": "jobDescriptionText"})
        return Job(
            meta["title"],
            meta["comp"],
            meta["loc"],
            desc,
            meta["url"]
        )
