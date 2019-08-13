# ewelists.com
The main ewelists.com project


## Web Stack

### Create a Test Environment
In the steps below, we create all the web components in one stack, except for the SSL certificate.  This is because the SSL needs to be created in the us-east-1 region and it also requires the hosted zone for the environment to be created, so that it can be validated.  The certificate ID is stored in a parameter store variable so that it can be programmatically referenced.

1. **Web Stack:** Create Web stack with default SSL certificate.
    ```
    aws cloudformation create-stack --stack-name Web-Test --template-body file://web.yaml \
      --parameters ParameterKey=Environment,ParameterValue=test \
      ParameterKey=DefaultSSLCertificate,ParameterValue=true
    ```
1. **Content:** Create a build of the content and copy to S3.
    ```
    npm run build
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
1. **Testing:** See [Initial Web Setup Tests](#initial-web-setup-tests) for quick curl tests.

## Deployments
Github is the Single source of truth for our web stack and content deployments.  Whenever there is a commit/pull request to the Master branch of either the main or web github projects, this will trigger the pipeline.

The pipeline doesn't include SSL certificate creation, although this could be automated in the future.  Therefore there is some setup required when creating the environments for the first time.  After this the pipeline is used for all changes.  

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

### Create CI/CD Pipeline
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

### Update Pipeline
```
aws cloudformation update-stack --stack-name Pipeline-Web \
 --template-body file://pipeline-web.yaml \
 --capabilities CAPABILITY_NAMED_IAM \
 --parameters ParameterKey=GitHubToken,ParameterValue=`aws ssm get-parameter --name "/ewelists.com/github" --with-decryption --query 'Parameter.Value' --output text`
```

## Testing

### Initial Web Setup Tests

| Name | Command | Expected Result |
| --- | --- | --- |
| Main domain success | curl -sI https://test.ewelists.com | 200 |
| http to https redirect | curl -sI http://test.ewelists.com | 301 Moved Permanently |
| www to root redirects | curl -sI http://www.test.ewelists.com <br> curl -sI https://www.test.ewelists.com | 301 Moved Permanently |
| .co.uk redirects | curl -sI http://test.ewelists.co.uk <br> curl -sI https://test.ewelists.co.uk <br> curl -sI http://www.test.ewelists.co.uk <br> curl -sI https://www.test.ewelists.co.uk | 301 Moved Permanently |
| Page missing | https://test.ewelists.com/nopage | 200 (404 shown in browser) |
| S3 Request | curl -sI http://test.ewelists.com.s3-website-eu-west-1.amazonaws.com | 301 <br> Location: http://test.ewelists.com/ |
| S3 Request to missing file | curl -sI http://test.ewelists.com.s3-website-eu-west-1.amazonaws.com/nopage | 301 <br> Location: http://test.ewelists.com/ |




# Reference
### AWS Cli Authentication
To generate a session for the required AWS profile:
```
. aws-auth --profile_name ListsMain --token_code 123456 [--duration 18000]
```

### Github Administration
The master branch will be the latest working code. To clone the project:
```
git clone git@github.com:Alex-Burgess/ewelists.com.git
```

Versioning is used to track changes to config, code and procedures. To create a version tag:
```
git tag -a v0.0.1 -m "Tag description..."
git push origin v0.0.1
```

### CloudFront Cache Invalidations
Cloudfronts default cache is set to 1 day.  if you have updated content you need to “invalidate the objects” that are currently being server by the cache.  To do this for a file, specific /index.html, or for the whole site, /*

```
aws cloudfront list-distributions --query 'DistributionList.Items[*].{ID:Id, DomainName:Origins.Items[*].DomainName}'
aws cloudfront create-invalidation --distribution-id ABCDEFGHIJK12 --paths '/*'
aws cloudfront wait invalidation-completed --distribution-id ABCDEFGHIJK12 --id ABCDEFG1234567
```

Or with file:
```
aws cloudfront create-invalidation --distribution-id EPHRMSYQN7X62 --invalidation-batch file://all.html
```

Check status of invalidation:
```
aws cloudfront get-invalidation --distribution-id ABCDEFGHIJK12 --id ABCDEFG1234567 --query 'Invalidation.Status'
```
