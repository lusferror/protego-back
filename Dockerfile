FROM python:3.12.1-slim as backend

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Copy the requirements file
COPY requirements.txt /app/requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY entry-point.sh /app/entry-point.sh

RUN chmod a+x /app/entry-point.sh

ENTRYPOINT ["./entry-point.sh"]

# Run app.py when the container launches
CMD ["python", "/app/app.py"]