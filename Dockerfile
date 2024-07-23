# Use playwright official python image as a base image
FROM mcr.microsoft.com/playwright/python:v1.31.1-focal

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install AWS CLI
RUN pip install awscli

# Copy the rest of your application code into the container
COPY . .

# Run scraper.py when the container launches
CMD ["python", "main.py"]