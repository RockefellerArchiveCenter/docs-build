FROM redhat/ubi8

ENV RUBY_VERSION=3.1.1
ENV CONTAINER_ROOT=/home/docs/docs-build/

RUN dnf -y install epel-release && dnf -y update && dnf -y --setopt=tsflags=nodocs install \
  make gcc curl gpg which \
  git \
  python310 \
  inotify-tools \
  httpd && \
  ln -fs /usr/bin/python3.10 /usr/bin/python && \
  ln -fs /usr/bin/pip3 /usr/bin/pip && \
  dnf -y clean all

# Install RVM and use RVM to install desired version of Ruby
RUN curl -sSL https://get.rvm.io | bash
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
