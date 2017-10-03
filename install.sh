#!/bin/sh

# these install steps should work on all Ubuntu-based systems
# (tested on CentOS 7)

DIR=$(cd $(dirname $(readlink -f "$0" )); pwd)
if python -mplatform | grep -qi Ubuntu
then
  sudo apt-get -y install \
      git make gcc \
      python-pip python-setuptools \
      curl \
      #nodejs npm
else
  sudo yum -y install epel-release
  sudo yum -y update
  sudo yum -y install \
    git make gcc \
    python-pip python-setuptools \
    curl \
    #nodejs npm
fi

# Install RVM and use RVM to install Ruby 2.1.8
gpg --keyserver hkp://keys.gnupg.net --recv-keys 409B6B1796C275462A1703113804BB82D39DC0E3 7D2BAF1CF37B13E2069D6956105BD0E739499BDB
curl -sSL https://get.rvm.io | bash -s stable
source /home/vagrant/.rvm/scripts/rvm
rvm install 2.1.8
rvm use 2.1.8 --default

# UGLY HACK to work around the 'node' vs 'nodejs' issue in the shebangs of StaticAid .js files
#if [ "x`which node`" = "x" ]
#then
#    sudo ln -s `which nodejs` /usr/local/bin/node 2>/dev/null
#fi

sudo pip install requests Flask ipaddress pyyaml
gem install jekyll github-pages --no-rdoc --no-ri
#sudo npm install -g grunt-cli

# install NPM dependencies
#cd $DIR
#sudo npm install

# Add ssh keys
if [ -f ~/.ssh/id_rsa.pub ]
then
  echo "
  An SSH key already exists.
  "
else
  # create ssh key
  echo "
  Enter the email associated with a GitHub account for which you want to configure an SSH key: "
  read github_email
  ssh-keygen -t rsa -b 4096 -C "$github_email"
fi

eval "$(ssh-agent -s)"
ssh-add -k ~/.ssh/id_rsa

echo "
Done installing.

1. set up config.json
2. deploy in Apache
2. Add SSH key to Github: https://help.github.com/articles/adding-a-new-ssh-key-to-your-github-account/
3. Set up webhook URL.
"
