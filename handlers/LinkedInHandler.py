import requests
from bs4 import BeautifulSoup

from handlers.make_request import make_request
from handlers.Handler import Handler
from handlers.Job import Job

class LinkedInHandler(Handler):

    type = "LinkedIn"
    request = """
GET /jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=junior%20new%20grad%20software%20engineer&location=&geoId=&trk=public_jobs_jobs-search-bar_search-submit&redirect=false&position=1&pageNum={2}&start={1} HTTP/2
Host: www.linkedin.com
User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Csrf-Token: {0}
Connection: keep-alive
Referer: https://www.linkedin.com/jobs/search?keywords=software%20engineer&location=&geoId=&trk=public_jobs_jobs-search-bar_search-submit&redirect=false&position=1&pageNum=0
TE: Trailers
"""

    def __init__(self):
        self.cookies = None

    def get_num_pages(self):
        r1 = requests.get("https://www.linkedin.com/jobs/search/?geoId=103644278&keywords=software%20engineer&location=United%20States")
        self.cookies = r1.cookies
        bs = BeautifulSoup(r1.text, "html.parser")
        #return int(int(bs.find(class_="results-context-header__job-count").text.replace(",","").replace("+","")) / 25)
        return 40

    def scan_page(self,n):
        r2 = make_request(LinkedInHandler.request.format(self.cookies["JSESSIONID"], (n)*25, n//40), cookies=self.cookies)
        bs = BeautifulSoup(r2.text, "html.parser")
        #result-card__title job-result-card__title title
        #result-card__full-card-link url
        #result-card__subtitle-link job-result-card__subtitle-link company
        #job-result-card__location location
        titles = [i.text for i in bs.findAll("h3", {"class": "result-card__title job-result-card__title"})]
        locs = [i.text for i in bs.findAll("span", {"class": "job-result-card__location"})]
        comps = [i.text for i in bs.findAll("a", {"class": "result-card__subtitle-link job-result-card__subtitle-link"})]
        urls = [i['href'] for i in bs.findAll("a", {"class": "result-card__full-card-link"})]
        return [{"title": title, "comp": comp, "loc": loc, "url": url} for title, loc, comp, url in zip(titles, locs, comps, urls)]

    def scan_posting(self,meta):

        r3 = requests.get(meta["url"])
        bs = BeautifulSoup(r3.text, "html.parser")

        desc = bs.findAll("div", {"class": "show-more-less-html__markup show-more-less-html__markup--clamp-after-5"})[0].text

        return Job(
            meta["title"],
            meta["comp"],
            meta["loc"],
            desc,
            meta["url"]
        )
