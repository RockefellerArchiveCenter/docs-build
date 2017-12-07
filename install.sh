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
      apache2 apache2-doc apache2-utils
  else
    sudo yum -y install epel-release
    sudo yum -y update
    sudo yum -y install \
      git make gcc \
      python-pip python-setuptools \
      curl \
      httpd mod_ssl
fi

# Install RVM and use RVM to install Ruby 2.1.8
gpg --keyserver hkp://keys.gnupg.net --recv-keys 409B6B1796C275462A1703113804BB82D39DC0E3 7D2BAF1CF37B13E2069D6956105BD0E739499BDB
curl -sSL https://get.rvm.io | bash -s stable
source ~/.rvm/scripts/rvm
rvm install 2.1.8
rvm use 2.1.8 --default

sudo pip install requests Flask ipaddress pyyaml
gem install jekyll github-pages --no-rdoc --no-ri

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
Done installing dependencies.

NEXT STEPS
1. Update variables in config.json
    See README.md for further information.
2. Deploy in Apache by adding a WSGIScriptAlias directive to your VirtualHost file.
    See README.md for details.
3. Add the SSH key created above to GitHub.
    See GitHub documentation for SSH keys.
4. Set up webhook URL in GitHub.
    See Github documentation for Webhooks.
"
