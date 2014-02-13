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
### Get the environment
Download and install [VirtualBox](https://www.virtualbox.org/wiki/Downloads) and [Vagrant] (http://www.vagrantup.com/downloads.html).

### Clone the project
Open a terminal and type `git clone https://github.com/yarox/hotaround.git`. This will create a folder containing the `master` branch of the project.

### Up and SSH
Open a terminal and type:

    cd /path/to/todo-app/vm/
    vagrant up --provision
    vagrant ssh

This will set up the virtual machine and then drop you into a full-fledged SSH session. Use `CTRL+D` to log out from the virtual machine. Once logged out, type `vagrant halt` to shut it down. Take a look of the rest of the Vagrant commands [here](http://docs.vagrantup.com/v2/cli/index.html).

### App.yaml
You will need to create your own `app.yaml` file. It should look like this:

```yaml
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

### Run the local server
Once into the virtual machine, type:

    /google_appengine/dev_appserver.py --host 0.0.0.0 --port 8888 --admin_host 0.0.0.0 --admin_port 9999 .

This will run the local server. The app will be listening on [localhost:8888](localhost:8888), and the admin panel on [localhost:9999](localhost:9999).
