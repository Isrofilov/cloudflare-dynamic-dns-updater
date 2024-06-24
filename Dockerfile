FROM python:3.9-slim

# Install dependencies
RUN pip install requests

# Copy the script to the container
COPY update_dns.py /app/update_dns.py

# Set the working directory
WORKDIR /app

# Run the script
CMD ["python", "update_dns.py"]
