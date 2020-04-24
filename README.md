# ewelists.com
This is the central repo and hence starting point of the documentation for this application.  There are a number of repositories that make up the full application.

- [Main](https://github.com/Alex-Burgess/ewelists.com) - Infrastructure templates for deploying the application
- [Web](https://github.com/Alex-Burgess/ewelists.com-web) - The Frontend React Application
- [Services](https://github.com/Alex-Burgess/ewelists.com-services) - The backend APIs for the main application
- [Admin](https://github.com/Alex-Burgess/ewelists.com-admin) - A collection of useful tools


## Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Implementation details](#implementation-details)
  - [Amazon DynamoDB](#amazon-dynamodb)
  - [Amazon API Gateway](#amazon-api-gateway)
  - [AWS Lambda](#aws-lambda)
- [Deploying Test Environment](#testing)
- [Deployments to Staging and Production](#deployments)
- [Testing](#testing)
- [Backup Procedures](#backups)
- [Monitoring](#monitoring)
- [Reference](#reference)


## Overview
Ewelists is based on a serverless architecture, where hosting/operating costs are in-line with usage of the application and so that AWS resource usage will automatically scale as demand increases over time or for periods of peak or increased demand, e.g. daily/weekly/monthly cycles or advertising campaigns.

**Front end**
- The front end is a React web application, based on the [Material Kit PRO React](https://demos.creative-tim.com/material-kit-pro-react/#/), to which custom pages, components, styling, etc has been added.
- The content is deployed to Amazon S3 and Amazon CloudFront provides a global distributed application.
- AWS Amplify provides the security layer for registering and authenticating users.
- We develop with a Mobile first approach.

**Back end**
- This is a microservice API architecture, using API gateway and Lambda, with functions written in Python.
- AWS SAM provides the framework for project structure, builds, packaging and deployment.

**Database**
- Amazon DynamoDB provides a "serverless" database, with "performance at scale"
- An [Adjaceny List Design Pattern](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-adjacency-graphs.html) is used to model the many-to-many relationships.

**Infrastructure**
- Route53 for DNS and monitoring
- Cognito for user data
- Parameter store for secrets
- SES for email
- CloudWatch for logging and alerting
- CodePipeline and CodeBuild for continuous deployments

## Architecture

## Implementation Details
