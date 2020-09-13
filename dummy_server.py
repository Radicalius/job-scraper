import flask
from flask import *
import sys
import time
import datetime
import csv

app = Flask(__name__)

last_updated = datetime.datetime.now().strftime("%m/%d %H:%M")

jobs = []

@app.route("/")
def index():
    page = 1 if not "page" in request.args else request.args["page"]
    desc = 1 if not "desc" in request.args else request.args["desc"]
    return """
<h2> New Grad Software Engineering Jobs </h2>
<hr/>
<img src=https://img.shields.io/endpoint?url=https://cache.nlogn.blog/job-scraper/number_of_jobs&style=plastic />
<img src=https://img.shields.io/endpoint?url=https://cache.nlogn.blog/job-scraper/last_update&style=plastic />
<p>A list of entry level software engineering jobs for recent graduates compiled from major job boards and updated daily<p>
<h3>Download</h3>
<ul>
    <li><a href=/jobs.csv>csv</a></li>
</ul>
<iframe width=100% height=75% src=/page/{0}/desc/{1}></iframe>
    """.format(page, desc)

@app.route("/jobs.csv")
def job_csv():
    return send_file("jobs.csv")

@app.route("/page/<number>/desc/<num>")
def page(number, num):
    resp = "<table><tr><td>"
    resp += "<div style='overflow: scroll; height:500px' valign=top><h2>Page {0}</h2><ul>".format(number)
    for i in range(int(number)*20-20, int(number)*20):
        try:
            resp += "<li>"
            resp += "<a href=/page/{2}/desc/{1}><h3>{0}</h3></a>".format(jobs[i][0], i+1, number)
            resp += "{0}<br/>{1}<br/><a href={2} target='_blank'>View on Job Board</a>".format(jobs[i][1], jobs[i][2], jobs[i][-1])
            resp += "</li>"
        except:
            pass
    resp += "</ul>"
    resp += "<a href=/page/{0}/desc/{2}>Previous</a> <a href=/page/{1}/desc/{2}>Next</a>".format(int(number)-1, int(number)+1, num)
    resp += "</div></td><td valign=top>"
    try:
        resp += jobs[int(num)-1][3].replace("\n", "<br/>")
    except:
        pass
    resp += "</td></tr></table>"
    return resp

@app.route("/desc/<number>")
def desc(number):
    return jobs[int(number)-1][3].replace("\n", "<br/>")

@app.route("/number_of_jobs")
def number():
    return jsonify(
        {
            "schemaVersion": 1,
            "label": "jobs",
            "message": str(len(jobs)),
            "color": "pink"
        }
    )

@app.route("/last_update")
def last_update():
    return jsonify(
        {
            "schemaVersion": 1,
            "label": "updated",
            "message": last_updated,
            "color": "green"
        }
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(sys.argv[1]))
