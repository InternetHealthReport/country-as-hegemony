FROM python:3.9.16

# Upgrade pip
RUN pip3 install --no-cache-dir --upgrade pip

# Set working directory
WORKDIR /app

# Copy the application code into the container
COPY . /app

# Install dependencies
RUN pip3 install --no-cache-dir -r requirements.txt country-as-hegemony

# Install cron and its log file
RUN apt-get update && apt-get -y install cron nano

# Add crontab file in the cron directory
COPY crontab /var/spool/cron/crontabs/root

# Set command to start cron service
CMD ["/usr/sbin/cron", "-f"]