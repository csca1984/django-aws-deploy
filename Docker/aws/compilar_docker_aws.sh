#!/bin/bash
set -e

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
PROJECT_ROOT=$(dirname "$SCRIPT_DIR")


DOCKERFILE="${PROJECT_ROOT}/Dockerfile"

IMAGE_NAME=django-app
AWS_ACCOUNT=154712418645
AWS_REGION=eu-west-1
REPO_BASE=${AWS_ACCOUNT}.dkr.ecr.${AWS_REGION}.amazonaws.com

IMAGE_TAG=$(cat "${SCRIPT_DIR}/.version")
IMAGE_FULL_PATH="$REPO_BASE/$IMAGE_NAME:$IMAGE_TAG"

echo "Building image from $DOCKERFILE"
echo "Using context $PROJECT_ROOT"

aws ecr get-login-password --region $AWS_REGION \
| docker login --username AWS --password-stdin "$REPO_BASE"

docker build -t "$IMAGE_FULL_PATH" -f "$DOCKERFILE" "$PROJECT_ROOT"
docker push "$IMAGE_FULL_PATH"

echo "Image pushed successfully"
