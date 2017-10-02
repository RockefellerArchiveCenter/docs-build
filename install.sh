#!/bin/sh

# these install steps should work on all Ubuntu-based systems
# (tested on Mint 17.3)

DIR=$(cd $(dirname $(readlink -f "$0" )); pwd)
python -mplatform | grep -qi Ubuntu && sudo apt-get -y install \
    git make gcc \
    python-pip python-setuptools \
    ruby ruby-dev \
    nodejs npm ||
    sudo yum -y install \
    epel-release \
    git make gcc \
    python-pip python-setuptools \
    ruby ruby-devel \
    nodejs npm


# UGLY HACK to work around the 'node' vs 'nodejs' issue in the shebangs of StaticAid .js files
if [ "x`which node`" = "x" ]
then
    sudo ln -s `which nodejs` /usr/local/bin/node 2>/dev/null
fi

sudo pip install requests Flask ipaddress pyyaml json
sudo gem install jekyll github-pages --no-rdoc --no-ri
sudo npm install -g grunt-cli

# install NPM dependencies
cd $DIR
sudo npm install

echo "
Done installing.

THINGS YOU NEED TO DO NEXT
"
