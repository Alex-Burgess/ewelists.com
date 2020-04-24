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

**High-level, end-to-end diagram**

![Main Architecture](documentationImages/MainArchitecture.png)

**Backend Lists API Services**

![Lists API](documentationImages/ListsApi.png)

**Backend Products API Services**

![Products API](documentationImages/ProductsApi.png)

**Backend NotFound API Services**

![NotFound API](documentationImages/NotfoundApi.png)

**Back Content API Services**

![Contact API](documentationImages/ContactApi.png)

## Implementation Details

### API Services

All services require Authorization, unless specified (+).

**Lists**

GET /lists (ListAll)
POST /lists (CreateList)

DELETE /lists/{:id} (Delete) <br />
GET /lists/{:id} (GetList) <br />
PUT /lists/{:id} (UpdateList)

POST /lists/{:id}/close (Close) <br />
GET /lists/{:id}/shared (GetSharedList) (+)

DELETE /lists/{:id}/product/{:productid} (DeleteProduct) <br />
POST /lists/{:id}/product/{:productid} (AddProduct) <br />
PUT /lists/{:id}/product/{:productid} (UpdateProduct)

POST /lists/{:id}/reserve/{:productid}/email/{email} (ReserveProduct) (+)

PUT /lists/purchase/{:reservationid}/email/{email} (Purchase) (+)

DELETE /lists/reservation/{:id} (DeleteReservation) (+) <br />
GET /lists/reservation/{:id} (Reservation) (+)

DELETE /lists/reserve/{:id}/email/{email} (UnreserveProduct) (+) <br />
PUT /lists/reserve/{:id}/email/{email} (UpdateProductReservation) (+)

**Products**

POST /products (CreateProduct) <br />
DELETE /products/{id} (Delete) <br />
GET /products/{id} (GetProduct) (+)

GET /products/url/{url} (SearchUrl)

**NotFound**

POST /notfound (CreateProduct) <br />
DELETE /notfound/{id} (Delete) <br />
GET /notfound/{id} (GetProduct) (+)

**Contact**

POST /contact (ContactUs) (+)

### User Sign up and Authentication
The following authentication methods are provided:
- Username (Email) and Password
- Google Federation
- Facebook Federation

The username in the Cognito User Pool is random uuid and we store the following user attributes:
- Name
- Email

Users can sign in with multiple methods, i.e. U&P and Google Federation.  If the same email address is used, we want to treat the different authentication methods as the same user, so we link the accounts in the User Pool, so that whatever method they user, we see the same Username id (a.k.a sub).  In order to achieve this we have a Pre sign-up Lambda function (SignUp), that checks if an account exists with the same email, when a user signs up.

If an account exists, the sign up process links the account and throws an exception.  If the sign up process was allowed to complete we would get a duplicate User Pool entry with a different Sub.  This means that the first time a user signs in with a social provider, the links processes needs to complete and effectively fail the sign up process.  The application handles this error and asks the user to sign in again with the same method.

**Handling Google Email Domains**

We have observed users using different google email domains, i.e. @gmail.com and @googlemail.com, both of which are valid for the same user google account.  In case of inconsistencies in the way users authenticate with their email address, during the signup process we check for the existence of both if it's a google email.  If the user has previously signed up with a different email address, we inform the user that an account exists.

In the main this works fine, unless the user is trying to sign in with a social provider that has a different email.  e.g. the user has signed up with user@googlemail.com, and they are attempting to sign in with Google Federation which uses user@gmail.com.  If this happens we just ask the user to sign in with their username and password, as we don't want a confusing/difficult experience for the user.

This situation is tricky because it seems that the user will not be able to sign into their Google account with user@googlemail.com, so the only resolution would be for the user to login with their username and password and update the email address to user@gmail.com.  At the moment we haven't implemented a method for a user to update their email, but doing so in the future would be good if the user wants to make their email usage consistent.

**LoginWithAmazon**

Initially the application made LoginWithAmazon available to users, however for now we have removed button from the login / sign up forms to reduce the number of scenarios that we have to support and hence the number of possible scenarios for errors/issues.  The configuration is still in place should we wish to re-enable it in the future.


## Setup

### Pre-Requisites
The API Gateway service must be given permissions to use the CloudWatch service for logging to work.  The creation of this role is a one-time task.

Create stack:
```
aws cloudformation create-stack --stack-name ApiGatewayCloudwatch-Role --template-body file://api-logging.yaml \
 --enable-termination-protection \
 --capabilities CAPABILITY_NAMED_IAM
```

### Test Environment
The steps below are used to build the test environment of the application.  The procedure is in 3 parts:
- Auth Infrastructure: Creates and configures the Cognito resources.
- Backend API services: Creates the lists, products and notfound
- Web Application

In the steps below, we create all the web components in one stack, except for the SSL certificate.  This is because the SSL needs to be created in the us-east-1 region and it also requires the hosted zone for the environment to be created, so that it can be validated.  The certificate ID is stored in a parameter store variable so that it can be programmatically referenced.

**Auth Infrastructure and Configuration**

1. Register with social IdPs: [Procedures](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-social-idp.html#cognito-user-pools-social-idp-step-1)
1. Add social identity providers to parameter store:
    ```
    aws ssm put-parameter --name /ewelists.com/test/Facebook/ClientId --type String --value "123456..."
    aws ssm put-parameter --name /ewelists.com/test/Facebook/ClientSecret --type String --value "123456..."

    aws ssm put-parameter --name /ewelists.com/test/Google/ClientId --type String --value "123456..."
    aws ssm put-parameter --name /ewelists.com/test/Google/ClientSecret --type String --value "123456..."

    aws ssm put-parameter --name /ewelists.com/test/Amazon/ClientId --type String --value "123456..."
    aws ssm put-parameter --name /ewelists.com/test/Amazon/ClientSecret --type String --value "123456..."
    ```
1. Create Auth stack (with termination protection):
    ```
    aws cloudformation create-stack --stack-name Auth-Test \
     --template-body file://auth.yaml \
     --capabilities CAPABILITY_NAMED_IAM \
     --enable-termination-protection \
     --parameters ParameterKey=Environment,ParameterValue=test \
        ParameterKey=SignUpFunction,ParameterValue=
    ```

1. Create SSM parameter with user pool ID, which is specified as an environment variable in the cf template for the signup lambda function.
    ```
    aws cloudformation describe-stacks --stack-name Auth-Test --query "Stacks[0].Outputs[?OutputKey=='userPoolId'].OutputValue" --output text

    aws ssm put-parameter --name /CognitoUserPoolId/test --type String --value "eu-west-1_abcd123e4"
    ```

**Backend DynamoDB Infrastructure**
Deploy stack with dynamodb tables.


**Backed API Services**

Build lists, notfound, products.  Then updated auth stack.

1. Update auth stack with Pre sign-up trigger Lambda function:
    ```
    aws cloudformation update-stack --stack-name Auth-Test \
     --template-body file://auth.yaml \
     --capabilities CAPABILITY_NAMED_IAM \
     --parameters ParameterKey=Environment,ParameterValue=test \
      ParameterKey=SignUpFunction,ParameterValue=lists-signup
    ```

1. Ensure that the required ses templates have been created (welcome)  See [Mail](documentation/mail.md) for more details.

1. **Test:**

**Web Application**

1. **Web Stack:** Create Web stack with default SSL certificate.
    ```
    aws cloudformation create-stack --stack-name Web-Test --template-body file://web.yaml \
      --parameters ParameterKey=Environment,ParameterValue=test \
      ParameterKey=DefaultSSLCertificate,ParameterValue=true
    ```
1. **Content:** Create a build of the content and copy to S3.
    ```
    npm run build
    mv build/staging.robots.txt build/robots.txt
    aws s3 sync build/ s3://test.ewelists.com --delete
    ```
1. **SSL Certificate:** Create SSL certificate. Stack will remain in CREATE_IN_PROGRESS state until the certificate is validated, so proceed to next step - see [acm docs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-certificatemanager-certificate.html) for more details.
    ```
    aws cloudformation create-stack --region us-east-1 --stack-name Web-SSL-Test \
    --template-body file://web-sslcert.yaml \
    --parameters ParameterKey=Environment,ParameterValue=test
    ```
1. **Validate SSL Certificate:** Validate certificate request using console (See [blog](https://aws.amazon.com/blogs/security/easier-certificate-validation-using-dns-with-aws-certificate-manager/) for steps).
1. **Parameter Store:** Create a parameter to store the SSL certificate ID.
    ```
    aws cloudformation describe-stacks --stack-name Web-SSL-Test --region us-east-1 \
     --query 'Stacks[].Outputs[?OutputKey==`CertificateArn`].OutputValue' --output text | awk -F\/ '{print $2}'

    aws ssm put-parameter --name /ewelists.com/test/SSLCertificateId --type String \
     --value "f38ecd9a-...."
    ```
1. **Update Web Stack:** Update the main stack to use the SSL certificate.
    ```
    aws cloudformation update-stack --stack-name Web-Test --template-body file://web.yaml \
      --parameters ParameterKey=Environment,ParameterValue=test
    ```
1. **Test:** Browse to https://test.ewelists.com (**Note:** Sign up and log in does not work unless User Pool Callback URLs are updated.)



**Notes**
1. Back up user pool (insert link)
### Staging / Production

Create auth stack:
```
aws cloudformation create-stack --stack-name Auth-Staging \
 --template-body file://auth.yaml \
 --capabilities CAPABILITY_NAMED_IAM \
 --enable-termination-protection \
 --parameters ParameterKey=Environment,ParameterValue=staging \
    ParameterKey=SignUpFunction,ParameterValue=
```

Updates to auth stack:
    ```
    aws cloudformation update-stack --stack-name Auth-Staging \
     --template-body file://auth.yaml \
     --capabilities CAPABILITY_NAMED_IAM \
     --parameters ParameterKey=Environment,ParameterValue=staging \
      ParameterKey=SignUpFunction,ParameterValue=lists-signup
    ```

### CI / CD Pipeline
Diagram details


## Deployment
