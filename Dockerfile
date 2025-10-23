FROM public.ecr.aws/lambda/python:3.12

# Set Ruby version
ENV RUBY_VERSION=3.2.4

# Install build tools and ruby dependencies
RUN dnf -y update && \
    dnf -y install \
      gcc gcc-c++ make \
      tar gzip bzip2 \
      curl wget git which \
      gnupg2 procps-ng \
      openssl-devel readline-devel zlib-devel libyaml-devel libffi-devel gdbm-devel ncurses-devel \
      ca-certificates findutils shadow-utils && \
    dnf clean all && rm -rf /var/cache/dnf

# Install RVM and Ruby
RUN curl -sSL https://rvm.io/mpapis.asc | gpg2 --import - && \
    curl -sSL https://rvm.io/pkuczynski.asc | gpg2 --import - && \
    curl -sSL https://get.rvm.io | bash -s stable

# Use bash login shell so RVM is available in this layer
SHELL ["/bin/bash", "-lc"]

# Install requested Ruby and common gems
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

# Copy application files
COPY update.py ${LAMBDA_TASK_ROOT}
COPY repositories.yml ${LAMBDA_TASK_ROOT}
COPY theme ${LAMBDA_TASK_ROOT}/theme

CMD [ "update.main" ]