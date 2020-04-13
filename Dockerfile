FROM centos:7.5.1804

ENV RUBY_VERSION=2.6.6
ENV CONTAINER_ROOT=/home/docs/docs-build/

RUN yum -y install epel-release && yum -y update && yum -y --setopt=tsflags=nodocs install \
  make gcc curl gpg which \
  git \
  python-pip \
  inotify-tools \
  httpd mod_ssl && \
  yum -y clean all

# Install RVM and use RVM to install desired version of Ruby
RUN gpg2 --keyserver hkp://pool.sks-keyservers.net --recv-keys 409B6B1796C275462A1703113804BB82D39DC0E3 7D2BAF1CF37B13E2069D6956105BD0E739499BDB
RUN curl -sSL https://get.rvm.io | bash -s stable
RUN /bin/bash -l -c ". /etc/profile.d/rvm.sh && \
  rvm install ${RUBY_VERSION} && \
  rvm --default use ${RUBY_VERSION} && \
  gem install --no-document bundler jekyll:4.0.0"

ADD requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

WORKDIR ${CONTAINER_ROOT}

COPY apache/httpd.conf /etc/httpd/conf.d/docs.httpd.conf

ADD . .

EXPOSE 4000
EXPOSE 4001
