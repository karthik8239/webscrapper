# Deeds Scraper and Uploader:

This project scrapes deed information from the charlestoncounty deeds url("https://roddaybook.charlestoncounty.org/") and uploads the data to an AWS S3 bucket. The project is containerized using Docker and utilizes AWS ECR for storing Docker images. The application is built using Python with Playwright for web scraping and Boto3 for interacting with AWS services.

![image](https://github.com/user-attachments/assets/a10a1f19-7875-47e3-bb7f-2534bffe2d91)



## Prerequisites:
Docker: Ensure Docker is installed and running on your local machine. Install Docker
AWS CLI: Ensure AWS CLI is installed and configured with the necessary permissions. Install AWS CLI
Python: Ensure Python is installed. Install Python


## AWS Configuration

The AWS credentials should be configured using the AWS CLI:
aws configure

This command will prompt you to enter your AWS access key ID, secret access key, region, and output format. The credentials will be stored in ~/.aws/credentials and the configuration in ~/.aws/config.

## Configuration File
config.json file in the project root directory with the following content:

Customize the content for the required date,url of website you want to scrap the data:

{
  "date": "MM/DD/YYYY",
  "bucket_name": "your-s3-bucket-name",
  "url":"Your_url_page"
}


## Execution in Local steps:

-> pip install -r requirements.txt

-> python main.py

We can see the deed_info.pkl file saving in our repository

![Scrapping_execution_python_Screenshot](https://github.com/user-attachments/assets/ec24ea29-3885-471d-a6ce-3f19a7284467)

![Scrapped_data_pkl_file_screenshot](https://github.com/user-attachments/assets/0677a6d5-f2ae-4a87-b607-d0d69d91bded)


## Docker exectuion steps:

in setup_aws.sh file
So modify the credentials in the setup_aws.sh to point your aws_secret_Access_key,secret_key and region

## Build docker command (my-deeds-app -> image name):

docker build -t my-deeds-app .

Run the docker image:

docker run -it --rm my-deeds-app

You can see the aws_s3_bucket contains the .pkl file

![deed_info_S3_AWS_Screenshot](https://github.com/user-attachments/assets/6637c1e9-c404-4c6c-a385-f48f94a47822)


## ECR_DOCKER_image_Steps:

configure your credentials in the script.sh to point your ECR  repository name , account id ,image name and region

chmod +x script.sh

./script.sh

It will run and push the docker image to the ECR 

you can navigate to the AWS ECR Console and check the image

![ECR_Image_Docker_AWS_Screenshot](https://github.com/user-attachments/assets/db46e0de-abb9-477b-9724-c4ab6afd03e0)


##Testing the pushed docker image to AWS ECR

![Testing_ECR_docker_image_AWS_Screenshot](https://github.com/user-attachments/assets/a05dba8d-8928-4d64-abba-43333c8d92ac)








