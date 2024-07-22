ACCOUNT_ID=4259-2391-0586
REGION=us-east-2
REPOSITORY_NAME="webscrapper"
IMAGE_NAME=my-deeds-app
TAG=latest

#Tag the docker image
echo "tagging the docker image"
docker tag $IMAGE_NAME $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/$REPOSITORY_NAME:$TAG


#Authenticate Docker to ECR
echo "Authenticating Docker to ECR.."
aws ecr get-login-password --region $REGION | docker login --username AWS --password-stdin $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com

# Check if the repository exists
if aws ecr describe-repositories --repository-names $REPOSITORY_NAME --region $REGION >/dev/null 2>&1; then
    echo "Repository $REPOSITORY_NAME exists."
else
    echo "Repository $REPOSITORY_NAME does not exist. Creating repository..."
    aws ecr create-repository --repository-name $REPOSITORY_NAME --region $REGION
fi

# Push the Docker image to ECR
echo "Pushing the Docker image to ECR..."
docker push $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/$REPOSITORY_NAME:$TAG

echo "Docker image pushed successfully."


