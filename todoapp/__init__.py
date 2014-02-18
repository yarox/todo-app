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


def parse_object(object):
    object['client_timestamp'] = unix2datetime(object['client_timestamp'])
    return object


# Models
class Item(ndb.Model):
    text = ndb.StringProperty()
    tags = ndb.StringProperty(repeated=True)
    is_deleted = ndb.BooleanProperty(default=False)

    server_timestamp = ndb.DateTimeProperty(auto_now=True)
    client_timestamp = ndb.DateTimeProperty()

    def to_dict(self):
        result = super(Item, self).to_dict()
        result['timestamp'] = datetime2unix(self.client_timestamp)
        result['server_key'] = self.key.urlsafe()

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

    # 1. obtener los nuevos elementos del servidor (incluye elementos nuevos y
    #    elementos a borrar).
    timestamp = unix2datetime(request.json['server_timestamp'])
    items_unsynced = Item.query(Item.server_timestamp > timestamp).order(Item.server_timestamp).fetch()

    if items_unsynced:
        last_server_timestamp = items_unsynced[-1].server_timestamp
    else:
        last_server_timestamp = unix2datetime(0)

    # 2. insertar en el servidor los nuevos elementos del cliente. obtener sus
    #    claves para enviarlas de vuelta.
    items_client = [Item(**parse_object(item['object'])) for item in request.json['items_new']]
    ndb.put_multi(items_client)

    if items_client:
        last_client_timestamp = max(items_client, key=lambda i: i.server_timestamp).server_timestamp
    else:
        last_client_timestamp = timestamp

    # 3. actualizar en el servidor los elementos marcados para borrar del
    #    cliente y actualizar su server_timestamp.
    items_update = ndb.get_multi([ndb.Key(urlsafe=item['value']['serverKey']) for item in request.json['items_delete']])

    for item in items_update:
        item.is_deleted = True

    ndb.put_multi(items_update)

    if items_update:
        last_update_timestamp = max(items_update, key=lambda i: i.server_timestamp).server_timestamp
    else:
        last_update_timestamp = timestamp

    # 4. enviar la respuesta al cliente.
    server_timestamp = datetime2unix(max(last_server_timestamp,
                                         last_client_timestamp,
                                         last_update_timestamp))
    items_server, items_delete = [], []

    for item in items_unsynced:
        if item.is_deleted:
            items_delete.append(item.to_dict())
        else:
            items_server.append(item.to_dict())

    return jsonify({
        'itemsServer': items_server,
        'itemsDelete': items_delete,
        'itemsClient': [item.to_dict() for item in items_client],
        'serverTimestamp': server_timestamp
    })
