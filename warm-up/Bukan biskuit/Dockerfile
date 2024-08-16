
# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 10001 available to the world outside this container
EXPOSE 10001

# Define environment variable
ENV FLASK_ENV=development

# Run app.py when the container launches
CMD ["python", "server.py"]
