# Use the official Python image as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code to the container
COPY . .

# Expose the port the Flask app will run on
EXPOSE 5001 

# Set the environment variable for the API key
ENV OPEN_AI_KEY=""

# Set the environment variables
ENV PORT=5001
ENV DOTENV_PATH=/app/.env

# Run the Flask app
CMD ["python", "api.py"]
