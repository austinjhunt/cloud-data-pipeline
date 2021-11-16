# Author: Austin Hunt
# Vanderbilt University
# Created: Fall 2021
#
# For Cloud Computing class, Assignment #4
# Here we create an image for Apache Spark so we can run
# both the master and workers

# Build with (from current directory): docker build -t austinjhunt/cs5287spark .
# Push with: docker push austinjhunt/cs5287spark

FROM ubuntu:latest
#
# Now install the needed packages.
RUN apt-get -y update && apt-get install -y default-jdk python3
RUN apt-get install -y python3-dev python3-pip
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install --upgrade pyspark
RUN python3 -m pip install --upgrade couchdb

# Note, I have added several other packages that provide networking utilities like
# ping, nslookup, ifconfig etc.
RUN apt-get -y update && apt-get install -y net-tools wget dnsutils iputils-ping iputils-tracepath iputils-arping iputils-clockdiff

# Here we are hardcoding the download mirror and the spark version. I am sure
# there will be another and better way to do this
RUN wget https://dlcdn.apache.org/spark/spark-3.2.0/spark-3.2.0-bin-hadoop3.2.tgz
RUN tar -xvzf spark-*

COPY spark-env.sh /spark-3.2.0-bin-hadoop3.2/conf/
COPY spark-worker.conf /spark-3.2.0-bin-hadoop3.2/conf/
COPY spark-driver.conf /spark-3.2.0-bin-hadoop3.2/conf/
COPY iot-mapreduce.py /

# Now we set environment variable that we will need in the container at runtime
ENV SPARK_HOME=/spark-3.2.0-bin-hadoop3.2
ENV PATH=${PATH}:${SPARK_HOME}/sbin:${SPARK_HOME}/bin


# Define the following environment variables at runtime for the container for the Python script to work
# COUCHDB_SERVER
# COUCHDB_USER
# COUCHDB_PASSWORD
# COUCHDB_DATABASE
CMD ["python3", "/mapreduce.py"]


