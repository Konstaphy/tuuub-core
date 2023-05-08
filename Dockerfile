# Base image
FROM python:3.9-slim-buster

# Set the working directory
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app code to the container
COPY . .

# Expose the Flask app's default port
EXPOSE 8080

# Start the WSGI server
CMD ["waitress-serve", "--call", "wsgi:flask_app"]