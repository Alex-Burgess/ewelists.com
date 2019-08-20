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
1. **Testing:** See [Initial Web Setup Tests](#initial-web-setup-tests) for quick curl tests.

## User Authentication
Useful AWS documentation: [Adding Social Identity Providers to a User Pool](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-social-idp.html)

### Create Authentication Setup
1. Create Auth stack (with termination protection):
    ```
    aws cloudformation create-stack --stack-name Auth-Test \
     --template-body file://auth.yaml \
     --capabilities CAPABILITY_NAMED_IAM \
     --parameters ParameterKey=Environment,ParameterValue=test \
     --enable-termination-protection
    ```
1. Configure UserPool:
  1. Callback URL(s): http://localhost:3000/
  1. Sign out URL(s): http://localhost:3000/
  1. Allowed OAuth Flows: Authorization code grant
  1. Allowed OAuth Scopes: email, openid, aws.cognito.signin.user.admin, profile.
  1. Domain Name: test-ewelists
1. Configuring social authentication with LoginWithAmazon.
  1. Create [Amazon](https://developer.amazon.com/login-with-amazon) developer account.
  1. Create Security Profile - [Steps](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-social-idp.html)
  1. Update app ID, secret and scope in Identity providers.
1. Configuring social authentication with Google
  1. Create [Google](https://console.developers.google.com) developer account.
  1. Create OAuth client IDs - [Steps](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-social-idp.html)
  1. Update app ID, secret and scope in Identity providers.
1. Configuring social authentication with Facebook
  1. Create [Facebook](https://developers.facebook.com/) developer account.
  1. Create App ID - [Steps](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-social-idp.html)
  1. Update app ID, secret and scope in Identity providers.
1. Enable all Identity Providers in App Client Settings and select Allowed OAuth Flows and Scopes (console).
1. Update Attribute mappings for the email attribute for each identity provider.
1. Add the configuration to the config.js file in the React Web App.

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
| Status Page | curl -sI https://test.ewelists.com/status.html | 200 |

### Robots Files
| Name | Command | Expected Result |
| --- | --- | --- |
| Test File | curl -sI https://test.ewelists.com/robots.txt | 200 <br> Disallow: / |
| Staging File | curl -sI https://staging.ewelists.com/robots.txt | 200 <br> Disallow: / |
| Prod File | curl -sI https://ewelists.com/robots.txt | 200 <br> Disallow: |

### Signup And Login Flows
| File | Test Details | Expected Result |
| --- | --- | --- |
| Sign up - links | Click on Terms and Conditions Link | Terms and Conditions page shown in new tab. |
| Sign up - links | Click on Privacy Policy Link | Privacy Policy page shown in new tab. |
| Sign up | Enter name, Username and Password | Confirmation code page shown.<br> Email with code sent. |
| Sign up - confirmation page | Enter confirmation code | Sign up complete, redirected to dashboard |
| Sign up - amazon | Click amazon icon.<br> Get login to amazon page.<br> Enter password and complete process. | "Ewelists would like to access to: Profile" message show.<br> Link to privacy policy on Allow decision page.<br>Login complete and redirected to dashboard. |
| Sign up - google | Click google icon.<br> Get login to google page.<br> Enter password and complete process. | Login page should have logo as well as working link to privacy policy and terms of service.<br>Login complete and redirected to dashboard. |
| Sign up - facebook | Click facebook icon.<br> Get login to facebook page.<br> Enter password and complete process. | After login see "Ewelists will receive..." message.<br> After "Continue as ..." login completed and redirected to dashboard page. |
| Login - links | Click on Terms and Conditions Link | Terms and Conditions page shown in new tab. |
| Login - links | Click on Privacy Policy Link | Privacy Policy page shown in new tab. |
| Login | Enter name, Username and Password | Login and redirected to dashboard |
| Login - amazon | Click amazon icon.<br> Get login to amazon page.<br> Enter password and complete process. | "Ewelists would like to access to: Profile" message show.<br> Link to privacy policy on Allow decision page.<br>Login complete and redirected to dashboard. |
| Login - google | Click google icon.<br> Get login to google page.<br> Enter password and complete process. | Login page should have logo as well as working link to privacy policy and terms of service.<br>Login complete and redirected to dashboard. |
| Login - facebook | Click facebook icon.<br> Get login to facebook page.<br> Enter password and complete process. | After login see "Ewelists will receive..." message.<br> After "Continue as ..." login completed and redirected to dashboard page. |
| Sign out - amazon | Click sign out link | Get redirected to login page |
| Sign out - google | Click sign out link | Get redirected to login page |
| Sign out - facebook | Click sign out link | Get redirected to login page |

## Monitoring
Route53 Health Checks can be used to monitoring the availability of the website.  Combining this with CloudWatch Alarms and SNS, it is then possible to send emails when issues occur.  In addition to basic availability monitoring, we also monitor requests received by the CloudFront distribution.

We want to monitor a page that has no cache, so that we alerted if there is an issue with underlying static website (i.e. on s3) a.s.a.p.  As files can be cached for days, there could be an issue and we wouldn't find out for hours, which would also be at the same time that users find out about the issue.  To facilitate this, we use a static html page with no cache.  For staging and production the buildspec file takes cache of copying this file with the correct no-cache metadata.

### Creating Monitoring
1. **CloudFront ID:** Get the Primary CloudFront Distribution ID
    ```
    aws cloudformation describe-stacks --stack-name Web-Test \
     --query 'Stacks[].Outputs[?OutputKey==`WebCloudFrontID`].OutputValue' --output text
    ```

1. **Health Checks:** Create the health checks stack (us-east-1)
    ```
    aws cloudformation create-stack --region us-east-1 --stack-name Web-HealthChecks-Test --template-body file://web-healthchecks.yaml \
     --parameters ParameterKey=Environment,ParameterValue=test \
      ParameterKey=CloudFrontId,ParameterValue=12345678910
    ```
1. **Confirm Subscription:** An email requesting confirmation of the subscription for the email address will be sent.  Click on the link to confirm the subscription.

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

### React
```
REACT_APP_STAGE=test npm start
REACT_APP_STAGE=test npm run build
aws s3 sync build/ s3://test.ewelists.com --delete
aws cloudfront list-distributions --query "DistributionList.Items[?AliasICPRecordals[?CNAME=='test.ewelists.com']].{ID:Id}" --output text
aws cloudfront create-invalidation --paths '/*' --distribution-id ABCDEFGHIJK12
```
