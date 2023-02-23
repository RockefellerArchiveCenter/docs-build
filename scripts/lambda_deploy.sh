#!/bin/bash -e

REGISTRY_URL=${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com
SOURCE_IMAGE="${DOCKER_REPO}"
TARGET_IMAGE="${REGISTRY_URL}/${DOCKER_REPO}"
VERSION="${TIMESTAMP}-${TRAVIS_COMMIT}"
TARGET_IMAGE_VERSIONED="${TARGET_IMAGE}:${VERSION}"

# make sure correct region is set
aws configure set default.region ${AWS_REGION}
# Log in to AWS
$(aws ecr get-login --no-include-email)

aws lambda update-function-code \
    --function-name  ${LAMBDA_FUNCTION_NAME} \
    --image-uri ${TARGET_IMAGE_VERSIONED}