# Use Python 3.9 slim as the base image
FROM python:3.9-slim

# Install necessary packages including gcc and other build tools
RUN apt-get update && apt-get install -y sqlite3 libsqlite3-dev gcc python3-dev musl-dev

# Set the working directory
WORKDIR /usr/src/app

# Copy the requirements file and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Initialize the database file
RUN sqlite3 app.db "CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY, text STRING NOT NULL);"

# Run the application
CMD [ "python", "./app.py" ]
