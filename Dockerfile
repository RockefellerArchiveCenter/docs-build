FROM centos:6.10

RUN yum -y install https://centos6.iuscommunity.org/ius-release.rpm \
  epel-release && yum -y update && yum -y install \
  git2u make gcc \
  python-pip python-setuptools \
  curl \
  httpd mod_ssl

# Install RVM and use RVM to install Ruby 2.1.8
RUN gpg2 --keyserver hkp://pool.sks-keyservers.net --recv-keys 409B6B1796C275462A1703113804BB82D39DC0E3 7D2BAF1CF37B13E2069D6956105BD0E739499BDB
RUN curl -sSL https://get.rvm.io | bash -s stable
RUN /bin/bash -l -c ". /etc/profile.d/rvm.sh && \
  rvm install 2.1.8 && \
  rvm use 2.1.8 --default && \
  gem install rb-inotify:0.9.10 ruby_dep:1.3.1 listen:3.0.8 jekyll:3.6.2 --no-rdoc --no-ri"

RUN pip install pyyaml

RUN curl -sL https://rpm.nodesource.com/setup_10.x | bash -
RUN yum -y install nodejs

WORKDIR /home/docs/docs-build/
COPY package*.json ./
RUN npm install
RUN npm install http-server -g

ADD . .

EXPOSE 4000
