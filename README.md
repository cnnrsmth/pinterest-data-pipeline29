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

![Database Connection Setup](./Images/Milestone%201&2/create_db_connector_function.png)

![Successful Connection](./Images/Milestone%201&2/successful_connection.png)

_A Python script (run_infinite_post_data_loop) was implemented to simulate continuous data ingestion from Pinterest, emulating user interactions with the Pinterest API. The script fetched random rows from tables (pinterest_data, geolocation_data, user_data) and outputted them as key-value pairs._

![Infinite Data Loop](./Images/Milestone%201&2/infinite_data_loop.png)

## Milestone 3: EC2 Kafka Client Configuration

This milestone focused on setting up an EC2 instance to act as a Kafka client:

- **SSH Access:** A key pair was generated and used to SSH into the EC2 instance.
- **Kafka Installation:** Apache Kafka was installed on the EC2 instance, along with the necessary IAM MSK authentication jar, enabling secure communication with the MSK cluster.
- **Topic Creation:** Using the Kafka command-line tools, three topics (pin, geo, user) were created in the MSK cluster, ready to receive data.

_A key pair file was generated locally with a .pem extension, allowing secure SSH access to the EC2 instance. This key pair was retrieved from the AWS Parameter Store and saved locally. The key was used to establish an SSH connection to the EC2 instance, ensuring secure communication._

![SSH Connection](./Images/Milestone%203/ssh.png)

_Apache Kafka was installed on the EC2 instance. Alongside this, the IAM MSK authentication package was configured to enable secure communication between the EC2 client and the MSK cluster. The necessary environment variables were set to ensure proper path configurations and to establish the EC2 instance’s ability to use AWS IAM for MSK cluster authentication._

![EC2 IAM](./Images/Milestone%203/ec2-iam.png)

_The EC2 instance was configured to authenticate with the MSK cluster using IAM roles. This involved setting up trust relationships and modifying client properties to include the IAM role ARN, which grants the necessary permissions for cluster access._

![Client Properties](./Images/Milestone%203/client-properties.png)

_Three Kafka topics were created within the MSK cluster—pin, geo, and user. These topics were configured using the Kafka command-line tools, with bootstrap servers and Zookeeper connection strings retrieved from the MSK management console. The CLASSPATH environment variable was set appropriately to ensure seamless operation of the Kafka commands._

![MSK Cluster Information](./Images/Milestone%203/MSK-cluster-info.png)

![Create Topics](./Images/Milestone%203/create-topics.png)

## Milestone 4: Connecting MSK Cluster to S3 Bucket

The objective here was to ensure that data flowing through Kafka topics was automatically stored in an S3 bucket:

- **Plugin Creation:** A custom MSK Connect plugin was created using the Confluent S3 connector, which was uploaded to an S3 bucket.
- **Connector Configuration:** A connector was configured within MSK Connect to route data from the Kafka topics to corresponding S3 buckets, ensuring persistent storage of streamed data.

_A custom plugin was created using the Confluent.io Amazon S3 Connector. This plugin was designed to manage the transfer of data from the Kafka topics to the designated S3 bucket. The plugin was downloaded to the EC2 client and then uploaded to an S3 bucket._

_The S3 bucket was already configured with the necessary VPC endpoint and IAM roles, eliminating the need for additional setup_

_A connector was then created in the MSK Connect console, using the custom plugin to route data from the Kafka topics to the S3 bucket. This involved setting the topics.regex field in the connector configuration to user-<your_UserId>.\* to ensure that all three Kafka topics were stored in the S3 bucket. Additionally, the IAM role used for authentication to the MSK cluster was specified in the Access permissions tab_

_Once the plugin and connector were set up, data passing through the IAM-authenticated Kafka cluster was automatically stored in the designated S3 bucket. This configuration ensured persistent storage of streamed data, providing a reliable backup and retrieval mechanism._

![kafka-connect-zip](./Images/Milestone%204/kafka-connect-zip.png)

![customised-plugin](./Images/Milestone%204/customised-plugin.png)

![connector](./Images/Milestone%204/connector.png)

## Milestone 5: API Gateway and REST Proxy Configuration

The goal was to build an API that sends data to the MSK cluster:

- **API Setup:** The API Gateway was configured with a proxy+ resource, allowing for flexible data routing.
- **REST Proxy Configuration:** A REST proxy was installed on the EC2 instance, enabling the API to communicate with the Kafka cluster.
- **Data Emulation:** The user_posting_emulation.py script was modified to send data through the API to the Kafka topics, which was then stored in the S3 bucket.

_The API Gateway was configured with a proxy+ resource. This setup allows the API to handle various paths and methods dynamically. An HTTP ANY method was created for this resource. This method allows the API to accept any type of HTTP request (GET, POST, PUT, DELETE, etc.). The Endpoint URL was set to the public DNS of the EC2 instance, which was configured to run the Kafka REST Proxy. After the resource and method were configured, the API was deployed. The deployment stage was named test, and an Invoke URL was generated. This URL is crucial as it serves as the entry point for any API requests that interact with the MSK cluster._

![api-gateway](./Images/Milestone%205/API-gateway.png)

![integration-type](./Images/Milestone%205/API-integration-type.png)

![test-stage](./Images/Milestone%205/test-stage.png)

_The Confluent Kafka REST Proxy was installed on the EC2 instance. This proxy acts as a bridge, allowing HTTP requests to interact with Kafka. The installation was performed using a downloaded package that was extracted and configured within the EC2 environment. The kafka-rest.properties file was modified to enable IAM authentication. This configuration is essential for secure communication with the MSK cluster. The bootstrap servers and the IAM role ARN were specified in the properties file to ensure proper authentication and connection to the Kafka cluster. Once configured, the Kafka REST Proxy was started on the EC2 instance. This proxy must run continuously to accept and forward API requests to the Kafka topics._

![kafka-rest.properties](./Images/Milestone%205/kafka-rest-properties.png)

![server-start](./Images/Milestone%205/server-start.png)

_The user_posting_emulation.py script was updated to send data to the Kafka topics via the newly created API. The script was modified to use the Invoke URL from the API Gateway as the destination for the POST requests. The script was structured to send data from three tables (pinterest_data, geolocation_data, user_data) to their respective Kafka topics. After running the script, the data flow was verified by checking the Kafka consumers on the EC2 instance to ensure that messages were being successfully consumed. Additionally, the S3 bucket was checked to confirm that the data was being stored correctly in the expected folder structure._

![invoke-api](./Images/Milestone%205/invoke-api.png)

![pin-payload](./Images/Milestone%205/pin-payload.png)
![geo&usr-payloads](./Images/Milestone%205/geo&usr-payload.png)

![s3-topics](./Images/Milestone%205/s3-topics.png)
![data-extract-example](./Images/Milestone%205/data-example.png)

## Milestone 6: Databricks Setup and S3 Integration

This milestone transitioned the focus to Databricks, where data processing would occur:

- **Databricks Setup:** The environment was configured to use Spark for processing data.
- **S3 Bucket Mounting:** The S3 bucket was mounted to Databricks, allowing easy access to the data stored by the Kafka Connectors.
- **DataFrame Creation:** Data from the S3 bucket was read into Spark DataFrames, ready for transformation and analysis.

_A Databricks account was configured to serve as the primary environment for processing the Pinterest data. After setting up the account, essential libraries for interacting with AWS services and processing data in Spark were imported._

_The S3 bucket, which was previously used to store Kafka stream data, was mounted to the Databricks environment. This step ensured seamless access to the data stored in the bucket, allowing it to be read directly into Spark DataFrames for further processing. The credentials for accessing the S3 bucket were securely handled, ensuring that the connection was both secure and efficient._

![mount](./Images/Milestone%206/mount.png)

_With the S3 bucket mounted, the JSON data stored in the bucket was read into Spark DataFrames. Separate DataFrames were created for each type of data—Pinterest post data (df_pin), geolocation data (df_geo), and user data (df_user). These DataFrames served as the foundation for subsequent data cleaning, transformation, and analysis tasks within Databricks._

![pin-df](./Images/Milestone%206/pin-df.png)

![geo-df](./Images/Milestone%206/geo-df.png)

![user-df](./Images/Milestone%206/user-df.png)

## Milestone 7: Data Cleaning and Transformation with Spark

This milestone involved cleaning and transforming the data using Spark:

- **Data Cleaning:** Each DataFrame (pin, geo, user) was cleaned by replacing null values, converting data types, and restructuring columns.
- **Complex Transformations:** The data was further transformed to enable analysis, such as finding the most popular categories and users by various metrics (e.g., by country, by year).
- **Joins and Aggregations:** The DataFrames were joined and aggregated to answer specific queries, such as identifying popular categories across different demographics.

_Cleaning operations included:_

- _**Replacing Null Values**: Replaced irrelevant or empty entries with None._
- _**Data Type Conversion**: The follower_count column in df_pin was converted from a string to an integer by removing non-numeric characters and standardizing the format (e.g., converting "k" and "M" to their numerical equivalents)._
- _**Column Reordering and Renaming**: Renamed columns for clarity and reordered them to match our analysis requirements. For instance, index was renamed to ind and positioned at the start of each DataFrame for consistency._

_Transformation operations included:_

- _**Creating Derived Columns**: Created new columns such as coordinates in df_geo by combining latitude and longitude values, and user_name in df_user by concatenating first_name and last_name._
- _**Time-based Transformations**: Converted timestamp strings into datetime objects to facilitate time-based analyses._

![cleaned-transformed-pin](./Images/Milestone%207/cleaned-pin.png)

![cleaned-transformed-geo](./Images/Milestone%207/cleaned-geo.png)

![cleaned-transformed-user](./Images/Milestone%207/cleaned-user.png)

_Joins and Aggregations included:_

- _**Most Popular Category by Country**: Joined df_pin and df_geo using the ind column and used groupBy and agg to count the occurrences of each category within each country. Employed a window function to partition the data by country and order by the category count to determine the most popular categories._
- _**Most Popular Category by Year**: A similar approach was used to find the most popular categories each year, focusing on the timestamp column to extract and analyze year-wise trends._
- _**Most Popular User by Country**: By joining df_pin and df_user, was able to group the data by country and identified users with the highest follower counts in each region._
- _**Age-based Analysis**: Created an age_group column in df_user and performed age-wise analysis to determine the most popular categories and median follower counts for different age groups._
- _**Time-based User Analysis**: Analyzed user activity over time, focusing on the number of users joining each year and their median follower counts. We employed Window functions and percentile_approx for calculating the median, ensuring robust statistical insights._

![question-1](./Images/Milestone%207/1-popular-post-categories.png)

![question-2](./Images/Milestone%207/2-timebound-posts.png)

![question-3](./Images/Milestone%207/3-most-followers.png)

![question-4](./Images/Milestone%207/4-popular-categories.png)

![question-5](./Images/Milestone%207/5-median-follower-count.png)

![question-6](./Images/Milestone%207/6-timebound-join.png)

![question-7](./Images/Milestone%207/7-timebound-median-follower.png)

![question-8](./Images/Milestone%207/8-timebound-median-follower-age.png)

## Milestone 8: Automating with AWS MWAA

The objective was to automate the entire data processing workflow using Airflow:

- **DAG Creation:** An Airflow DAG was created in VSCode and uploaded to an S3 bucket. This DAG orchestrated the execution of the Databricks notebook.
- **MWAA Integration:** The DAG was triggered in the Airflow UI, confirming successful execution and automation of the pipeline.

_A Directed Acyclic Graph (DAG) was constructed in VSCode to define the sequence of tasks that needed to be executed within Databricks. The DAG was designed to trigger the execution of a Databricks notebook, handling the complete ETL process. The DAG was scripted to be reusable and was uploaded to an S3 bucket dedicated to MWAA (mwaa-dags-bucket), ensuring it could be scheduled and managed through the Airflow UI._

_The process included:_

- _**Environment Configuration**: The MWAA environment, pre-configured with access to necessary AWS resources, was leveraged for the DAG deployment. The environment also had access to Databricks through an API, allowing seamless integration._
- _**DAG Scheduling**: The DAG was configured with a daily schedule, ensuring the ETL processes were executed at regular intervals without manual intervention. Error handling and retry mechanisms were incorporated into the DAG to account for any potential failures during execution._
- _**Task Orchestration**: Each task within the DAG represented a step in the data pipeline, from reading data from S3 to processing it in Databricks. The DAG was designed to handle dependencies between tasks, ensuring they executed in the correct sequence._

![DAG-script](./Images/Milestone%208/dag-script.png)

_The DAG was uploaded to the MWAA environment and manually triggered through the Airflow UI to verify the correctness of the setup. The successful execution of the DAG confirmed that the automation pipeline was functioning as expected, with the Databricks notebook running end-to-end, processing data as per the defined tasks. The entire workflow was now automated, eliminating the need for manual triggers and enabling consistent and repeatable data processing operations._

![S3-DAG-Upload](./Images/Milestone%208/S3-dag.png)

![Airflow-DAG](./Images/Milestone%208/Airflow-DAG-UI.png)

![Databricks-DAG-Triggered-Job](./Images/Milestone%208/Databricks-DAG-Triggered-Job.png)

## Milestone 9: Real-Time Data Processing with AWS Kinesis

This milestone replaced Kafka with Kinesis to handle real-time data streaming:

_While batch processing (previous milestones) involves handling data in large blocks at scheduled intervals, stream processing deals with continuous data flow, allowing for real-time insights._

- **Kinesis Stream Setup:** Three Kinesis data streams were created to replace the Kafka topics.
- **API Gateway Configuration:** The API was updated to send data to Kinesis instead of Kafka.
- **Real-Time Data Ingestion:** The Python script was modified to send data to the Kinesis streams. Data was then read into Databricks in real-time, transformed, and written to Delta tables.

_Kinesis Setup steps:_

- _**Kinesis Streams**: Three Kinesis streams were created to handle data that was previously processed using Kafka. These streams are specifically named for Pinterest's pin, geo, and user data tables._
- _**API Gateway Configuration**: The existing API was modified to route data to these Kinesis streams instead of Kafka. This ensured that data generated by the user_posting_emulation.py script would now be sent to Kinesis._
- _**Data Ingestion**: A new Python script, user_posting_emulation_streaming.py, was implemented. This script sends data in real-time to the Kinesis streams, emulating continuous user interaction with the Pinterest platform._

![Kinesis](./Images/Milestone%209/1-Kinesis-Streams.png)

![API-Gateway](./Images/Milestone%209/2-API-Gateway.png)

![Python-Script-Producer-1](./Images/Milestone%209/3a-Data-to-Kinesis.png)

![Python-Script-Producer-2](./Images/Milestone%209/3b-Data-to-Kinesis.png)

![Send-it-Babyyy-1](./Images/Milestone%209/4-Python-Data-Generation.png)

![Kinesis-Geo](./Images/Milestone%209/5a-Geo-Kinesis.png)

![Kinesis-Pin](./Images/Milestone%209/5b-Pin-Kinesis.png)

![Kinesis-User](./Images/Milestone%209/5c-User-Kinesis.png)

_Kinesis and Databricks Integration steps:_

- _**Real-Time Data Reading**: Databricks was set up to read the data directly from Kinesis streams in real-time. This involved configuring a new Databricks notebook to connect with the Kinesis streams using appropriate credentials and ingesting the streaming data._
- _**Data Transformation**: Once ingested, the streaming data underwent similar cleaning and transformation processes as the batch data. This included handling missing values, converting data types, and reordering columns._
- _**Writing to Delta Tables**: The transformed streaming data was written to Delta tables within Databricks. These tables, named after the user ID, ensured that the real-time data was stored efficiently and was readily accessible for further analysis or queries._

![Databricks-Setup](./Images/Milestone%209/6a-Databricks-Setup.png)

![Databricks-PIN](./Images/Milestone%209/6b-Databricks-PIN.png)

![Databricks-Geo](./Images/Milestone%209/6c-Databricks-Geo.png)

![Databricks-Geo](./Images/Milestone%209/6d-Databricks-User.png)

![Live-Data-Pin](./Images/Milestone%209/7a-Live-Pin-Data.png)

![Live-Data-Geo](./Images/Milestone%209/7b-Live-Geo-Data.png)

![Live-Data-User](./Images/Milestone%209/7c-Live-User-Data.png)

![Clean-Data-Pin](./Images/Milestone%209/8a-Live-Clean-PIN.png)

![Clean-Data-Geo](./Images/Milestone%209/8b-Live-Clean-Geo.png)

![Clean-Data-User](./Images/Milestone%209/8c-Live-Clean-User.png)

![Write-to-Tables](./Images/Milestone%209/9-Write-Data-to-Table.png)

![Geo-Table](./Images/Milestone%209/9a-cleaned-geo-date.png)

![Geo-Table](./Images/Milestone%209/9b-cleaned-pin-data.png)

![Geo-Table](./Images/Milestone%209/9c-cleaned-user-data.png)

## Conclusion

This project successfully simulated a real-world data pipeline using AWS and Databricks, handling both batch and stream processing scenarios. The pipeline is scalable, fault-tolerant, and capable of handling real-time data, providing a solid foundation for further expansion and integration into more complex data workflows.
