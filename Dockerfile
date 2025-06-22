# Use official Python 3.9 image from Docker Hub
FROM python:3.10-buster

# Install dependencies and system libraries
RUN apt-get update && apt-get install --no-install-recommends -y \
  build-essential \
  libpq-dev \
  redis-server \
  libpangocairo-1.0-0 \
  libmagic1 libmagic-dev \
  && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /apps

# Copy the current directory to the container
COPY . .
COPY requirements.txt ./

# Install Python dependencies
RUN pip install --upgrade pip setuptools && pip install -r requirements.txt

# Make entrypoint script executable
RUN chmod +x entrypoint.sh

# Expose necessary ports
EXPOSE 8000 6379

# Run entrypoint.sh script
ENTRYPOINT ["sh", "entrypoint.sh"]
