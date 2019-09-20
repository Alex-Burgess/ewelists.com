## Deployments
Github is the Single source of truth for our web stack and content deployments.  Whenever there is a commit/pull request to the Master branch of either the main or web github projects, this will trigger the pipeline.

The web pipeline doesn't include SSL certificate creation, although this could be automated in the future.  Therefore there is some setup required when creating the environments for the first time.  After this the pipeline is used for all changes.  

The Health Checks pipeline needs to create resources in us-east-1, as that is where the cloudfront metrics are recorded.  After hit a brick wall with using cross-region stacks in the web-pipeline I decided to create a separate pipeline just for this stack.

### Setup Staging Environment
1. **Web Stack:** Create Web stack with default SSL certificate.
    ```
    aws cloudformation create-stack --stack-name Web-Staging --template-body file://web.yaml \
      --parameters ParameterKey=Environment,ParameterValue=staging \
      ParameterKey=DefaultSSLCertificate,ParameterValue=true
    ```
1. **SSL Certificate:** Create SSL certificate. Stack will remain in CREATE_IN_PROGRESS state until the certificate is validated, so proceed to next step - see [acm docs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-certificatemanager-certificate.html) for more details.
    ```
    aws cloudformation create-stack --region us-east-1 --stack-name Web-SSL-Staging \
    --template-body file://web-sslcert.yaml \
    --parameters ParameterKey=Environment,ParameterValue=staging
    ```
1. **Validate SSL Certificate:** Validate certificate request using console (See [blog](https://aws.amazon.com/blogs/security/easier-certificate-validation-using-dns-with-aws-certificate-manager/) for steps).
1. **Parameter Store:** Create a parameter to store the SSL certificate ID.
    ```
    aws cloudformation describe-stacks --stack-name Web-SSL-Staging --region us-east-1 \
     --query 'Stacks[].Outputs[?OutputKey==`CertificateArn`].OutputValue' --output text | awk -F\/ '{print $2}'

    aws ssm put-parameter --name /ewelists.com/staging/SSLCertificateId --type String \
     --value "f38ecd9a-...."
    ```

### Setup Production Environment
As the hosted zone already exists for the production domain, we can skip creating the stack and go straight to creating the SSL certificate.

1. **SSL Certificate:** Create SSL certificate. Stack will remain in CREATE_IN_PROGRESS state until the certificate is validated, so proceed to next step - see [acm docs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-certificatemanager-certificate.html) for more details.
    ```
    aws cloudformation create-stack --region us-east-1 --stack-name Web-SSL-Prod \
     --template-body file://web-sslcert.yaml \
     --parameters ParameterKey=Environment,ParameterValue=prod
    ```
1. **Validate SSL Certificate:** Validate certificate request using console (See [blog](https://aws.amazon.com/blogs/security/easier-certificate-validation-using-dns-with-aws-certificate-manager/) for steps).
1. **Parameter Store:** Create a parameter to store the SSL certificate ID.
    ```
    aws cloudformation describe-stacks --stack-name Web-SSL-Prod --region us-east-1 \
     --query 'Stacks[].Outputs[?OutputKey==`CertificateArn`].OutputValue' --output text | awk -F\/ '{print $2}'

    aws ssm put-parameter --name /ewelists.com/prod/SSLCertificateId --type String \
     --value "f38ecd9a-...."
    ```

### Create Web CI/CD Pipeline
1. **Personal Access Token:** In github developer settings, create a Personal access token, with repo and admin:repo_hook scopes.
1. **Parameter Store:** Add github oauth key to parameter store.
    ```
    aws ssm put-parameter --name "/ewelists.com/github" --value "123456abcde...." --type SecureString
    ```
1. **Pipeline Stack:** Create the stack, using the cli to import the oauth token from the parameter store.
    ```
    aws cloudformation create-stack --stack-name Pipeline-Web \
     --template-body file://pipeline-web.yaml \
     --capabilities CAPABILITY_NAMED_IAM \
     --parameters ParameterKey=GitHubToken,ParameterValue=`aws ssm get-parameter --name "/ewelists.com/github" --with-decryption --query 'Parameter.Value' --output text`
    ```

### Update Web Pipeline
```
aws cloudformation update-stack --stack-name Pipeline-Web \
 --template-body file://pipeline-web.yaml \
 --capabilities CAPABILITY_NAMED_IAM \
 --parameters ParameterKey=GitHubToken,ParameterValue=`aws ssm get-parameter --name "/ewelists.com/github" --with-decryption --query 'Parameter.Value' --output text`
```

### Create Health Checks CI/CD Pipeline
Note: It is assumed that the github personal access token was created in the Create Web Pipeline steps.

1. **Pipeline Stack:** Create the stack, using the cli to import the oauth token from the parameter store.
    ```
    aws cloudformation create-stack --stack-name Pipeline-HealthChecks \
     --region us-east-1 \
     --template-body file://pipeline-healthchecks.yaml \
     --capabilities CAPABILITY_NAMED_IAM \
     --parameters ParameterKey=StagingCloudFrontId,ParameterValue=`aws cloudformation describe-stacks --stack-name Web-Staging --query 'Stacks[].Outputs[?OutputKey==`WebCloudFrontID`].OutputValue' --output text` \
      ParameterKey=ProdCloudFrontId,ParameterValue=`aws cloudformation describe-stacks --stack-name Web-Prod --query 'Stacks[].Outputs[?OutputKey==`WebCloudFrontID`].OutputValue' --output text` \
      ParameterKey=GitHubToken,ParameterValue=`aws ssm get-parameter --name "/ewelists.com/github" --with-decryption --query 'Parameter.Value' --output text`
    ```
1. **Validate Subscriptions:** Validate the SNS subscriptions created, by clicking on link in the emails.

### Update Health Checks Pipeline
```
aws cloudformation update-stack --stack-name Pipeline-HealthChecks \
 --region us-east-1 \
 --template-body file://pipeline-healthchecks.yaml \
 --capabilities CAPABILITY_NAMED_IAM \
 --parameters ParameterKey=StagingCloudFrontId,ParameterValue=`aws cloudformation describe-stacks --stack-name Web-Staging --query 'Stacks[].Outputs[?OutputKey==`WebCloudFrontID`].OutputValue' --output text` \
  ParameterKey=ProdCloudFrontId,ParameterValue=`aws cloudformation describe-stacks --stack-name Web-Prod --query 'Stacks[].Outputs[?OutputKey==`WebCloudFrontID`].OutputValue' --output text` \
  ParameterKey=GitHubToken,ParameterValue=`aws ssm get-parameter --name "/ewelists.com/github" --with-decryption --query 'Parameter.Value' --output text`
```
