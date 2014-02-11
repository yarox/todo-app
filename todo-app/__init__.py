# -*- coding: utf-8 -*-

import datetime
import logging
import time
import uuid
import os

from google.appengine.api import memcache
from google.appengine.ext import ndb

from flask import Flask, request, render_template, jsonify
from werkzeug import DebuggedApplication

from Crypto.Random import random


# Config
SECRET_KEY = '\x81(\xfb\x80\t3\xcb\x94\x10l\xf9\x82\xb7H\x07N@\x98N\xd4n~\xbbq'
DEBUG = os.environ.get('SERVER_SOFTWARE') is None


# Create the application
app = Flask(__name__)
app.config.from_object(__name__)


# Utils
def datetime2unix(d):
    return time.mktime(d.timetuple()) + d.microsecond / 1e6


def unix2datetime(d):
    return datetime.datetime.utcfromtimestamp(d)


# Models
class ToDo(ndb.Model):
    text = ndb.StringProperty()
    tags = ndb.StringProperty(repeated=True)
    timestamp = ndb.DateTimeProperty(auto_now_add=True)

    def to_dict(self):
        result = super(ToDo, self).to_dict()
        result['timestamp'] = datetime2unix(self.timestamp)

        return result


# Views
@app.route('/', methods=['GET'])
def main():
    client_id = str(uuid.UUID(int=random.getrandbits(128)))
    logging.info('new client {0}'.format(client_id))

    return render_template('index.html', client_id=client_id)


@app.route('/sync', methods=['POST'])
def sync():
    logging.info('sync request')

    elements2add = []

    for e in request.json['new_items']:
        text = e['value']['text']
        timestamp = unix2datetime(e['value']['timestamp'])

        elements2add.append(ToDo(text=text, timestamp=timestamp))

    ndb.put_multi(elements2add)

    timestamps = [unix2datetime(e['value']['timestamp'])
                 for e in request.json['deleted_items']]

    if timestamps:
        elements2del = ToDo.query(ToDo.timestamp.IN(timestamps)).fetch(keys_only=True)
        ndb.delete_multi(elements2del)

    return jsonify({'response': 'OK'})
