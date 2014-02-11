# todo-app
A simple TODO app example.

## Technologies
+ HTML5
+ CSS3
+ DOM Storage
+ IndexedDB
+ JavaScript
+ Bootstrap
+ Python
+ jQuery
+ Flask
+ Google App Engine

## Quick Start
You'll need to create your own `app.yaml` file. It should look like this:

```ỳaml
application: <your-gae-app-id>
version: 1
runtime: python27
api_version: 1
threadsafe: true

handlers:
- url: /.*
  script: todo-app.app

- url: /static
  static_dir: /static

builtins:
- remote_api: on
- appstats: on

libraries:
- name: jinja2
  version: latest

- name: pycrypto
  version: latest
```
