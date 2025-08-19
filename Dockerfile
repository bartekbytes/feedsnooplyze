FROM alpine:latest

# Set environment variables to prevent Python from writing .pyc files and buffering output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install Python and pip
RUN apk add --no-cache python3 py3-pip py3-virtualenv

# Set work directory
WORKDIR /app

# Copy the application files
# Assuming 'snooplyze' is the main application directory
COPY ./snooplyze /app/snooplyze
COPY config.yaml requirements.txt /app

# Create and activate virtualenv, then install dependencies
# Use the virtual environment to isolate dependencies
RUN python3 -m venv /app/venv \
 && . /app/venv/bin/activate \
 && pip install --no-cache-dir -r requirements.txt

# Ensure the application files are executable
RUN chmod -R a+rx /app/snooplyze

# Run th app!
ENTRYPOINT ["/app/venv/bin/python", "-m", "snooplyze"]
