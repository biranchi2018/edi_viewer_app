# Create a Dockerfile to containerize the EDI 837 Viewer application
FROM python:3.11-slim
# Set the working directory
WORKDIR /app    
# Copy the application files into the container
COPY . /app
# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt
# Expose the port the app runs on
EXPOSE 5000
# Set the environment variable for Flask
ENV FLASK_APP=app.py
# Set the environment variable to run Flask in production mode
ENV FLASK_ENV=production
# Command to run the application
CMD ["python", "app.py"]
