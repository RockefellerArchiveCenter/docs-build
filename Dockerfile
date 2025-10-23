FROM public.ecr.aws/lambda/python:3.12

ENV JEKYLL_BIN=/usr/local/bin/jekyll

# Install system packages
RUN dnf -y update && \
    dnf -y install \
      gcc gcc-c++ make \
      autoconf automake bison libtool patch \
      tar gzip bzip2 xz \
      git which procps-ng findutils ca-certificates \
      ruby ruby-devel rubygems \
      openssl-devel readline-devel zlib-devel libyaml-devel libffi-devel \
      gdbm-devel ncurses-devel sqlite-devel && \
    dnf clean all && rm -rf /var/cache/dnf

# Install Ruby gems
RUN gem update --system && \
    gem install bundler --no-document && \
    gem install jekyll --no-document

# Install Python dependencies
ADD requirements.txt ${LAMBDA_TASK_ROOT}
RUN pip install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

COPY update.py ${LAMBDA_TASK_ROOT}
COPY repositories.yml ${LAMBDA_TASK_ROOT}
COPY theme ${LAMBDA_TASK_ROOT}/theme

CMD [ "update.main" ]