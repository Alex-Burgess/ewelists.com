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

Ewelists is based on a serverless architecture, with a microservice API backend.
