# Use an Alpine Conda image
FROM python:3.8.0a2-alpine3.9

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /tmp

# install graphviz
RUN apk add --no-cache --update gcc libc-dev libstdc++ graphviz graphviz-dev ttf-freefont
RUN pip install -r /tmp/requirements.txt

# Run script when the container launches
ENTRYPOINT ["python", "./src/main.py"]
