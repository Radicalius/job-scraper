import requests

request = """
GET /v1/dice/jobs/search?q=software%20engineer&countryCode2=US&radius=30&radiusUnit=mi&page=100&pageSize=50&facets=employmentType%7CpostedDate%7CworkFromHomeAvailability%7CemployerType%7CeasyApply%7CisRemote&fields=id%7CjobId%7Csummary%7Ctitle%7CpostedDate%7CjobLocation.displayName%7CdetailsPageUrl%7Csalary%7CclientBrandId%7CcompanyPageUrl%7CcompanyLogoUrl%7CpositionId%7CcompanyName%7CemploymentType%7CisHighlighted%7Cscore%7CeasyApply%7CemployerType%7CworkFromHomeAvailability%7CisRemote&culture=en&recommendations=true&interactionId=0&fj=true&includeRemote=true HTTP/2
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

meths = {
    "GET": requests.get,
    "POST": requests.post
}

def make_request(req):
    """make a request formatted like google inspect toolbar and return result"""
    lines = req.split("\n")
    meth, path, ver = lines[1].split(" ")
    headers = {i.split(":")[0].strip(): i.split(":")[1].strip() for i in lines[2:] if len(i.split(":")) > 1}
    return meths[meth]("https://"+headers["Host"]+path, headers=headers)

if __name__ == "__main__":
    print(make_request(request).json())
