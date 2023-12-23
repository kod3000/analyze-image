# Use an official Python runtime as a parent image
FROM python:3.10.10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set Api key for OpenAI
ENV OPENAI_API_KEY_1=SECREEEETKEEEEYS
ENV OPENAI_API_KEY_2=SECREEEETKEEEEYS

# Set the working directory in the container
WORKDIR /app/backend

# Copy the current directory contents into the container at /app
COPY . /app/backend

# Install any needed packages specified in requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# Run tests
RUN python3 manage.py test api.tests.api_health_endpoint --noinput
RUN python3 manage.py test api.tests.api_image_upload --noinput
RUN python3 manage.py test api.tests.api_serve_thumbnail --noinput


# Expose the port the app runs on
EXPOSE 8000

# Run the command to start uWSGI
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
