ACCOUNT_ID=<YOUR_Account_ID>
REGION=<Your_Region>
REPOSITORY_NAME=<Your_ECR_Public_repo_name>
IMAGE_NAME=<Docker_image_name>
TAG=latest

#Building the docker image
echo "Building the docker image"
docker build -t $IMAGE_NAME .

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


