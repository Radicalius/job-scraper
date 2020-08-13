import flask
from flask import *
import sys

app = Flask(__name__)

@app.route("/")
def index():
    return """
<h2> New Grad Software Engineering Jobs </h2>
<hr/>
<p>A list of entry level software engineering jobs for recent graduates compiled from major job boards and updated daily<p>
<h3>Download</h3>
<ul>
    <li><a href=/jobs.csv>csv</a></li>
</ul>
    """

@app.route("/jobs.csv")
def csv():
    return send_file("jobs.csv")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(sys.argv[1]))
