FROM public.ecr.aws/lambda/python:3.12

ENV RUBY_VERSION=3.2.4

# Install build tools
RUN dnf -y update && \
    dnf -y install \
      gcc gcc-c++ make \
      tar gzip bzip2 \
      curl wget git which \
      procps-ng \
      openssl-devel readline-devel zlib-devel libyaml-devel libffi-devel gdbm-devel ncurses-devel \
      ca-certificates findutils shadow-utils && \
    dnf clean all && rm -rf /var/cache/dnf

# Install RVM and Ruby
RUN curl -sSL https://rvm.io/mpapis.asc | gpg --import - && \
    curl -sSL https://rvm.io/pkuczynski.asc | gpg --import - && \
    curl -sSL https://get.rvm.io | bash -s stable

SHELL ["/bin/bash", "-lc"]

RUN source /etc/profile.d/rvm.sh && \
    rvm requirements && \
    rvm install "${RUBY_VERSION}" && \
    rvm --default use "${RUBY_VERSION}" && \
    gem update --system && \
    gem install bundler --no-document && \
    gem install jekyll --no-document

# Install Python dependencies
ADD requirements.txt ${LAMBDA_TASK_ROOT}
RUN pip install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

COPY update.py ${LAMBDA_TASK_ROOT}
COPY repositories.yml ${LAMBDA_TASK_ROOT}
COPY theme ${LAMBDA_TASK_ROOT}/theme

CMD [ "update.main" ]
