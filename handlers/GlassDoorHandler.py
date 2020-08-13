from handlers.Handler import Handler
from handlers.make_request import handlers.make_request

class GlassDoorHandler(Handler):

    type = "GlassDoor"

    request = """
GET /Job/jobs.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword=Software+Engineer&locT=N&locId=1&jobType=&context=Jobs&sc.keyword=Software+Engineer&dropdown=0 HTTP/2
Host: www.glassdoor.com
User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://www.glassdoor.com/
Upgrade-Insecure-Requests: 1
Connection: keep-alive
Cache-Control: max-age=0
TE: Trailers
"""

    def get_num_pages(self):
