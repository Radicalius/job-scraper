import flask
from flask import *
import sys
import time
import datetime

app = Flask(__name__)

last_updated = datetime.datetime.now().strftime("%m/%d %H:%M")

@app.route("/")
def index():
    return """
<h2> New Grad Software Engineering Jobs </h2>
<hr/>
<img src=https://img.shields.io/endpoint?url=http://cache.nlogn.blog/job-scraper/number_of_jobs&style=plastic />
<img src=https://img.shields.io/endpoint?url=http://cache.nlogn.blog/job-scraper/last_update&style=plastic />
<p>A list of entry level software engineering jobs for recent graduates compiled from major job boards and updated daily<p>
<h3>Download</h3>
<ul>
    <li><a href=/jobs.csv>csv</a></li>
</ul>
    """

@app.route("/jobs.csv")
def csv():
    return send_file("jobs.csv")

@app.route("/number_of_jobs")
def number():
    return jsonify(
        {
            "schemaVersion": 1,
            "label": "jobs",
            "message": str(len(open("jobs.csv").readlines())),
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
