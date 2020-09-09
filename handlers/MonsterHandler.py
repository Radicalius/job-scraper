from handlers.Handler import Handler
from handlers.Job import Job
from handlers.make_request import make_request

import requests, sys
from bs4 import BeautifulSoup

class MonsterHandler(Handler):

    type = "Monster"
    request = """
GET /jobs/search/pagination/?q=software-engineer&intcid=skr_navigation_nhpso_searchMainPrefill&isDynamicPage=true&isMKPagination=true&page={0}&total=26 HTTP/1.1
Host: www.monster.com
User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0
Accept: application/json, text/javascript, */*; q=0.01
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
X-Requested-With: XMLHttpRequest
Connection: keep-alive
Referer: https://www.monster.com/jobs/search/?q=software-engineer&intcid=skr_navigation_nhpso_searchMainPrefill&stpage=1&page=2
"""

    def __init__(self):
        self.cookies = requests.get("https://www.monster.com/jobs/search/?q=software-engineer&intcid=skr_navigation_nhpso_searchMainPrefill").cookies

    def get_num_pages(self):
        return 50

    def scan_page(self, n):
        json = make_request(MonsterHandler.request.format(n), cookies=self.cookies).json()
        meta = []
        for job in json:
            try:
                meta.append({
                    "title": job["Title"],
                    "comp": job["Company"]["Name"],
                    "loc": job["LocationText"],
                    "url": job["JobViewUrl"]
                })
            except:
                pass
                #print(sys.exc_info())
        return meta

    def scan_posting(self, meta):
        text = requests.get(meta["url"]).text
        bs = BeautifulSoup(text, "html.parser")
        desc = bs.find("div", {"class": "job-description"}).text
        return Job(
            meta["title"],
            meta["comp"],
            meta["loc"],
            desc,
            meta["url"]
        )
