FROM public.ecr.aws/lambda/python:3.11

ENV RUBY_VERSION=3.2.4

RUN yum update -y && yum install -y \
  make gcc curl gpg which tar procps wget \
  git

# Install RVM and use RVM to install desired version of Ruby
RUN \curl -L https://get.rvm.io | bash
RUN /bin/bash -l -c "rvm requirements"
RUN /bin/bash -l -c "rvm install $RUBY_VERSION"
RUN /bin/bash -l -c "gem install bundler --no-document"
RUN /bin/bash -l -c "gem install jekyll --no-document"

ADD requirements.txt ${LAMBDA_TASK_ROOT}
RUN pip install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

COPY update.py ${LAMBDA_TASK_ROOT}
COPY repositories.yml ${LAMBDA_TASK_ROOT}
COPY theme ${LAMBDA_TASK_ROOT}/theme

CMD [ "update.main" ]
