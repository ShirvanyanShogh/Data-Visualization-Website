from flask import Flask
import json
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = '966e27e8d5eb01266f43dc96f8a9d812'

with open(os.path.join('website_project', 'users')) as json_file:
    db = json.load(json_file)

from website_project import routes
