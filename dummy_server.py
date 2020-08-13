import flask
from flask import *
import sys
import time

app = Flask(__name__)

last_updated = time.time()

@app.route("/")
def index():
    return """
<h2> New Grad Software Engineering Jobs </h2>
<hr/>
<img src=https://img.shields.io/endpoint?url=https://new-grad-job-list.herokuapp.com/number_of_jobs&style=plastic />
<img src=https://img.shields.io/endpoint?url=https://new-grad-job-list.herokuapp.com/last_update&style=plastic />
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
            "message": str(int((time.time() - last_updated) // 3600))+" hours ago",
            "color": "green"
        }
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(sys.argv[1]))
