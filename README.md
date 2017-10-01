# Table of Contents
1. [Program Description](README.md#program-description)
2. [Data Pipeline](README.md#data-pipeline)
3. [Data Model](README.md#data-model)
4. [How to Run the Program](README.md#run-instruction)
5. [Limitations and Future Work](README.md#future-work)
6. [Contact](README.md#contact)


# Program Description

TweeTrade platform allows user to write and automate conditional execution on stock trading using public sentiment from a web UI. It ingests livestream Twitter firehose and ~3200 NASDAQ stock quotes (simulated) using Kafka, performs linear NLP sentiment analysis certain keywords on Twitter stream and window stock averaging on each ticker using Spark stream processing, and utilizes Apache Cassandra for its database infrastructure. 

# Data Pipeline

![data-pipeline](/Images/fig1-data-pipeline.png)

# Data Model
## Kafka Cluster Parameters & Settings

## Spark Streaming Parameters & Settings

## Cassandra Parameters & Settings

# How to Run the Program
## Dependencies
## Run Command (in sequence)

# Limitations and Future Work

# Contact
paurakh[at]gmail[dot]com






