# Set up a base image for Python-3.6 to use
FROM python:3.6

LABEL name="Invictus Assignment"
LABEL maintainer="Julian Kenwood"
LABEL version="1.0"

# Install the app requirements
WORKDIR /usr/src/app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy over the src directory and config files.
COPY src src
COPY words config.yaml ./

# Expose the 8000 port for this service
EXPOSE 8000

# Set default environment variables
ENV RABBITMQ_USER="guest"
ENV RABBITMQ_PASSWORD="guest"
ENV RABBITMQ_HOST="localhost"
ENV WORDS_PATH='words'
ENV LOG_LEVEL="DEBUG"

# Set an entrypoint to use
ENTRYPOINT [ "nameko", "run", "src.main", "--config", "config.yaml"]
