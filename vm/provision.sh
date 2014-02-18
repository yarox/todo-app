# Run the provisioning script in noninteractive mode
export DEBIAN_FRONTEND=noninteractive

# Update the package system first
sudo apt-get -y update

# Install packages
sudo apt-get install -y zsh
sudo apt-get install -y curl
sudo apt-get install -y unzip
sudo apt-get install -y git
sudo apt-get install -y build-essential
sudo apt-get install -y python
sudo apt-get install -y python-dev
sudo apt-get install -y libzmq-dev
sudo apt-get install -y python-zmq

# Install dependecies
sudo apt-get build-dep -y ipython ipython-notebook

if [ ! -f /home/vagrant/.first_run ]; then
    echo ">>> First run <<<"
    touch /home/vagrant/.first_run

    # Set and configure zsh as the default shell
    git clone git://github.com/robbyrussell/oh-my-zsh.git /home/vagrant/.oh-my-zsh
    cp /home/vagrant/.oh-my-zsh/templates/zshrc.zsh-template /home/vagrant/.zshrc
    chsh -s /usr/bin/zsh vagrant

    # Add some custom configuration to zsh
    echo "# Custom Vagrant configuration" >> /home/vagrant/.zshrc
    echo "bindkey '[D' backward-word" >> /home/vagrant/.zshrc
    echo "bindkey '[C' forward-word" >> /home/vagrant/.zshrc
    echo "cd /todo-app" >> /home/vagrant/.zshrc
    echo "alias notebook='ipython notebook --pylab=inline --no-browser --ip=0.0.0.0 --port=8888'" >> /home/vagrant/.zshrc
    echo "alias dev_appserver='/google_appengine/dev_appserver.py --port=8888 --host=0.0.0.0 --admin_port=9999 --admin_host=0.0.0.0 .'" >> /home/vagrant/.zshrc
    echo "alias remote_api_shell='/google_appengine/remote_api_shell.py -s localhost:8888'" >> /home/vagrant/.zshrc

    # Enable profile switching for iterm2
    echo "echo -e '\033]50;SetProfile=Vagrant\a'" >> /home/vagrant/.zlogin
    echo "echo -e '\033]50;SetProfile=Default\a'" >> /home/vagrant/.zlogout

    # Install distribute and pip
    curl http://python-distribute.org/distribute_setup.py | sudo python
    curl https://raw.github.com/pypa/pip/master/contrib/get-pip.py | sudo python

    # Download and install GAE
    wget http://googleappengine.googlecode.com/files/google_appengine_1.8.9.zip
    unzip google_appengine_1.8.9.zip -d /

    # Patch GAE's remote_api_shell to get an IPython console
    cp /hotaround/remote_api_shell.py /google_appengine/google/appengine/tools/

    # Restore '/home' ownership
    chown -R vagrant /home
fi

# Install python requirements
sudo pip install -r /vagrant/requirements.txt
