# Pinterest Experiment Analytics Data Pipeline Project

## Table of Contents

- [Project Overview](#Project-Overview)
- [Architecture Overview](#Architecture-Overview)
- [Milestone 1: Environment Setup](#Milestone-1-Environment-Setup)
- [Milestone 2: Building the Pipeline Foundation](#Milestone-2-Building-the-Pipeline-Foundation)
- [Milestone 3: EC2 Kafka Client Configuration](#Milestone-3-EC2-Kafka-Client-Configuration)
- [Milestone 4: Connecting MSK Cluster to S3 Bucket](#Milestone-4-Connecting-MSK-Cluster-to-S3-Bucket)
- [Milestone 5: API Gateway and REST Proxy Configuration](#Milestone-5-API-Gateway-and-REST-Proxy-Configuration)
- [Milestone 6: Databricks Setup and S3 Integration](#Milestone-6-Databricks-Setup-and-S3-Integration)
- [Milestone 7: Data Cleaning and Transformation with Spark](#Milestone-7-Data-Cleaning-and-Transformation-with-Spark)
- [Milestone 8: Automating with AWS MWAA](#Milestone-8-Automating-with-AWS-MWAA)
- [Milestone 9: Real-Time Data Processing with AWS Kinesis](#Milestone-9-Real-Time-Data-Processing-with-AWS-Kinesis)
- [Conclusion](#Conclusion)

## Project Overview

This project focuses on building a Pinterest data pipeline that ingests, processes, and analyzes data from Pinterest using AWS services like MSK (Managed Streaming for Apache Kafka), S3, and Kinesis, along with Databricks for data processing and analysis. The pipeline simulates a production environment where data is ingested in real-time and batch modes, processed, and stored for analysis.

## Architecture Overview

The architecture of this project is designed to simulate a real-time data pipeline. It involves several key components:

- **AWS MSK Cluster:** Used to manage Kafka for data ingestion.
- **EC2 Instances:** Serve as Kafka clients for producing and consuming data.
- **S3 Buckets:** Store raw and processed data.
- **API Gateway:** Facilitates data ingestion into Kafka or Kinesis.
- **AWS Kinesis:** Manages streaming data.
- **Databricks:** Used for processing and analyzing the data.

## Milestone 1&2: Environment Setup

The initial phase involved setting up the development environment. This included:

- **Setting up the GitHub repository:** The repository was created and organized to manage project files and documentation.
- **Python Environment:** Essential libraries like pymysql, boto3, and sqlalchemy were installed to manage database connections and interactions.
- **AWS Credentials:** The AWS environment was configured using pre-existing credentials, with access to IAM roles and an SSH keypair for secure access to resources.

_To begin, infrastructure was established to simulate a typical Pinterest data engineering environment. A zip package containing the user_posting_emulation.py script was downloaded. This script connects to an RDS (Relational Database Service) instance holding three key tables:_

- _**pinterest_data**: Contains information about posts uploaded to Pinterest._
- _**geolocation_data**: Stores geolocation data linked to each Pinterest post._
- _**user_data**: Includes details about the users who uploaded the posts._

_A db_creds.yaml file was then created to securely store the database credentials (HOST, USER, PASSWORD), ensuring these details were not uploaded to GitHub by adding the file to the .gitignore list. A class was created to connect to the RDS database using parameters like HOST, USER, PASSWORD, etc._

_A Python script (run_infinite_post_data_loop) was implemented to simulate continuous data ingestion from Pinterest, emulating user interactions with the Pinterest API. The script fetched random rows from tables (pinterest_data, geolocation_data, user_data) and outputted them as key-value pairs._

## Milestone 3: EC2 Kafka Client Configuration

This milestone focused on setting up an EC2 instance to act as a Kafka client:

- **SSH Access:** A key pair was generated and used to SSH into the EC2 instance.
- **Kafka Installation:** Apache Kafka was installed on the EC2 instance, along with the necessary IAM MSK authentication jar, enabling secure communication with the MSK cluster.
- **Topic Creation:** Using the Kafka command-line tools, three topics (pin, geo, user) were created in the MSK cluster, ready to receive data.

_A key pair file was generated locally with a .pem extension, allowing secure SSH access to the EC2 instance. This key pair was retrieved from the AWS Parameter Store and saved locally. The key was used to establish an SSH connection to the EC2 instance, ensuring secure communication._

_Apache Kafka was installed on the EC2 instance. Alongside this, the IAM MSK authentication package was configured to enable secure communication between the EC2 client and the MSK cluster. The necessary environment variables were set to ensure proper path configurations and to establish the EC2 instance’s ability to use AWS IAM for MSK cluster authentication._

_The EC2 instance was configured to authenticate with the MSK cluster using IAM roles. This involved setting up trust relationships and modifying client properties to include the IAM role ARN, which grants the necessary permissions for cluster access._

_Three Kafka topics were created within the MSK cluster—pin, geo, and user. These topics were configured using the Kafka command-line tools, with bootstrap servers and Zookeeper connection strings retrieved from the MSK management console. The CLASSPATH environment variable was set appropriately to ensure seamless operation of the Kafka commands._

## Milestone 4: Connecting MSK Cluster to S3 Bucket

The objective here was to ensure that data flowing through Kafka topics was automatically stored in an S3 bucket:

- **Plugin Creation:** A custom MSK Connect plugin was created using the Confluent S3 connector, which was uploaded to an S3 bucket.
- **Connector Configuration:** A connector was configured within MSK Connect to route data from the Kafka topics to corresponding S3 buckets, ensuring persistent storage of streamed data.

_A custom plugin was created using the Confluent.io Amazon S3 Connector. This plugin was designed to manage the transfer of data from the Kafka topics to the designated S3 bucket. The plugin was downloaded to the EC2 client and then uploaded to an S3 bucket._

_The S3 bucket was already configured with the necessary VPC endpoint and IAM roles, eliminating the need for additional setup_

_A connector was then created in the MSK Connect console, using the custom plugin to route data from the Kafka topics to the S3 bucket. This involved setting the topics.regex field in the connector configuration to user-<your_UserId>.\* to ensure that all three Kafka topics were stored in the S3 bucket. Additionally, the IAM role used for authentication to the MSK cluster was specified in the Access permissions tab_

_Once the plugin and connector were set up, data passing through the IAM-authenticated Kafka cluster was automatically stored in the designated S3 bucket. This configuration ensured persistent storage of streamed data, providing a reliable backup and retrieval mechanism._

## Milestone 5: API Gateway and REST Proxy Configuration

The goal was to build an API that sends data to the MSK cluster:

- **API Setup:** The API Gateway was configured with a proxy+ resource, allowing for flexible data routing.
- **REST Proxy Configuration:** A REST proxy was installed on the EC2 instance, enabling the API to communicate with the Kafka cluster.
- **Data Emulation:** The user_posting_emulation.py script was modified to send data through the API to the Kafka topics, which was then stored in the S3 bucket.

_The API Gateway was configured with a proxy+ resource. This setup allows the API to handle various paths and methods dynamically. An HTTP ANY method was created for this resource. This method allows the API to accept any type of HTTP request (GET, POST, PUT, DELETE, etc.). The Endpoint URL was set to the public DNS of the EC2 instance, which was configured to run the Kafka REST Proxy. After the resource and method were configured, the API was deployed. The deployment stage was named test, and an Invoke URL was generated. This URL is crucial as it serves as the entry point for any API requests that interact with the MSK cluster._

_The Confluent Kafka REST Proxy was installed on the EC2 instance. This proxy acts as a bridge, allowing HTTP requests to interact with Kafka. The installation was performed using a downloaded package that was extracted and configured within the EC2 environment. The kafka-rest.properties file was modified to enable IAM authentication. This configuration is essential for secure communication with the MSK cluster. The bootstrap servers and the IAM role ARN were specified in the properties file to ensure proper authentication and connection to the Kafka cluster. Once configured, the Kafka REST Proxy was started on the EC2 instance. This proxy must run continuously to accept and forward API requests to the Kafka topics._

_The user_posting_emulation.py script was updated to send data to the Kafka topics via the newly created API. The script was modified to use the Invoke URL from the API Gateway as the destination for the POST requests. The script was structured to send data from three tables (pinterest_data, geolocation_data, user_data) to their respective Kafka topics. After running the script, the data flow was verified by checking the Kafka consumers on the EC2 instance to ensure that messages were being successfully consumed. Additionally, the S3 bucket was checked to confirm that the data was being stored correctly in the expected folder structure._

## Milestone 6: Databricks Setup and S3 Integration

This milestone transitioned the focus to Databricks, where data processing would occur:

- **Databricks Setup:** The environment was configured to use Spark for processing data.
- **S3 Bucket Mounting:** The S3 bucket was mounted to Databricks, allowing easy access to the data stored by the Kafka Connectors.
- **DataFrame Creation:** Data from the S3 bucket was read into Spark DataFrames, ready for transformation and analysis.

## Milestone 7: Data Cleaning and Transformation with Spark

This milestone involved cleaning and transforming the data using Spark:

- **Data Cleaning:** Each DataFrame (pin, geo, user) was cleaned by replacing null values, converting data types, and restructuring columns.
- **Complex Transformations:** The data was further transformed to enable analysis, such as finding the most popular categories and users by various metrics (e.g., by country, by year).
- **Joins and Aggregations:** The DataFrames were joined and aggregated to answer specific queries, such as identifying popular categories across different demographics.

## Milestone 8: Automating with AWS MWAA

The objective was to automate the entire data processing workflow using Airflow:

- **DAG Creation:** An Airflow DAG was created in VSCode and uploaded to an S3 bucket. This DAG orchestrated the execution of the Databricks notebook.
- **MWAA Integration:** The DAG was triggered in the Airflow UI, confirming successful execution and automation of the pipeline.

## Milestone 9: Real-Time Data Processing with AWS Kinesis

This milestone replaced Kafka with Kinesis to handle real-time data streaming:

- **Kinesis Stream Setup:** Three Kinesis data streams were created to replace the Kafka topics.
- **API Gateway Configuration:** The API was updated to send data to Kinesis instead of Kafka.
- **Real-Time Data Ingestion:** The Python script was modified to send data to the Kinesis streams. Data was then read into Databricks in real-time, transformed, and written to Delta tables.

## Conclusion

This project successfully simulated a real-world data pipeline using AWS and Databricks, handling both batch and stream processing scenarios. The pipeline is scalable, fault-tolerant, and capable of handling real-time data, providing a solid foundation for further expansion and integration into more complex data workflows.
