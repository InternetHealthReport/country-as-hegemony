FROM python:3.9.16

# Upgrade pip
RUN pip3 install --no-cache-dir --upgrade pip

# Set working directory
WORKDIR /app

# Copy the application code into the container
COPY . /app

# Install dependencies
RUN pip3 install --no-cache-dir -r requirements.txt country-as-hegemony

# Set entrypoint to bash
ENTRYPOINT ["/bin/bash"]