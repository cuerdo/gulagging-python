# Use a base image with Python
FROM python:3.9-slim

# Set the working directory
WORKDIR /bot

# Copy application files
COPY . /bot

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Start Supervisor
CMD ["python", "bot.py"]