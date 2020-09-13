import Crypto
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Hash import SHA256
import Crypto.Signature.pkcs1_15
import base64
import requests
import sys
import os
import datetime
import csv
import json

def sign(privatekey,data):
    hash = SHA256.new(data.encode("utf8"))
    signer = Crypto.Signature.pkcs1_15.new(privatekey)
    return base64.b64encode(signer.sign(hash))

def upload(fname,cont,append=False):
    priv = RSA.import_key(os.environ["PRIVKEY"].replace("\\n", "\n"))
    dom = "job-scraper"
    method = requests.put if append else requests.post
    assert (method("https://cache.nlogn.blog/{0}/{1}".format(dom, fname), json={
            "content": cont,
            "signature": sign(priv, cont).decode("utf8")
    }).status_code) == 201

if __name__ == "__main__":
    upload("last_update", json.dumps({
        "color":"green",
        "label":"updated",
        "message":datetime.datetime.now().strftime("%m/%d %H:%M"),
        "schemaVersion":1
    }))

    with open("jobs.csv") as f:
        reader = csv.reader(f)
        i = 0
        for _ in reader:
            i += 1
        upload("number_of_jobs", json.dumps({
            "color":"pink",
            "label":"jobs",
            "message":str(i),
            "schemaVersion":1
        }))

    with open("jobs.csv") as f:
        c = f.read()
        chunk = 102400
        upload("jobs.csv",c[:chunk])
        i = chunk
        while i < len(c):
            upload("jobs.csv", c[i: i+chunk], append=True)
            print(i,i+chunk,len(c))
            i+=chunk
