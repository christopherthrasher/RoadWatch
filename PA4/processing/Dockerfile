# python version which will be used
FROM python:3.11.1-slim

# setting up the working directory in the container
WORKDIR /app

# copy the requirements file and install dependencies (will be updated)
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# copy python script in the container
COPY . .

# run the python script when the container starts
CMD [ "python", "app.py" ]