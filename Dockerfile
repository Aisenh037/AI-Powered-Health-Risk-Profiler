# Use an official, lightweight Python image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /code

# Copy the file that lists your Python dependencies
COPY ./requirements.txt /code/requirements.txt

# Install the dependencies
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# This is a key step for performance:
# We run a small script to pre-download the EasyOCR models
# so they are included in the package, avoiding slow server startups.
COPY ./preload_models.py /code/preload_models.py
RUN python /code/preload_models.py

# Copy your application code and simulator into the package
COPY ./app /code/app
COPY ./simulator.html /code/simulator.html

# The command to run your application when it starts
# It listens on all network interfaces (0.0.0.0) on port 10000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "10000"]