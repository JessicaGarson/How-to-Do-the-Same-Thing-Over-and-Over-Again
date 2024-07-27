# How to Do the Same Thing Over and Over Again and Yield Differnt Results
Code from a talk outlining strategies for automating routine processes while ensuring that the outcomes adapt to changing requirements, enhancing project innovation and data accuracy.

## Render cron job example
This project consists of a Python script designed to send notifications about sunset times, allowing you to plan activities like running based on optimal light conditions. The script uses external APIs to fetch the sunset time for New York City and sends a notification one hour prior to sunset via Pushover.

### Features
- Fetch sunset times for New York City from the Sunrise Sunset API.
- Calculate the optimal time for activities based on sunset.
- Send notifications using the Pushover service.

### Prerequisites
Before you run this script, you need to have:

- Python 3.x installed.
- `requests` library installed, which can be done via `pip install requests`.
- An active account with Pushover with an application token and a user key.

### Environment Variables
Set the following environment variables in Render:

- `PUSHOVER_APP_TOKEN`: Your Pushover application token.
- `PUSHOVER_USER_KEY`: Your Pushover user key.

### Deployment on Render
1. Create a new Web Service on Render and link to the repository.
2. Set the environment variables in the "Environment" section of your Render service settings.
3. Choose Python as the environment and set the start command to `python running.py`.
4. Deploy the service.

### Usage
Once deployed, the script runs and checks the current sunset time daily, sending a notification an hour before sunset. Ensure the script is scheduled to run at least once a day at a time that precedes the earliest sunset time of the year.

### Cron syntax used
```
0 18 * * *
``` 

## Function examples
### GCP Function
This Google Cloud Function retrieves data on near-earth objects from NASA's API and updates an Elasticsearch index with the new data. It's triggered by messages on a Google Cloud Pub/Sub topic, making it well-suited for regular updates based on streaming data or periodic events.

#### Requirements
- Python 3.12
- `functions-framework` - For Google Cloud Function emulation and deployment.
- `requests` - For making HTTP requests.
- `pandas` - For data manipulation.
- `elasticsearch` - For interacting with Elasticsearch.

#### Set up environment variables
Set the following environment variables:
- `ELASTIC_CLOUD_ID`: Your Elasticsearch Cloud ID.
- `ELASTIC_API_KEY`: API Key for authenticating with Elasticsearch.
- `NASA_API_KEY`: API Key for accessing NASA's NEO API.

#### Deployment
To deploy this function to Google Cloud Functions:

1. **Create a Google Cloud Pub/Sub topic:**
2. **Deploy the function:**
3. **Schedule using Google Cloud Schedular**

#### Cron syntax used
```
0 8 * * * (America/New_York)
```

### Azure Function App
This Azure Function is designed to regularly fetch and update data from NASA's Near Earth Object (NEO) API into an Elasticsearch index. The function is triggered by a timer, making it suitable for periodic updates to keep the index current with the latest data.

#### Requirements
- Python 3.11
- [Azure's Visual Studio Code extension](https://code.visualstudio.com/docs/azure/extensions)
- `requests` - For HTTP requests to the NASA API.
- `pandas` - For data manipulation.
- `elasticsearch` - For interacting with Elasticsearch.
- `azure.functions` - For Azure Function bindings and triggers.

#### Configure environment variables:**
Set the following environment variables for your Azure and Elasticsearch configurations:
- `ELASTIC_CLOUD_ID`: Your Elasticsearch Cloud ID.
- `ELASTIC_API_KEY`: API Key for authenticating with Elasticsearch.
- `NASA_API_KEY`: API Key for accessing NASA's NEO API.

#### Deployment
Deploy this function to Azure Functions using the Azure Visual Studio code extension.

#### Cron syntax used
```
0 30 9 * * *
```

### AWS Lambda function
This AWS Lambda function retrieves data on near-earth objects from NASA's API, updates an Elasticsearch index with the new data, and logs the results. It is designed to run periodically to keep the Elasticsearch index updated with the latest data about near-earth objects.

#### Requirements
- Python 3.12
- `requests` - For API requests.
- `pandas` - For data manipulation.
- `elasticsearch` - For Elasticsearch operations.
- `os`, `logging` - For environment variable management and logging.

#### Set up environment variables
Set the following environment variables for your AWS and Elasticsearch configurations:
- `ELASTIC_CLOUD_ID`: Your Elasticsearch Cloud ID.
- `ELASTIC_API_KEY`: API Key for authenticating with Elasticsearch.
- `NASA_API_KEY`: API Key for accessing NASA's NEO API.

#### Deployment
This function is intended to be deployed as an AWS Lambda function.

1. **Package the Lambda function:**
Zip the necessary files including the dependencies.
2. **Create a new Lambda function:**
Use the AWS Management Console, AWS CLI, or your preferred infrastructure as code tool (like Terraform or AWS SAM) to deploy the function.
3. **Set a trigger:**
Configure a schedule to run this Lambda function periodically (e.g., daily using AWS CloudWatch).

#### Cron syntax used
```
0 10 * * ? *
```

## Operational testing 
You can find a notebook for creating an index and testing locally on [Elastic's Search Labs repository](https://github.com/elastic/elasticsearch-labs/blob/main/supporting-blog-content/keeping-your-index-current/local_testing.ipynb).

## Elasticsearch queries
The Elasticsearch queries run during this talk can be found [here](https://github.com/JessicaGarson/How-to-Do-the-Same-Thing-Over-and-Over-Again/blob/main/dev_tools.console).

## Resources
- [What is an Elasticsearch index?](https://www.elastic.co/blog/what-is-an-elasticsearch-index)
- [What Is a Cron Job: Understanding Cron Syntax and How to Configure Cron Jobs](https://www.hostinger.com/tutorials/cron-job)
- [Asteroids NeoWs API](https://data.nasa.gov/Space-Science/Asteroids-NeoWs-API/73uw-d9i8/about_data)
- [NASA API Overview](https://wilsjame.github.io/how-to-nasa/)
- [Downloading Python](https://wiki.python.org/moin/BeginnersGuide/Download)
- [NASA APIs](https://api.nasa.gov/)
- [Getting started with Elasticsearch](https://www.elastic.co/guide/en/elasticsearch/reference/current/getting-started.html)
- [Render cron jobs](https://docs.render.com/cronjobs)
- [Google Cloud Functions](https://cloud.google.com/functions?hl=en)
- [Crontab.guru](https://crontab.guru/)
- [Google Cloud Scheduler](https://cloud.google.com/scheduler)
- [PyEnv](https://github.com/pyenv/pyenv)
- [Develop Azure Functions by using Visual Studio Code](https://learn.microsoft.com/en-us/azure/azure-functions/functions-develop-vs-code?tabs=node-v4%2Cpython-v2)
- [Azure Functions overview](https://learn.microsoft.com/en-us/azure/azure-functions/functions-overview?pivots=programming-language-python)
- [AWS Lambda](https://aws.amazon.com/lambda/)
- [AWS Eventbridge](https://aws.amazon.com/eventbridge/)
- [AWS S3](https://aws.amazon.com/s3/)
- [Using cron and rate expressions to schedule rules in Amazon EventBridge](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-scheduled-rule-pattern.html)
- [Lambda Python package](https://docs.aws.amazon.com/lambda/latest/dg/python-package.html)
- [Automation using Cron Jobs: From Basics to Advanced](https://dev.to/devrx/automation-using-cron-jobs-from-basics-to-advanced-4e69)
- [Automate the Boring Stuff with Python](https://automatetheboringstuff.com)
