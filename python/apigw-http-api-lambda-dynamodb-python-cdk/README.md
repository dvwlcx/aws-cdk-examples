
# AWS API Gateway HTTP API to AWS Lambda in VPC to DynamoDB CDK Python Sample!


## Overview

Creates an [AWS Lambda](https://aws.amazon.com/lambda/) function writing to [Amazon DynamoDB](https://aws.amazon.com/dynamodb/) and invoked by [Amazon API Gateway](https://aws.amazon.com/api-gateway/) REST API. 

![architecture](docs/architecture.png)

## Monitoring and Observability

This stack implements AWS Well-Architected Framework best practices for monitoring and observability:

### End-to-End Tracing (REL06-BP07)
- **AWS X-Ray Tracing**: Enabled on API Gateway and Lambda for complete request tracing
- **DynamoDB Instrumentation**: Lambda function uses X-Ray SDK to trace DynamoDB operations
- **Service Map**: Visualize request flows through API Gateway → Lambda → DynamoDB in X-Ray console

### CloudWatch Alarms
- **Lambda Error Alarm**: Alerts when function errors occur
- **Lambda Throttle Alarm**: Alerts when function is throttled

After deployment, view traces in the [AWS X-Ray Console](https://console.aws.amazon.com/xray/) to analyze performance and debug issues.

## Security and Compliance

This stack implements AWS Well-Architected Framework best practices for security logging and compliance:

### Service and Application Logging (SEC04-BP01)
- **VPC Flow Logs**: Network traffic monitoring for security investigations
- **API Gateway Access Logs**: Comprehensive request auditing with caller identity, source IP, and request details
- **Lambda Function Logs**: Application logs with 1-year retention including security-relevant events (request ID, source IP, user agent)
- **DynamoDB Point-in-Time Recovery**: Continuous backup for data protection and forensic analysis

### Log Retention
All logs are retained for 1 year to meet compliance requirements and support security investigations.

### Prerequisites
- **AWS CloudTrail** should be enabled at the account or organization level to capture AWS API activity
- Ensure appropriate IAM permissions for log delivery to CloudWatch Logs (automatically handled by CDK)

After deployment, logs can be queried in [CloudWatch Logs Insights](https://console.aws.amazon.com/cloudwatch/home#logsV2:logs-insights) for security analysis and troubleshooting.

## Setup

The `cdk.json` file tells the CDK Toolkit how to execute your app.

This project is set up like a standard Python project.  The initialization
process also creates a virtualenv within this project, stored under the `.venv`
directory.  To create the virtualenv it assumes that there is a `python3`
(or `python` for Windows) executable in your path with access to the `venv`
package. If for any reason the automatic creation of the virtualenv fails,
you can create the virtualenv manually.

To manually create a virtualenv on MacOS and Linux:

```
$ python3 -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `pip install -r requirements.txt`
command.

## Deploy
At this point you can deploy the stack. 

Using the default profile

```
$ cdk deploy
```

With specific profile

```
$ cdk deploy --profile test
```

## After Deploy
Navigate to AWS API Gateway console and test the API with below sample data 
```json
{
    "year":"2023", 
    "title":"kkkg",
    "id":"12"
}
```

You should get below response 

```json
{"message": "Successfully inserted data!"}
```

### Viewing Traces
After making API requests, navigate to the AWS X-Ray console to view end-to-end traces showing:
- API Gateway request processing time
- Lambda function execution (including cold starts)
- DynamoDB operation latency
- Complete request timeline and service map

### Viewing Logs
Access logs in CloudWatch Logs console:
- **VPC Flow Logs**: Network traffic patterns and connection details
- **API Gateway Access Logs**: API request details including caller IP, method, path, and response status
- **Lambda Function Logs**: Application logs with request context and operation results

## Cleanup 
Run below script to delete AWS resources created by this sample stack.
```
cdk destroy
```

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Enjoy!
