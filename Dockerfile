FROM python:3.10-slim-bullseye

# Set the environment variables
ENV PYTHONPATH="${PYTHONPATH}:/opt/app/" \
    SITE="encuentra24" \
    MAX_PAGES=10000

# Set the working directory
WORKDIR /opt/app

# Install the required packages
RUN apt-get update && \
    apt-get install -y \
    build-essential \
    python3-launchpadlib \
    python3-dev \
    python3-pip \
    gcc \
    && apt-get clean

# Copy the project files into the working directory
ADD project/ ./project
COPY config.toml main.py requirements.txt ./

# Install the project dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Run the application
CMD python3 main.py ${SITE} ${MAX_PAGES}
