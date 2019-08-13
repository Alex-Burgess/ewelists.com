# ewelists.com
Main ewelists.com project


## Web Stack

### Create a Test Environment
The architecture employed here, uses

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
